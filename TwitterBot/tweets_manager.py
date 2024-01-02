from tweepy.asynchronous import AsyncClient
import os
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
import asyncio
from text_processing import get_text_from_GPT
from db_operations import insert_tweet, get_tweet_by_id
from text_processing import remove_urls
import re
from imagegenerator import create_image_with_text
import tweepy

load_dotenv()

last_processed_time = (datetime.utcnow() -
                       timedelta(seconds=11)).strftime('%Y-%m-%dT%H:%M:%SZ')
Tweepy_clients = {
    "@nvctranslator": AsyncClient(consumer_key=os.environ['NVC_CONSUMER_KEY'], consumer_secret=os.environ['NVC_CONSUMER_SECRET'], access_token=os.environ['NVC_ACCESS_TOKEN_KEY'], access_token_secret=os.environ['NVC_ACCESS_TOKEN_SECRET']),
    "@eli5translator": AsyncClient(consumer_key=os.environ['ELI5_CONSUMER_KEY'], consumer_secret=os.environ['ELI5_CONSUMER_SECRET'], access_token=os.environ['ELI5_ACCESS_TOKEN_KEY'], access_token_secret=os.environ['ELI5_ACCESS_TOKEN_SECRET']),
    "@adulttranslate": AsyncClient(consumer_key=os.environ['ADULT_CONSUMER_KEY'], consumer_secret=os.environ['ADULT_CONSUMER_SECRET'], access_token=os.environ['ADULT_ACCESS_TOKEN_KEY'], access_token_secret=os.environ['ADULT_ACCESS_TOKEN_SECRET']),
    "@makethismature": AsyncClient(consumer_key=os.environ['MATURE_CONSUMER_KEY'], consumer_secret=os.environ['MATURE_CONSUMER_SECRET'], access_token=os.environ['MATURE_ACCESS_TOKEN_KEY'], access_token_secret=os.environ['MATURE_ACCESS_TOKEN_SECRET'])
}

Tweepy_auth = {
    "@nvctranslator": tweepy.OAuth1UserHandler(consumer_key=os.environ['NVC_CONSUMER_KEY'], consumer_secret=os.environ['NVC_CONSUMER_SECRET'], access_token=os.environ['NVC_ACCESS_TOKEN_KEY'], access_token_secret=os.environ['NVC_ACCESS_TOKEN_SECRET']),
    "@eli5translator": tweepy.OAuth1UserHandler(consumer_key=os.environ['ELI5_CONSUMER_KEY'], consumer_secret=os.environ['ELI5_CONSUMER_SECRET'], access_token=os.environ['ELI5_ACCESS_TOKEN_KEY'], access_token_secret=os.environ['ELI5_ACCESS_TOKEN_SECRET']),
    "@adulttranslate": tweepy.OAuth1UserHandler(consumer_key=os.environ['ADULT_CONSUMER_KEY'], consumer_secret=os.environ['ADULT_CONSUMER_SECRET'], access_token=os.environ['ADULT_ACCESS_TOKEN_KEY'], access_token_secret=os.environ['ADULT_ACCESS_TOKEN_SECRET']),
    "@makethismature": tweepy.OAuth1UserHandler(consumer_key=os.environ['MATURE_CONSUMER_KEY'], consumer_secret=os.environ['MATURE_CONSUMER_SECRET'], access_token=os.environ['MATURE_ACCESS_TOKEN_KEY'], access_token_secret=os.environ['MATURE_ACCESS_TOKEN_SECRET'])
}

Bots_list = ["@nvctranslator", "@eli5translator",
             "@adulttranslate", "@makethismature"]


def get_intro_for_the_tweet(username: str, bot: str):
    """Get a introduction for the tweet"""
    match bot:
        case "@nvctranslator":
            intro = f"Here's a translation of @{username}’s message using Nonviolent Communication principles."
        case "@eli5translator":
            intro = f"Here is @{username}’s message explained like a 5-year-old would understand."
        case "@adulttranslate":
            intro = f"To align with adult communication norms, here is @{username}’s message conveyed in a more formal manner."
        case "@makethismature":
            intro = f"To elevate and refine the tone, here is @{username}’s message presented in mature language."
    return intro


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


def extract_mentions(text: list[str]):
    """
    Extracts mentions (usernames starting with "@") from a string
    """
    mentions = re.findall(r"@\w+", text)
    return mentions


async def reply_to_tweet(tweet_id: str, reply_text: str, bot: str, username: str):
    """
    Replies to a tweet with the given text.
    """
    try:
        client = Tweepy_clients[bot]
        auth = Tweepy_auth[bot]
        api = tweepy.API(auth)
        img_byte_arr = create_image_with_text(
            text=reply_text, bot=bot, username=username)
        media = api.media_upload(filename=tweet_id+".png", file=img_byte_arr)
        base_url = os.environ['HOST_URL'] + bot[1:]+'/'
        url_link = base_url+tweet_id
        await client.create_tweet(
            text=get_intro_for_the_tweet(username=username, bot=bot)+f"\n\nTo read the full text, please visit: {url_link}", in_reply_to_tweet_id=tweet_id, media_ids=[media.media_id])
        logging.info("Successfully replied to tweet")

    except Exception as e:
        logging.error(f"Error replying to tweet {tweet_id}: {e}")


async def handle_each_mention(bot: str, params: dict):
    """
    Handles the each mention or bot in tweet
    """
    # check if tweet exist in database
    tweet_from_database = await get_tweet_by_id(
        tweet_id=params['in_reply_to_tweet_id'], db=params['db'], bot=bot)
    if (tweet_from_database):
        logging.info("Tweet already translated")
        translated_text = " ".join(tweet_from_database['translated_text'].split(
            "<<>>"))
        await reply_to_tweet(tweet_id=params['tweet_id'], reply_text=translated_text, bot=bot, username=params['userdetails_who_posted']['username'])
        return

    # Your code to get translated text
    translated_text = await get_text_from_GPT(text=str(params['in_reply_to_user_text']), prompt_type=bot)
    # code to reply to the tweet
    if (len(translated_text) == 0 or translated_text == None):
        logging.warning("No text recieved from translator")
        return
    await reply_to_tweet(tweet_id=params['tweet_id'], reply_text=translated_text, bot=bot, username=params['userdetails_who_posted']['username'])

    # code to store translation,original and user details in database
    await insert_tweet(db=params['db'], tweet_id=params['tweet_id'], translated_text=translated_text, userdetails_who_posted=params['userdetails_who_posted'], bot=bot, original_text=params['in_reply_to_user_text'])


async def handle_each_tweet(semaphore: asyncio.Semaphore, tweet_data: dict, index: int, db):
    """
    Handles each tweet fetched from Twitter.
    """
    async with semaphore:
        try:

            # Get tweet details
            tweet_id = tweet_data['tweet']['id']
            tweet_created_at = tweet_data['tweet']['created_at']

            if ('note_tweet' in tweet_data['tweet']):
                tweet_text = tweet_data['tweet']['note_tweet']['text']
            else:
                tweet_text = tweet_data['tweet']['text']

            # Update the newest tweet time
            created_time = (datetime.strptime(
                tweet_created_at, '%Y-%m-%dT%H:%M:%S.%fZ')+timedelta(seconds=1)).strftime('%Y-%m-%dT%H:%M:%SZ')

            # Save the time of the most recent tweet processed
            if (index == 0):
                set_last_processed_time(created_time)

            # handle tweet with  latest_tweets
            in_reply_to_tweet_id = None
            if ('referenced_tweets' in tweet_data['tweet']):
                in_reply_to_tweet_id = next(
                    (ref_tweet['id'] for ref_tweet in tweet_data['tweet']['referenced_tweets'] if ref_tweet['type'] == 'replied_to'), None)

            if (in_reply_to_tweet_id):
                # Get user details
                in_reply_to_user_id = tweet_data['tweet']['in_reply_to_user_id']
                in_reply_to_user_tweet_details = next(
                    (one_tweet for one_tweet in tweet_data['latest_tweets']['includes']['tweets'] if one_tweet['id'] == in_reply_to_tweet_id), None)
                if (in_reply_to_user_tweet_details):
                    if ('note_tweet' in in_reply_to_user_tweet_details):
                        in_reply_to_user_text = in_reply_to_user_tweet_details['note_tweet']['text']
                    else:
                        in_reply_to_user_text = in_reply_to_user_tweet_details['text']

                in_reply_to_user_text = remove_urls(
                    text=in_reply_to_user_text)
                userdetails_who_posted = next(
                    (user for user in tweet_data['latest_tweets']['includes']['users'] if user['id'] == in_reply_to_user_id), None)

                if any(mention in set(extract_mentions(text=in_reply_to_user_text)) for mention in Bots_list):
                    logging.error("Can't reply back")
                    return
                tasks = []
                for mention in extract_mentions(text=tweet_text):
                    if (mention in Bots_list):
                        tasks.append(handle_each_mention(bot=mention, params={'in_reply_to_tweet_id': in_reply_to_tweet_id, 'db': db,
                                                                              'in_reply_to_user_text': in_reply_to_user_text, 'tweet_id': tweet_id, 'userdetails_who_posted': userdetails_who_posted}))
                await asyncio.gather(*tasks)
            else:
                logging.warning('This tweet is not a reply')

        except Exception as e:
            logging.error(f"Error processing tweet {tweet_id}: {e}")
