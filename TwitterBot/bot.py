
import os
import re
import logging
import asyncio
from datetime import datetime, timedelta
from nltk import download as nltk_download
from tweepy.asynchronous import AsyncClient
from dotenv import load_dotenv
from openai import AsyncOpenAI
import motor.motor_asyncio
import nltk

# NLTK setup
nltk_download('punkt')


# Environment Variables Setup

def load_env_variables():
    """
    Load environment variables from the .env file.
    """
    load_dotenv()
    return {
        "bearer_token": os.getenv("BEARER_TOKEN"),
        "api_key": os.getenv("CONSUMER_KEY"),
        "api_secret": os.getenv("CONSUMER_SECRET"),
        "access_token": os.getenv("ACCESS_TOKEN_KEY"),
        "access_secret": os.getenv("ACCESS_TOKEN_SECRET"),
        "openai_key": os.getenv('OPENAI'),
        "mongo_uri": os.getenv('MONGOURL'),
        "host_url": os.getenv('HOST_URL')
    }


env_vars = load_env_variables()

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

# Configuration Constants
DATABASE_NAME = "nvctranslator"
COLLECTION_NAME = "tweets"
OPENAI_CLIENT = AsyncOpenAI(api_key=os.environ['OPENAI'])

# Last Processed Time Setup
last_processed_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')


def get_last_processed_time():
    """
    Get the last processed time for tweets.
    """
    global last_processed_time
    return last_processed_time


def set_last_processed_time(tweet_time):
    """
    Set the last processed time after processing a tweet.
    """
    global last_processed_time
    last_processed_time = tweet_time


async def connect_to_mongodb() -> motor.motor_asyncio.AsyncIOMotorDatabase:
    """
    Establishes a connection to the MongoDB database.
    """
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(env_vars['mongo_uri'])
        logging.info('Connected to MongoDB')
        return client[DATABASE_NAME]
    except Exception as e:
        logging.error(f'Error while connecting to MongoDB: {e}')
        return None


async def get_tweet_by_id(db, tweet_id: str):
    """
    Retrieves a tweet by its ID from the database.
    """
    try:
        tweet = await db[COLLECTION_NAME].find_one({"tweet_id": tweet_id})
        logger.info(f'Successfully retrieved tweet with id: {tweet_id}')
        return tweet
    except Exception as e:
        logger.error(f'Error retrieving tweet: {e}')
        return None


async def insert_tweet(db, tweet_id: str, sentences: list):
    """
    Inserts a tweet into the database.
    """
    try:
        tweet_data = {"translated_text": "<<>>".join(
            sentences), "tweet_id": tweet_id}
        await db[COLLECTION_NAME].insert_one(tweet_data)
        logger.info(f'Successfully inserted tweet with id: {tweet_id}')
    except Exception as e:
        logger.error(f'Error inserting tweet: {e}')

#  NVC Translation and Text Processing


def remove_urls(text: str):
    """
    Remove the urls and hastags from the given text.
    """
    # Remove URLs
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    text = re.sub(url_pattern, '', text)

    return text


def create_sentences(text: str) -> list:
    """
    Splits the given text into sentences.
    """
    sentences = []
    for batch in text.split('\n'):
        sentences.extend(nltk.sent_tokenize(batch))
        sentences.append('\n')
    return sentences


def divide_into_tweets(sentences: list, username_who_posted: str, max_length: int = 275, max_tweets: int = 5,) -> list:
    """
    Divides a list of text into tweets, each not exceeding the max_length.
    """
    tweets = []
    current_tweet = f"Here is @{username_who_posted}’s message in a form of non-violent communication:\n\n"
    for sentence in sentences:
        if len(current_tweet) + len(sentence) + 1 <= max_length:
            current_tweet += " " + \
                sentence if (current_tweet and sentence != '\n') else sentence
        else:
            words = nltk.word_tokenize(sentence)
            for word in words:
                if len(current_tweet) + len(word) + 1 <= max_length:
                    current_tweet += " " + \
                        word if (current_tweet and sentence != '\n') else word
                else:
                    tweets.append(current_tweet)
                    current_tweet = word
                    if len(tweets) == max_tweets:
                        return tweets

        if len(tweets) == max_tweets:
            break

    if current_tweet and len(tweets) < max_tweets:
        tweets.append(current_tweet)

    return tweets


async def get_text_from_GPT(text: str) -> str:
    """
    Retrieves text rephrased using GPT from OpenAI.
    """
    if (text == '\n' or text == " " or text == "" or len(text) < 5):
        return text
    try:
        prompt = f"""
        Please Rephrase the following text into Nonviolent Communication (NVC) language. Ensure that the translation:
        1. Is direct and does not include introductory phrases such as 'NVC Language:'
        2. Has a length comparable to the original text.
        3. DO translation word by word that is change only those words which require translation

        Original Text:
        "{text}"
        """
        response = await OPENAI_CLIENT.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": prompt
            }],
            temperature=0.1,
            max_tokens=50
        )
        if ("I'm sorry, but I am unable to translate the text" in response.choices[0].message.content):
            return text
        return response.choices[0].message.content.replace('"', '')
    except Exception as e:
        logger.error(f'Error in GPT processing: {e}')
        return ""


async def nvctranslator(full_text: str, username_who_posted: str) -> tuple:
    """
    Translates the provided text to NVC using GPT and divides it into tweets.
    """
    sentences = create_sentences(text=full_text)
    tasks = [
        asyncio.create_task(get_text_from_GPT(text=sentence))
        for sentence in sentences[:20]
    ]
    results = await asyncio.gather(*tasks)
    tweets = divide_into_tweets(
        sentences=results, username_who_posted=username_who_posted)
    return (tweets, sentences[20:], results)


async def handle_remaining_tweet_text(to_convert: list, converted: list, db, tweet_id: str):
    """
    Handles the remaining text for conversion and inserts into the database.
    """
    all_converted_text = converted + await asyncio.gather(
        *[asyncio.create_task(get_text_from_GPT(text)) for text in to_convert]
    )
    await insert_tweet(db, tweet_id, all_converted_text)


async def reply_to_tweet(tweet_id: str, reply_text: str, repy_tweet_id: str):
    """
    Replies to a tweet with the given text.
    """
    try:

        client = AsyncClient(bearer_token=env_vars['bearer_token'], consumer_key=env_vars['api_key'], consumer_secret=env_vars['api_secret'],
                             access_token=env_vars['access_token'], access_token_secret=env_vars['access_secret'])
        tweet_id_to_reply = tweet_id
        for i in range(0, len(reply_text)):
            tweet_reply_text = reply_text[i]
            status = await client.create_tweet(text=str(tweet_reply_text), in_reply_to_tweet_id=tweet_id_to_reply)
            tweet_id_to_reply = status[0]['id']

        if (len(reply_text) >= 2):
            base_url = env_vars['host_url']
            url_link = base_url+repy_tweet_id
            final_text = f"Complete text available at {url_link}"
            await client.create_tweet(text=str(final_text), in_reply_to_tweet_id=tweet_id_to_reply)

        logger.info("Successfully replied to tweet")

    except Exception as e:

        logger.error(f"Error replying to tweet {tweet_id}: {e}")


async def handle_each_tweet(semaphore: asyncio.Semaphore, tweet_data: dict, index: int, db):
    """
    Handles each tweet fetched from Twitter.
    """
    async with semaphore:
        try:

            # Get tweet details
            tweet_id = tweet_data['tweet']['id']
            tweet_created_at = tweet_data['tweet']['created_at']

            # Update the newest tweet time
            created_time = (datetime.strptime(
                tweet_created_at, '%Y-%m-%dT%H:%M:%S.%fZ')+timedelta(seconds=1)).strftime('%Y-%m-%dT%H:%M:%SZ')

            # Save the time of the most recent tweet processed
            if (index == 0):
                set_last_processed_time(created_time)

             # Get tweet details
            in_reply_to_tweet_id = None
            if ('referenced_tweets' in tweet_data['tweet']):
                in_reply_to_tweet_id = next(
                    (ref_tweet['id'] for ref_tweet in tweet_data['tweet']['referenced_tweets'] if ref_tweet['type'] == 'replied_to'), None)

            if (in_reply_to_tweet_id):
                # Get user details
                in_reply_to_user_id = tweet_data['tweet']['in_reply_to_user_id']
                in_reply_to_user_tweet_details = next(
                    (one_tweet for one_tweet in tweet_data['mentions']['includes']['tweets'] if one_tweet['id'] == in_reply_to_tweet_id), None)
                if (in_reply_to_user_tweet_details):
                    if ('note_tweet' in in_reply_to_user_tweet_details):
                        in_reply_to_user_text = in_reply_to_user_tweet_details['note_tweet']['text']
                    else:
                        in_reply_to_user_text = in_reply_to_user_tweet_details['text']

                in_reply_to_user_text = remove_urls(text=in_reply_to_user_text)
                userdetails_who_posted = next(
                    (user for user in tweet_data['mentions']['includes']['users'] if user['id'] == in_reply_to_user_id), None)
                username_who_posted = None
                if (userdetails_who_posted):
                    username_who_posted = userdetails_who_posted['username']

                if (username_who_posted == 'nvctranslator' or '@nvctranslator' in in_reply_to_user_text):
                    logger.warning("Can't reply back to tweet")
                    return
                # check if tweet exist in database
                tweet_from_database = await get_tweet_by_id(
                    tweet_id=in_reply_to_tweet_id, db=db)
                if (tweet_from_database):
                    logger.info("Tweet already translated")
                    translated_text = tweet_from_database['translated_text'].split(
                        "<<>>")
                    tweets_to_reply = divide_into_tweets(
                        sentences=translated_text)
                    await reply_to_tweet(tweet_id=tweet_id, reply_text=tweets_to_reply, repy_tweet_id=in_reply_to_tweet_id)
                    return

                # Your code to get translated text
                tweets_to_reply, to_convert, converted = await nvctranslator(
                    full_text=str(in_reply_to_user_text), username_who_posted=username_who_posted)

                # code to reply to the tweet
                if (len(tweets_to_reply) == 0 or len(tweets_to_reply[0]) == 0 or tweets_to_reply == None):
                    logger.warning("No text recieved from NVC API")
                    return
                await reply_to_tweet(tweet_id=tweet_id, reply_text=tweets_to_reply, repy_tweet_id=in_reply_to_tweet_id)

                # code to store convert remaing text and store in database
                await handle_remaining_tweet_text(
                    to_convert=to_convert, converted=converted, db=db, tweet_id=in_reply_to_tweet_id)

            else:
                logger.warning('This tweet is not a reply')

        except Exception as e:
            logger.error(f"Error processing tweet {tweet_id}: {e}")


async def twitter_bot(db):
    """
    Main function to run the Twitter bot.
    """
    global last_processed_time
    try:
        logger.info("Twitter bot started")

        # Initialize Tweepy Client
        client = AsyncClient(bearer_token=env_vars['bearer_token'], return_type=dict,
                             wait_on_rate_limit=True)

        # Fetch mentions since the last processed tweet
        logger.info("Fetching latest mentions tweets")

        mentions = await client.get_users_mentions(
            id='1640149719447109633',
            start_time=get_last_processed_time(),
            tweet_fields=["created_at", "author_id", "note_tweet"],
            expansions=["in_reply_to_user_id", "referenced_tweets.id",
                        'author_id', 'edit_history_tweet_ids'],
            user_fields=["username"]
        )
        if 'data' in mentions:
            semaphore = asyncio.Semaphore(50)
            tasks = [asyncio.create_task(handle_each_tweet(
                tweet_data={'tweet': tweet, 'mentions': mentions}, index=index, semaphore=semaphore, db=db)) for index, tweet in enumerate(mentions['data'])]
            await asyncio.gather(*tasks)

        else:
            logger.warning('No mentions found')

    except Exception as e:
        logger.error(f"error in twitter bot function :-{e}")


async def main():
    db = await connect_to_mongodb()
    while 1:
        WAIT_TIME = 1.01  # min
        await asyncio.gather(twitter_bot(db=db), asyncio.sleep(WAIT_TIME*60))


if __name__ == "__main__":
    asyncio.run(main())
