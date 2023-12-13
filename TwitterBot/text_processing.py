import re
import nltk
from openai import AsyncOpenAI
import os
import logging
from dotenv import load_dotenv

load_dotenv()

OPENAI_CLIENT = AsyncOpenAI(api_key=os.getenv('OPENAI'))

# prompts

prompts = {
    "@nvctranslator": "Translate into simple Nonviolent Communication (NVC) language ",
    "@eli5translator": "Explain Like I'm 5 year old",
    "@adulttranslate": "Tailor the text to sound more 'adult-like', perhaps by refining slang or casual language into simple formal English",
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


def create_sentences(text: str) -> list:
    """
    Splits the given text into sentences.
    """
    sentences = []
    for batch in text.split('\n'):
        sentences.extend(nltk.sent_tokenize(batch))
        sentences.append('\n')
    return sentences[:-1]


async def get_text_from_GPT(text: str, prompt_type: str) -> str:
    """
    Retrieves text rephrased using GPT from OpenAI.
    """
    if (text == '\n' or text == " " or text == "" or len(text) < 5 or remove_mentions_hashtags(text) == ""):
        return text
    try:
        prompt = f"""
        {prompts[prompt_type]}and keep the output short and precise as possible:-\n
        Original Text:
        "{text}"
        """
        response = await OPENAI_CLIENT.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": prompt
            }],
            temperature=0.1
        )
        return response.choices[0].message.content.replace('"', '')
    except Exception as e:
        logging.error(f'Error in GPT processing: {e}')
        return ""
