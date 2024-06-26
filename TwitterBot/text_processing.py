import re
from openai import AsyncOpenAI
import os
import logging
from dotenv import load_dotenv

load_dotenv()

OPENAI_CLIENT = AsyncOpenAI(api_key=os.getenv('OPENAI'))

# prompts

prompts = {
    "@nvctranslator": "Translate the following text into simple nvc language:-",
    "@eli5translator": "Write the content using simple same language as input like you’re explaining something to a 5-year-old. If you belief it can't be explained then you should say 'I'm sorry i can't explain it' with some emojis,and please don't make any friction story around it. Make sure answer should be of optimal lenght so that user don't find it too long to read.",
    "@woketranslate": "become woke translator that can rephrase statements to be more inclusive, socially aware, and sensitive to issues of race, gender, class, and other forms of social inequality. This translator should be able to recognize potentially insensitive or uninformed language and offer alternatives that are more aligned with progressive values and social justice principles. It should be able to handle a wide range of topics, from everyday conversation to more complex subjects like politics, history, and culture. The translator should prioritize language that is respectful, inclusive, and considerate of diverse perspectives and experiences.",
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
                "content": f"You're an online bot on Twitter that aims to follow the platform's guidelines while prioritizing the delivery of results without causing offense to anyone.You are provided with a text of tweet, and your task is to {prompts[prompt_type]}"
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
