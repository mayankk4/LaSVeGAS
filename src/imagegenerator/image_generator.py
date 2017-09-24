''' Generates png (lossless) outputs for the given VideoGenerationState.

The images are generated in the following format

<path_to_output>/key_image.png

<path_to_output>/value_image0.png
<path_to_output>/value_image1.png
<path_to_output>/value_image2.png
...

'''

from imagegenerator import pil_key_image_generator
from imagegenerator import pil_value_image_generator

def GenerateImages(state):
    pil_key_image_generator.GenerateImage(state.title,
                                          state.path_to_output + "/key_image.png",
                                          state.bgcolor)


    for i in range(len(state.values)):
        pil_value_image_generator.GenerateImage(state.values[i],
                                                state.path_to_output + "/value_image" + str(i) + ".png",
                                                state.bgcolor)
