''' Generates png (lossless) outputs for paragraphs.

References:
Image Module
https://pillow.readthedocs.io/en/3.4.x/reference/Image.html
ImageDraw Module
https://pillow.readthedocs.io/en/3.4.x/reference/ImageDraw.html
ImageFont
https://pillow.readthedocs.io/en/3.4.x/reference/ImageFont.html

'''

# TODO: Add support for splitting values over multiple images. Otherwise
#      we need to add a character limit for the value.


import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

import textwrap

MAX_W, MAX_H = 1920, 1080
TEXT_COLOR = "black"

# TODO: Decide fontsize based on the number of characters.
FONT_SIZE = 80
CHARACTERS_PER_LINE = 40

def GenerateImage(text, output_path, bgcolor):
    print "Generating Image for the value: " + text

    # Create an image with a bg colour.
    img = Image.new("RGBA", (MAX_W, MAX_H), bgcolor)
    draw = ImageDraw.Draw(img)

    # Now add text to the image.
    # Convert to paragraph.
    para = textwrap.wrap(text, width=CHARACTERS_PER_LINE)

    font = ImageFont.truetype("Georgia.ttf", FONT_SIZE)  # fontsize

    # Determining the height at which we want to start the text.
    w_first, h_first = draw.textsize(para[0], font=font)
    current_h = (MAX_H / 2) - ((len(para) / 2) * h_first)

    pad = 10
    for line in para:
        w, h = draw.textsize(line, font=font)
        x = (MAX_W - w) / 2
        y = current_h

        # Add test
        draw.text((x, y), line, fill=TEXT_COLOR, font=font)

        current_h += h + pad

    img.save(output_path)
