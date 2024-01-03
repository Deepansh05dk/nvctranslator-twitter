import re
from openai import AsyncOpenAI
import os
import logging
from dotenv import load_dotenv

load_dotenv()

OPENAI_CLIENT = AsyncOpenAI(api_key=os.getenv('OPENAI'))

# prompts

prompts = {
    "@nvctranslator": "Translate into simple Nonviolent Communication (NVC) language ",
    "@eli5translator": "Explain like I am five year old",
    "@woketranslate": "Translate into simple woke language",
    "@makethismature": "Converts immature or simplistic language in text into a more sophisticated and mature form, perhaps for professional or academic use"
}


def remove_urls(text: str):
    """
    Remove the urls and hastags from the given text.
    """
    # Remove URLs
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    text = re.sub(url_pattern, '', text)

    return text


def remove_mentions_hashtags(text: str):
    """
    Remove mentions, and hashtags from the given text.
    """

    # Remove mentions (usernames)
    mention_pattern = re.compile(r'@[\w]+')
    text = re.sub(mention_pattern, '', text)

    # Remove hashtags
    hashtag_pattern = re.compile(r'#\w+')
    text = re.sub(hashtag_pattern, '', text)

    return text.strip()


async def get_text_from_GPT(text: str, prompt_type: str) -> str:
    """
    Retrieves text rephrased using GPT from OpenAI.
    """
    if (text == '\n' or text == " " or text == "" or len(text) < 5 or remove_mentions_hashtags(text) == ""):
        return text
    try:
        response = await OPENAI_CLIENT.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": f"You are AI twitter bot .You will be provided with a tweet, and your task is to {prompts[prompt_type]}"
            }, {
                "role": "user",
                "content": text
            }],
            temperature=0.1
        )
        return response.choices[0].message.content.replace('"', '')
    except Exception as e:
        logging.error(f'Error in GPT processing: {e}')
        return ""
