from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import textwrap


Bot_resultimage_details = {
    "nvctranslator": {
        "text_position": (900, 510),
        "username_font_colour": "#f59e0b",
        "max_chars_per_line": 32
    },
    "adulttranslate": {
        "text_position": (420, 250),
        "username_font_colour": "#000080",
        "max_chars_per_line": 38

    },
    "eli5translator": {
        "text_position": (320, 200),
        "username_font_colour": "#008080",
        "max_chars_per_line": 46

    },
    "makethismature": {
        "text_position": (380, 480),
        "username_font_colour": "#573c27",
        "max_chars_per_line": 40

    },
}


def draw_text(draw, text: str, position: list, font, image_width: int, line_spacing: int, bot: str, username: str):
    """
    Draw text within an image with wrapping and appropriate line spacing.
    """
    text = text.replace("\n", "")
    if (len(text) > 305):
        text = text[:306]+"..."

    # Calculate how many characters can fit in a line given the image width
    max_chars_per_line = Bot_resultimage_details[bot]["max_chars_per_line"]

    # Wrap the text
    wrapped_text = textwrap.wrap(text, width=max_chars_per_line)

    # Draw the text
    y_text = position[1]
    for line in wrapped_text:
        # Calculate the width of the line of text and the full height with line spacing
        line_width = draw.textbbox((0, 0), line, font=font)[2]

        # If the text width is greater than the image width, reduce the number of characters per line
        if line_width > image_width:
            wrapped_text = textwrap.wrap(text, width=max_chars_per_line - 1)
            line_width = draw.textbbox((0, 0), line, font=font)[2]

        # Draw the line of text
        draw.text((position[0], y_text), line,
                  font=font, fill="rgb( 36, 36, 36)")
        # Increment y position for the next line
        y_text += line_spacing

    username_width = draw.textbbox(
        (0, 0), username, font=ImageFont.truetype("TwitterBot/fonts/Raleway-ExtraBoldItalic.ttf", 65))[2]

    draw.text(((image_width-position[0]-username_width) /
              2+position[0], y_text+50), "- "+username, font=ImageFont.truetype("TwitterBot/fonts/Raleway-ExtraBoldItalic.ttf", 65), fill=Bot_resultimage_details[bot]['username_font_colour'])


def create_image_with_text(text: str, bot: str, username: str):
    """ Create text on image """
    image_path = "TwitterBot/image_templates/"+bot+".png"
    with Image.open(image_path) as base:
        # Create a drawing context
        draw = ImageDraw.Draw(base)

        # Define the font and size
        font_path = "TwitterBot/fonts/Raleway-Bold.ttf"
        font_size = 70  # Choose an appropriate font size
        font = ImageFont.truetype(font_path, font_size)

        # Position for the  quote text
        text_position = Bot_resultimage_details[bot]['text_position']

        # Draw the quote text
        draw_text(
            draw, text, text_position, font, base.width, 95, bot, username)

        # Convert to Bytes
        img_byte_arr = BytesIO()
        base.save(img_byte_arr, format='PNG')  # Adjust format as needed
        img_byte_arr.seek(0)  # Move to the start of the bytes stream
        # return the result
        return img_byte_arr
