import motor.motor_asyncio
import os
import logging
from dotenv import load_dotenv
load_dotenv()

# database configuration details

mongo_url = os.getenv('MONGOURL')
DATABASE_NAMES = {"@nvctranslator": "nvctranslator",
                  "@eli5translator": "eli5translator",
                  "@adulttranslate": "adulttranslate"}
COLLECTION_NAME = "tweets"


async def connect_to_mongodb() -> motor.motor_asyncio.AsyncIOMotorDatabase:
    """
    Establishes a connection to the MongoDB database.
    """
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
        logging.info('Connected to MongoDB')
        return client
    except Exception as e:
        logging.error(f'Error while connecting to MongoDB: {e}')
        return None


async def get_tweet_by_id(db, tweet_id: str, mention: str):
    """
    Retrieves a tweet by its ID from the database.
    """
    try:
        tweet = await db[DATABASE_NAMES[mention]][COLLECTION_NAME].find_one({"tweet_id": tweet_id})
        logging.info(f'Successfully retrieved tweet with id: {tweet_id}')
        return tweet
    except Exception as e:
        logging.error(f'Error retrieving tweet: {e}')
        return None


async def insert_tweet(db, tweet_id: str, sentences: list, mention: str, userdetails_who_posted: dict, original_text: str):
    """
    Inserts a tweet into the database.
    """
    try:
        tweet_data = {"translated_text": "<<>>".join(
            sentences), "original_text": original_text, "tweet_id": tweet_id, "userdetails_who_posted": userdetails_who_posted}
        await db[DATABASE_NAMES[mention]][COLLECTION_NAME].insert_one(tweet_data)
        logging.info(f'Successfully inserted tweet with id: {tweet_id}')
    except Exception as e:
        logging.error(f'Error inserting tweet: {e}')
