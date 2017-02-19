''' Some utils to generate background images with gradients.

'''

import PIL
import math

from PIL import Image
from random import randint


# Create an image with a bg colour and gradient.
# (0,0,0) is black
def GenerateRandomKeyImageBackground(MAX_W, MAX_H, bgcolor):
    img = randint(0, 3)
    if (img == 0):
        img = GenerateCircularGradientImage((MAX_W, MAX_H), bgcolor, (0, 0, 0))
    if (img == 1):
        img = GenerateCircularGradientImage((MAX_W, MAX_H), (0, 0, 0), bgcolor)
    if (img == 2):
        img = GenerateRectangularGradientImage(
            (MAX_W, MAX_H), bgcolor, (0, 0, 0))
    if (img == 3):
        img = GenerateRectangularGradientImage(
            (MAX_W, MAX_H), (0, 0, 0), bgcolor)

    return img

# Create an image with a bg colour and gradient.
# (255,255,255) is white


def GenerateRandomValueImageBackground(MAX_W, MAX_H, bgcolor):
    img = randint(0, 1)
    if (img == 0):
        img = GenerateCircularGradientImage(
            (MAX_W, MAX_H), (255, 255, 255), bgcolor)
    if (img == 1):
        img = GenerateRectangularGradientImage(
            (MAX_W, MAX_H), (255, 255, 255), bgcolor)

    return img


def GenerateCircularGradientImage(imgsize, innerColor, outerColor):
    image = Image.new('RGB', imgsize)
    for y in range(imgsize[1]):
        for x in range(imgsize[0]):

            # Find the distance to the center
            distanceToCenter = math.sqrt(
                (x - imgsize[0] / 2) ** 2 + (y - imgsize[1] / 2) ** 2)

            # Make it on a scale from 0 to 1
            distanceToCenter = float(distanceToCenter) / \
                (math.sqrt(2) * imgsize[0] / 2)

            # Calculate r, g, and b values
            r = outerColor[0] * distanceToCenter + \
                innerColor[0] * (1 - distanceToCenter)
            g = outerColor[1] * distanceToCenter + \
                innerColor[1] * (1 - distanceToCenter)
            b = outerColor[2] * distanceToCenter + \
                innerColor[2] * (1 - distanceToCenter)

            # Place the pixel
            image.putpixel((x, y), (int(r), int(g), int(b)))

    return image


def GenerateRectangularGradientImage(imgsize, innerColor, outerColor):
    image = Image.new('RGB', imgsize)
    for y in range(imgsize[1]):
        for x in range(imgsize[0]):
            # Find the distance to the closest edge
            distanceToEdge = min(
                abs(x - imgsize[0]), x, abs(y - imgsize[1]), y)

            # Make it on a scale from 0 to 1
            distanceToEdge = float(distanceToEdge) / (imgsize[0] / 2)

            # Calculate r, g, and b values
            r = innerColor[0] * distanceToEdge + \
                outerColor[0] * (1 - distanceToEdge)
            g = innerColor[1] * distanceToEdge + \
                outerColor[1] * (1 - distanceToEdge)
            b = innerColor[2] * distanceToEdge + \
                outerColor[2] * (1 - distanceToEdge)

            # Place the pixel
            image.putpixel((x, y), (int(r), int(g), int(b)))

    return image
