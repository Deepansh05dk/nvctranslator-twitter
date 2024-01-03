from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import textwrap
import re
import logging


Bot_resultimage_details = {
    "@nvctranslator": {
        "text_position_x": 900,
        "username_font_colour": "#f59e0b",
        "max_chars_per_line": 35,
        "ymin_allowed": 420,
        "ymax_allowed": 1700,
        "max_text_lenght_allowed": 350
    },
    "@woketranslate": {
        "text_position_x": 380,
        "username_font_colour": "#000080",
        "max_chars_per_line": 45,
        "ymin_allowed": 100,
        "ymax_allowed": 1600,
        "max_text_lenght_allowed": 440

    },
    "@eli5translator": {
        "text_position_x": 260,
        "username_font_colour": "#008080",
        "max_chars_per_line": 56,
        "ymin_allowed": 80,
        "ymax_allowed": 1100,
        "max_text_lenght_allowed": 470

    },
    "@makethismature": {
        "text_position_x": 330,
        "username_font_colour": "#573c27",
        "max_chars_per_line": 46,
        "ymin_allowed": 300,
        "ymax_allowed": 1520,
        "max_text_lenght_allowed": 420
    },

}


def draw_text(draw, text: str, font, image_width: int, line_spacing: int, bot: str, username: str):
    """
    Draw text within an image with wrapping and appropriate line spacing.
    """
    text = text.replace("\n", "")
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    if (len(text) > Bot_resultimage_details[bot]['max_text_lenght_allowed']):
        text = text[:Bot_resultimage_details[bot]
                    ['max_text_lenght_allowed']+1]+"..."

    # Calculate how many characters can fit in a line given the image width
    max_chars_per_line = Bot_resultimage_details[bot]["max_chars_per_line"]

    # Wrap the text
    wrapped_text = textwrap.wrap(text, width=max_chars_per_line)
    text_height = (2*len(wrapped_text)-1)*50

    # Calculate the starting y position to center the text vertically
    y_min = Bot_resultimage_details[bot]['ymin_allowed']
    y_max = Bot_resultimage_details[bot]['ymax_allowed']
    allowed_height = y_max - y_min
    start_y = (allowed_height - text_height) / 2 + y_min

    # Draw the text
    y_text = start_y
    for line in wrapped_text:
        # Calculate the width of the line of text and the full height with line spacing
        line_width = draw.textbbox((0, 0), line, font=font)[2]

        # If the text width is greater than the image width, reduce the number of characters per line
        if line_width > image_width:
            wrapped_text = textwrap.wrap(text, width=max_chars_per_line - 1)
            line_width = draw.textbbox((0, 0), line, font=font)[2]

        # Draw the line of text
        draw.text((Bot_resultimage_details[bot]['text_position_x'], y_text), line,
                  font=font, fill="rgb( 36, 36, 36)")
        # Increment y position for the next line
        y_text += line_spacing

    username_width = draw.textbbox(
        (0, 0), username, font=ImageFont.truetype("TwitterBot/fonts/Raleway-ExtraBoldItalic.ttf", 65))[2]

    draw.text(((image_width-Bot_resultimage_details[bot]['text_position_x']-username_width) /
              2+Bot_resultimage_details[bot]['text_position_x'], y_text+40), "- "+username, font=ImageFont.truetype("TwitterBot/fonts/Raleway-ExtraBoldItalic.ttf", 65), fill=Bot_resultimage_details[bot]['username_font_colour'])


def create_image_with_text(text: str, bot: str, username: str):
    """ Create text on image """

    try:
        image_path = "TwitterBot/image_templates/"+bot[1:]+".png"
        with Image.open(image_path) as base:
            # Create a drawing context
            draw = ImageDraw.Draw(base)

            # Define the font and size
            font_path = "TwitterBot/fonts/Raleway-Bold.ttf"
            font_size = 62  # Choose an appropriate font size
            font = ImageFont.truetype(font_path, font_size)

            # Draw the quote text
            draw_text(
                draw, text, font, base.width, 90, bot, username)

            # Convert to Bytes
            img_byte_arr = BytesIO()
            base.save(img_byte_arr, format='PNG')  # Adjust format as needed
            img_byte_arr.seek(0)  # Move to the start of the bytes stream
            # return the result
            return img_byte_arr

    except Exception as e:
        logging.error(f"Error in creating image : {e}")
