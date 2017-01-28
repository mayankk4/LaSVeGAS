''' Util which helps us decide the background colours for our videos.
This script takes a lot longer to run than bgcolor_tester.py since it also
adds gradient to each image.

Usage:
python bgcolor_gradient_tester.py

'''

import PIL
import textwrap
import subprocess
import math

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from random import randint


FONT_SIZE = 250
SHADOW_WIDTH = 2
MAX_W, MAX_H = 2880, 1800
SHADOW_COLOR = "black"

INPUT_KEY = '''Empressite'''
INPUT_VALUE = '''Empressite is a mineral form of silver telluride, AgTe. It is
 rare, grey, orthorhombic mineral with which can form compact masses, rarely
 as bipyrimidal crystals.'''


def GenerateCircularGradientImage(imgsize, innerColor, outerColor):
    image = Image.new('RGB', imgsize)
    for y in range(imgsize[1]):
        for x in range(imgsize[0]):

            #Find the distance to the center
            distanceToCenter = math.sqrt((x - imgsize[0]/2) ** 2 + (y - imgsize[1]/2) ** 2)

            #Make it on a scale from 0 to 1
            distanceToCenter = float(distanceToCenter) / (math.sqrt(2) * imgsize[0]/2)

            #Calculate r, g, and b values
            r = outerColor[0] * distanceToCenter + innerColor[0] * (1 - distanceToCenter)
            g = outerColor[1] * distanceToCenter + innerColor[1] * (1 - distanceToCenter)
            b = outerColor[2] * distanceToCenter + innerColor[2] * (1 - distanceToCenter)

            #Place the pixel
            image.putpixel((x, y), (int(r), int(g), int(b)))

    return image

def GenerateRectangularGradientImage(imgsize, innerColor, outerColor):
    image = Image.new('RGB', imgsize)
    for y in range(imgsize[1]):
        for x in range(imgsize[0]):
            #Find the distance to the closest edge
            distanceToEdge = min(abs(x - imgsize[0]), x, abs(y - imgsize[1]), y)

            #Make it on a scale from 0 to 1
            distanceToEdge = float(distanceToEdge) / (imgsize[0]/2)

            #Calculate r, g, and b values
            r = innerColor[0] * distanceToEdge + outerColor[0] * (1 - distanceToEdge)
            g = innerColor[1] * distanceToEdge + outerColor[1] * (1 - distanceToEdge)
            b = innerColor[2] * distanceToEdge + outerColor[2] * (1 - distanceToEdge)

            #Place the pixel
            image.putpixel((x, y), (int(r), int(g), int(b)))

    return image


def GenerateKeyImage(text, output_path, bgcolor):
    TEXT_COLOR = "white"

    # Create an image with a bg colour and gradient.
    img = randint(0,3)
    if (img == 0):
        img = GenerateCircularGradientImage((MAX_W, MAX_H), bgcolor, (0,0,0))
    if (img == 1):
        img = GenerateCircularGradientImage((MAX_W, MAX_H), (0,0,0), bgcolor)
    if (img == 2):
        img = GenerateRectangularGradientImage((MAX_W, MAX_H), bgcolor, (0,0,0))
    if (img == 3):
        img = GenerateRectangularGradientImage((MAX_W, MAX_H), (0,0,0), bgcolor)

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

    # Create an image with a bg colour and gradient.
    img = randint(0,3)
    if (img == 0):
        img = GenerateCircularGradientImage((MAX_W, MAX_H), bgcolor, (255,255,255))
    if (img == 1):
        img = GenerateCircularGradientImage((MAX_W, MAX_H), (255,255,255), bgcolor)
    if (img == 2):
        img = GenerateRectangularGradientImage((MAX_W, MAX_H), bgcolor, (255,255,255))
    if (img == 3):
        img = GenerateRectangularGradientImage((MAX_W, MAX_H), (255,255,255), bgcolor)

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
