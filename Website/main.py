from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv
import re
import motor.motor_asyncio
import logging

load_dotenv()
# fastapi app configurations
app = FastAPI()
app.mount("/static", StaticFiles(directory="./static"), name="static")
templates = Jinja2Templates(directory='./templates')


# functionalities related to database
mongo_uri = os.environ['MONGOURL']
COLLECTION_NAME = "tweets"
client = motor.motor_asyncio.AsyncIOMotorClient(
    mongo_uri)  # Initialize MongoDB client
db = client

# Precompiled regex pattern for URL removal
url_pattern = re.compile(r'https?://\S+|www\.\S+')


async def get_tweet_by_id(db, tweet_id: str, database: str):
    try:
        tweet = await db[database][COLLECTION_NAME].find_one({"tweet_id": tweet_id})
        logging.info(f'Successfully retrieved tweet with id: {tweet_id}')
        return tweet
    except Exception as e:
        logging.error(
            f'Error while retrieving tweet with id: {tweet_id}, Error: {e}')
        return None


def remove_urls(text: str):
    # Regex pattern to match URLs
    return re.sub(url_pattern, '', text)


@app.get("/nvctranslator/{status_id}", response_class=HTMLResponse)
async def read_item(request: Request, status_id: str):
    if db != None:
        tweet_from_database = await get_tweet_by_id(
            tweet_id=status_id, db=db, database='nvctranslator')
        if (tweet_from_database == None):
            return templates.TemplateResponse("not_found.html", {"request": request, "theme_colour": "#fbbf24", "bot": 'NVCTranslator', "logo": "../static/logos/nvctranslator.jpg", "mention": "nvctranslator"})
        translated_text = " ".join(
            tweet_from_database['translated_text'].split("<<>>"))
        original_text = tweet_from_database['original_text']
        user_details = tweet_from_database['userdetails_who_posted']
        return templates.TemplateResponse("index.html", {"request": request, "original_text": original_text, "translated_text": translated_text, "user_details": user_details, "theme_colour": "#fbbf24", "bot": 'NVCTranslator', "logo": "../static/logos/nvctranslator.jpg", "mention": "nvctranslator"})
    else:
        return templates.TemplateResponse("not_found.html", {"request": request})


@app.get("/eli5translator/{status_id}", response_class=HTMLResponse)
async def read_item(request: Request, status_id: str):
    if db != None:
        tweet_from_database = await get_tweet_by_id(
            tweet_id=status_id, db=db, database='eli5translator')
        if (tweet_from_database == None):
            return templates.TemplateResponse("not_found.html", {"request": request, "theme_colour": "#68baa2", "bot": 'ELI5Translator', "logo": "../static/logos/eli5translator.png", "mention": "eli5translator"})
        translated_text = " ".join(
            tweet_from_database['translated_text'].split("<<>>"))
        original_text = tweet_from_database['original_text']
        user_details = tweet_from_database['userdetails_who_posted']
        return templates.TemplateResponse("index.html", {"request": request, "original_text": original_text, "translated_text": translated_text, "user_details": user_details, "theme_colour": "#68baa2", "bot": 'ELI5Translator', "logo": "../static/logos/eli5translator.png", "mention": "eli5translator"})
    else:
        return templates.TemplateResponse("not_found.html", {"request": request})


@app.get("/adulttranslate/{status_id}", response_class=HTMLResponse)
async def read_item(request: Request, status_id: str):
    if db != None:
        tweet_from_database = await get_tweet_by_id(
            tweet_id=status_id, db=db, database='adulttranslate')
        if (tweet_from_database == None):
            return templates.TemplateResponse("not_found.html", {"request": request, "theme_colour": "#29558d", "bot": 'AdultTranslator', "logo": "../static/logos/adulttranslate.png", "mention": "adulttranslate"})
        translated_text = " ".join(
            tweet_from_database['translated_text'].split("<<>>"))
        original_text = tweet_from_database['original_text']
        user_details = tweet_from_database['userdetails_who_posted']
        return templates.TemplateResponse("index.html", {"request": request, "original_text": original_text, "translated_text": translated_text, "user_details": user_details, "theme_colour": "#29558d", "bot": 'AdultTranslator', "logo": "../static/logos/adulttranslate.png", "mention": "adulttranslate"})
    else:
        return templates.TemplateResponse("not_found.html", {"request": request})


@app.get("/makethismature/{status_id}", response_class=HTMLResponse)
async def read_item(request: Request, status_id: str):
    if db != None:
        tweet_from_database = await get_tweet_by_id(
            tweet_id=status_id, db=db, database='makethismature')
        if (tweet_from_database == None):
            return templates.TemplateResponse("not_found.html", {"request": request, "theme_colour": "#ab551f", "bot": 'MakeThisMature', "logo": "../static/logos/makethismature.png", "mention": "makethismature"})
        translated_text = " ".join(
            tweet_from_database['translated_text'].split("<<>>"))
        original_text = tweet_from_database['original_text']
        user_details = tweet_from_database['userdetails_who_posted']
        return templates.TemplateResponse("index.html", {"request": request, "original_text": original_text, "translated_text": translated_text, "user_details": user_details, "theme_colour": "#ab551f", "bot": 'MakeThisMature', "logo": "../static/logos/makethismature.png", "mention": "makethismature"})
    else:
        return templates.TemplateResponse("not_found.html", {"request": request})
