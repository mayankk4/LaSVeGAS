''' Util which helps us decide the background colours for our videos.

- Take a list of input RGB color codes through a text file.
- Generates two images per colour - one with white text and one with dark text.

The image titles contain the rgb colour code so that we can quickly add or
remove a color if needed.

Usage:
python bgcolor_tester.py


'''

import PIL
import textwrap
import subprocess

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

FONT_SIZE = 250
SHADOW_WIDTH = 2
MAX_W, MAX_H = 2880, 1800
SHADOW_COLOR = "black"

INPUT_KEY = '''Empressite'''
INPUT_VALUE = '''Empressite is a mineral form of silver telluride, AgTe. It is
 rare, grey, orthorhombic mineral with which can form compact masses, rarely
 as bipyrimidal crystals.'''


def GenerateKeyImage(text, output_path, bgcolor):
    TEXT_COLOR = "white"

    img = Image.new('RGB', imgsize, bgcolor)
    draw = ImageDraw.Draw(img)

    # TODO: Store the font file locally
    font = ImageFont.truetype("Georgia.ttf", FONT_SIZE)

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

    img.save(output_path)


def GenerateValueImage(text, output_path, bgcolor):
    TEXT_COLOR = "black"

    img = Image.new('RGB', imgsize, bgcolor)
    draw = ImageDraw.Draw(img)

    # Now add text to the image.
    # Convert to paragraph.
    para = textwrap.wrap(text, width=40)  # width = number of characters.

    font = ImageFont.truetype("Georgia.ttf", 100)  # fontsize

    # Determining the height at which we want to start the text.
    w_first, h_first = draw.textsize(para[0], font=font)
    current_h = (MAX_H / 2) - ((len(para) / 2) * h_first)

    pad = 10
    for line in para:
        w, h = draw.textsize(line, font=font)
        x = (MAX_W - w) / 2
        y = current_h

        # Add text
        draw.text((x, y), line, fill=TEXT_COLOR, font=font)

        current_h += h + pad

    img.save(output_path)


if __name__ == '__main__':
    print "Starting..."

    subprocess.call("rm -r ./output/", shell=True)
    subprocess.call("mkdir ./output/", shell=True)

    print "Reading the color code text file."
    lines = []
    with open("./modern_colors.txt") as f:
        for line in f:
            lines.append(line)

    print "Read completed."

    i = 0
    for line in lines:
        i = i + 1
        if (not line.startswith('rgb')):
            print "continue " + str(i)
            continue

        # Read the RGB color code as a tuple
        current_color = tuple(
            map(int, line.split('(')[1].split(')')[0].split(',')))

        key_output_path = "./output/" + str(i) + "_key.png"
        value_output_path = "./output/" + str(i) + "_value.png"

        GenerateKeyImage(INPUT_KEY, key_output_path, current_color)
        GenerateValueImage(INPUT_VALUE, value_output_path, current_color)
        print "generating " + str(i)
