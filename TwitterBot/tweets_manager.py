from tweepy.asynchronous import AsyncClient
import os
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
import asyncio
import nltk
from text_processing import get_text_from_GPT
from db_operations import insert_tweet, get_tweet_by_id
from text_processing import create_sentences, remove_urls
import re

load_dotenv()

last_processed_time = (datetime.utcnow() -
                       timedelta(seconds=11)).strftime('%Y-%m-%dT%H:%M:%SZ')
Tweepy_clients = {
    "@nvctranslator": AsyncClient(consumer_key=os.environ['NVC_CONSUMER_KEY'], consumer_secret=os.environ['NVC_CONSUMER_SECRET'], access_token=os.environ['NVC_ACCESS_TOKEN_KEY'], access_token_secret=os.environ['NVC_ACCESS_TOKEN_SECRET']),
    "@eli5translator": AsyncClient(consumer_key=os.environ['ELI5_CONSUMER_KEY'], consumer_secret=os.environ['ELI5_CONSUMER_SECRET'], access_token=os.environ['ELI5_ACCESS_TOKEN_KEY'], access_token_secret=os.environ['ELI5_ACCESS_TOKEN_SECRET']),
    "@adulttranslate": AsyncClient(consumer_key=os.environ['ADULT_CONSUMER_KEY'], consumer_secret=os.environ['ADULT_CONSUMER_SECRET'], access_token=os.environ['ADULT_ACCESS_TOKEN_KEY'], access_token_secret=os.environ['ADULT_ACCESS_TOKEN_SECRET']),
    "@makethismature": AsyncClient(consumer_key=os.environ['MATURE_CONSUMER_KEY'], consumer_secret=os.environ['MATURE_CONSUMER_SECRET'], access_token=os.environ['MATURE_ACCESS_TOKEN_KEY'], access_token_secret=os.environ['MATURE_ACCESS_TOKEN_SECRET'])
}

Bots_list = ["@nvctranslator", "@eli5translator",
             "@adulttranslate", "@makethismature"]


def get_intro_for_the_tweet(username: str, mention: str):
    """Get a introduction for the tweet"""
    match mention:
        case "@nvctranslator":
            intro = f"Here's a translation of @{username}’s message using Nonviolent Communication principles:"
        case "@eli5translator":
            intro = f"Here is @{username}’s message explained like a 5-year-old would understand:"
        case "@adulttranslate":
            intro = f"To align with adult communication norms, here is @{username}’s message conveyed in a more formal manner:"
        case "@makethismature":
            intro = f"To elevate and refine the tone, here is @{username}’s message presented in mature language:"
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


def divide_into_tweets(sentences: list, username_who_posted: str, mention: str, tweet_id: str, max_length: int = 275, max_tweets: int = 2) -> list:
    """
    Divides a list of text into tweets, each not exceeding the max_length.
    """
    tweets = []
    current_tweet = get_intro_for_the_tweet(
        mention=mention, username=username_who_posted)+"\n\n"
    for sentence in sentences:
        if len(current_tweet) + len(sentence) + 1 <= max_length:
            current_tweet += " " + \
                sentence if (current_tweet and not current_tweet.endswith(
                    "\n") and sentence != '\n') else sentence
        else:
            words = nltk.word_tokenize(sentence)
            for word in words:
                if len(current_tweet) + len(word) + 1 <= max_length:
                    current_tweet += " " + \
                        word if (current_tweet and not current_tweet.endswith(
                            "\n") and word != '\n') else word
                else:
                    tweets.append(current_tweet)
                    current_tweet = word
                    if len(tweets) == max_tweets:
                        return tweets

        if len(tweets) == max_tweets:
            break

    if current_tweet and len(tweets) < max_tweets:
        tweets.append(current_tweet)

    if (len(tweets) == 2):
        tweets[0] = ' 1/3 ' + tweets[0]
        tweets[1] = ' 2/3 ' + tweets[1]
        base_url = os.environ['HOST_URL'] + mention[1:]+'/'
        url_link = base_url+tweet_id
        tweets.append(
            f"3/3 Complete text available at {url_link}"
        )

    return tweets


async def translator(full_text: str, username_who_posted: str, mention: str, tweet_id: str) -> tuple:
    """
    Translates the provided text using GPT and divides it into tweets.
    """
    sentences = create_sentences(text=full_text)
    tasks = [
        asyncio.create_task(get_text_from_GPT(
            text=sentence, prompt_type=mention))
        for sentence in sentences[:20]
    ]
    results = await asyncio.gather(*tasks)
    tweets = divide_into_tweets(
        sentences=results, username_who_posted=username_who_posted, mention=mention, tweet_id=tweet_id)
    return (tweets, sentences[20:], results)


async def reply_to_tweet(tweet_id: str, reply_text: list[str], client_type: str):
    """
    Replies to a tweet with the given text.
    """
    try:
        client = Tweepy_clients[client_type]
        tweet_id_to_reply = tweet_id
        for i in range(0, len(reply_text)):
            tweet_reply_text = reply_text[i]
            status = await client.create_tweet(
                text=str(tweet_reply_text), in_reply_to_tweet_id=tweet_id_to_reply)
            tweet_id_to_reply = status[0]['id']

        logging.info("Successfully replied to tweet")

    except Exception as e:

        logging.error(f"Error replying to tweet {tweet_id}: {e}")


async def handle_remaining_tweet_text(to_convert: list, converted: list, db, tweet_id: str, mention: str, userdetails_who_posted: dict, original_text: str):
    """
    Handles the remaining text for conversion and inserts into the database.
    """
    all_converted_text = converted + await asyncio.gather(
        *[asyncio.create_task(get_text_from_GPT(text, prompt_type=mention)) for text in to_convert]
    )
    await insert_tweet(db, tweet_id, all_converted_text, userdetails_who_posted=userdetails_who_posted, mention=mention, original_text=original_text)


async def handle_each_mention(mention: str, params: dict):
    """
    Handles the each mention or bot in tweet
    """
    # check if tweet exist in database
    tweet_from_database = await get_tweet_by_id(
        tweet_id=params['in_reply_to_tweet_id'], db=params['db'], mention=mention)
    if (tweet_from_database):
        logging.info("Tweet already translated")
        translated_text = tweet_from_database['translated_text'].split(
            "<<>>")
        tweets_to_reply = divide_into_tweets(
            sentences=translated_text, username_who_posted=params['userdetails_who_posted']['username'], mention=mention, tweet_id=params['in_reply_to_tweet_id'])
        await reply_to_tweet(tweet_id=params['tweet_id'], reply_text=tweets_to_reply, client_type=mention)
        return

    # Your code to get translated text
    tweets_to_reply, to_convert, converted = await translator(
        full_text=str(params['in_reply_to_user_text']), username_who_posted=params['userdetails_who_posted']['username'], mention=mention, tweet_id=params['in_reply_to_tweet_id'])

    # code to reply to the tweet
    if (len(tweets_to_reply) == 0 or len(tweets_to_reply[0]) == 0 or tweets_to_reply == None):
        logging.warning("No text recieved from translator")
        return
    await reply_to_tweet(tweet_id=params['tweet_id'], reply_text=tweets_to_reply, client_type=mention)

    # code to store convert remaing text and store in database
    await handle_remaining_tweet_text(
        to_convert=to_convert, converted=converted, db=params['db'], tweet_id=params['in_reply_to_tweet_id'], mention=mention, userdetails_who_posted=params['userdetails_who_posted'], original_text=params['in_reply_to_user_text'])


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
                        tasks.append(handle_each_mention(mention=mention, params={'in_reply_to_tweet_id': in_reply_to_tweet_id, 'db': db,
                                                                                  'in_reply_to_user_text': in_reply_to_user_text, 'tweet_id': tweet_id, 'userdetails_who_posted': userdetails_who_posted}))
                await asyncio.gather(*tasks)
            else:
                logging.warning('This tweet is not a reply')

        except Exception as e:
            logging.error(f"Error processing tweet {tweet_id}: {e}")
