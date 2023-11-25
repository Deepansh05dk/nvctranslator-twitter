from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv
from tweepy.asynchronous import AsyncClient
import re
import motor.motor_asyncio
import logging

load_dotenv()

# Create a logger
logger = logging.getLogger(__name__)
logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s]   %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    force=True)

# fastapi app configurations
app = FastAPI()
app.mount("/static", StaticFiles(directory="Website/static"), name="static")
templates = Jinja2Templates(directory='Website/templates')

# Twitter API credentials
bearer_token = os.environ['BEARER_TOKEN']

# twitter client
twitter_client = AsyncClient(bearer_token=bearer_token)


# database handling
mongo_uri = os.environ['MONGOURL']
DATABASE_NAME = "nvctranslator"
COLLECTION_NAME = "tweets"
client = motor.motor_asyncio.AsyncIOMotorClient(
    mongo_uri)  # Initialize MongoDB client
db = client[DATABASE_NAME]

# Precompiled regex pattern for URL removal
url_pattern = re.compile(r'https?://\S+|www\.\S+')


async def connect_to_mongodb():
    """Connect to the MongoDB server."""
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
        logging.info('Connected to MongoDB')
        return client[DATABASE_NAME]
    except Exception as e:
        logging.error(f'Error while connecting to MongoDB: {e}')
        return None


async def get_tweet_by_id(db, tweet_id):
    """ Get tweet from database"""
    try:
        tweet = await db[COLLECTION_NAME].find_one({"tweet_id": tweet_id})
        logging.info(f'Successfully retrieved tweet with id: {tweet_id}')
        return tweet
    except Exception as e:
        logging.error(
            f'Error while retrieving tweet with id: {tweet_id}, Error: {e}')
        return None


def remove_urls(text: str):
    """Remove URLs from the given text"""
    return re.sub(url_pattern, '', text)


async def get_tweet_details(status_id: str):
    """Extract tweet details"""
    try:
        status = await twitter_client.get_tweet(
            id=status_id,
            expansions=['author_id'],
            user_fields=['username', 'name', 'profile_image_url'],
            tweet_fields=['text', 'note_tweet'],
        )
        if ('note_tweet' in status[0]):
            return {'user': status[1]['users'][0], 'text': remove_urls(status[0]['note_tweet']['text'])}
        else:
            return {'user': status[1]['users'][0], 'text': remove_urls(status[0]['text'])}
    except Exception as e:
        print("Error getting tweet details: ", e)
        return None


@app.get("/", response_class=RedirectResponse)
async def read_root():
    return RedirectResponse(url='https://nvcthis.com/')


@app.get("/{status_id}", response_class=HTMLResponse)
async def read_item(request: Request, status_id: str):
    if db != None:
        tweet_from_database = await get_tweet_by_id(
            tweet_id=status_id, db=db)
        if (tweet_from_database == None):
            return templates.TemplateResponse("not_found.html", {"request": request})
        result = await get_tweet_details(status_id=status_id)
        translated_text = " ".join(
            tweet_from_database['translated_text'].split("<<>>"))
        return templates.TemplateResponse("index.html", {"request": request, "tweet": result, "translated_text": translated_text})
    else:
        return templates.TemplateResponse("not_found.html", {"request": request})
