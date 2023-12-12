
from db_operations import connect_to_mongodb
from tweets_manager import handle_each_tweet, get_last_processed_time, last_processed_time
from dotenv import load_dotenv
from tweepy.asynchronous import AsyncClient
import os
import logging
import asyncio
from nltk import download as nltk_download
nltk_download('punkt')

load_dotenv()

# Logger Setup


def setup_logger():
    """
    Set up the logger for the application.
    """
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        format='[%(asctime)s] [%(levelname)s]   %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        force=True
    )
    return logger


logger = setup_logger()
# Last Processed Time Setup


async def twitter_bot(db):
    """
    Main function to run the Twitter bot.
    """
    global last_processed_time
    try:
        logger.info("Twitter bot started")

        # Initialize Tweepy Client
        client = AsyncClient(bearer_token=os.getenv("BEARER_TOKEN"), return_type=dict,
                             wait_on_rate_limit=True)

        # Fetch latest tweets since the last processed tweet
        logger.info("Fetching latest tweets")

        query = "(@nvctranslator OR @eli5translator OR @adulttranslator) is:reply -is:retweet -is:quote -from:nvctranslator -to:nvctranslator -from:eli5translator -to:eli5translator -from:adulttranslator -to:adulttranslator"

        # Your Twitter API request
        latest_tweets = await client.search_recent_tweets(
            query=query,
            tweet_fields=["created_at", "author_id", "note_tweet"],
            expansions=["in_reply_to_user_id", "referenced_tweets.id",
                        'author_id'],
            user_fields=['username', 'name', 'profile_image_url'],
            max_results=10,
            start_time=get_last_processed_time(),
        )

        if 'data' in latest_tweets:
            semaphore = asyncio.Semaphore(50)
            tasks = [asyncio.create_task(handle_each_tweet(
                tweet_data={'tweet': tweet, 'latest_tweets': latest_tweets}, index=index, semaphore=semaphore, db=db)) for index, tweet in enumerate(latest_tweets['data'])]
            await asyncio.gather(*tasks)

        else:
            logger.warning('No latest_tweets found')

    except Exception as e:
        logger.error(f"error in twitter bot function :-{e}")


async def main():
    db = await connect_to_mongodb()
    while 1:
        WAIT_TIME = 16  # secs
        await asyncio.gather(twitter_bot(db=db), asyncio.sleep(WAIT_TIME))

if __name__ == "__main__":
    asyncio.run(main())
