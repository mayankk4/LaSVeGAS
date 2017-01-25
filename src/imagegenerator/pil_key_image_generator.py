''' Generates png (lossless) outputs for short input text.

References:
Image Module
https://pillow.readthedocs.io/en/3.4.x/reference/Image.html
ImageDraw Module
https://pillow.readthedocs.io/en/3.4.x/reference/ImageDraw.html
ImageFont
https://pillow.readthedocs.io/en/3.4.x/reference/ImageFont.html

Notes:
Consider using jpg to reduce the size of the outputs if needed.

'''

# TODO: Take a proper KV pair as input and generate all the necessary images
# TODO: Add flags support.
# TODO: Give a slight gradiant in the background image.

import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

import textwrap

MAX_W, MAX_H = 1920, 1080

SHADOW_COLOR = "black"
TEXT_COLOR = "white"

# TODO: Decide font size based on the key size.
FONT_SIZE = 250
SHADOW_WIDTH = 2


def GenerateImage(text, output_path, bgcolor):
    print "Generating Image for the key: " + text
    # Create an image with a bg colour.
    img = Image.new("RGBA", (MAX_W, MAX_H), bgcolor)
    draw = ImageDraw.Draw(img)

    # TODO: Store the font file locally
    font = ImageFont.truetype("Georgia.ttf", FONT_SIZE)

    # A sample text addition
    # .text((10,10), "Empressite", fill=None, font=font, anchor=None, spacing=0, align="center")

    # Get coordinates for drawing text
    w, h = draw.textsize(text, font=font)
    x = (MAX_W - w) / 2
    y = (MAX_H - h) / 2

    # Now add text to the image.
    # Adding shadows first.
    draw.text((x - SHADOW_WIDTH, y), text, font=font, fill=SHADOW_COLOR)
    draw.text((x + SHADOW_WIDTH, y), text, font=font, fill=SHADOW_COLOR)
    draw.text((x, y - SHADOW_WIDTH), text, font=font, fill=SHADOW_COLOR)
    draw.text((x, y + SHADOW_WIDTH), text, font=font, fill=SHADOW_COLOR)

    # Adding text in white.
    draw.text((x, y), text, fill=TEXT_COLOR, font=font)

    # img.save("key.png")
    img.save(output_path)
