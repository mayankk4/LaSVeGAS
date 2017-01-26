''' Pipeline runner.

Please use lasvegas_tool.sh to run the pipeline in debug mode.

1. Read the dump.

2. For each KV-pair in the dump,
    - generate image files
    - generate audio files
    - mux the images and the audio files to generate the final output.

'''
import os

from random import randint
from oauth2client.tools import argparser

# local libraries
from imagegenerator import *
from audiogenerator import *
from videogenerator import *

# List of colours which is read into memory from a text file.
colors = []


def validate_debug_args(args):
    if not args.path_to_bgcolors_file:
        exit("Please specify a valid file using --path_to_bgcolors_file.")
    if not os.path.exists(args.path_to_bgcolors_file):
        exit("Please specify a valid file using --path_to_bgcolors_file.")

    if not args.debug_key:
        exit("1: Please check args.")
    if not args.debug_value:
        exit("2: Please check args.")
    if not args.path_to_key_image:
        exit("4: Please check args.")
    if not args.path_to_value_image:
        exit("5: Please check args.")
    if not args.path_to_key_audio:
        exit("6: Please check args.")
    if not args.path_to_value_audio:
        exit("7: Please check args.")
    if not args.path_to_output:
        exit("8: Please check args.")


def read_bgcolors(args):
    with open(args.path_to_bgcolors_file) as f:
        for line in f:
            if (line.startswith('rgb')):
                colors.append(line.split('(')[1].split(')')[0])


def run_pipeline_debug(args):
    validate_debug_args(args)

    # Read the colors file into memory once
    read_bgcolors(args)
    print "Read " + str(len(colors)) + " colors for background."

    # Choose bgcolour
    key_bg_color = tuple(
        map(int, colors[randint(0, len(colors) - 1)].split(',')))
    value_bg_color = tuple(
        map(int, colors[randint(0, len(colors) - 1)].split(',')))

    # Generate images
    pil_key_image_generator.GenerateImage(args.debug_key,
                                          args.path_to_key_image,
                                          key_bg_color)
    pil_value_image_generator.GenerateImage(args.debug_value,
                                            args.path_to_value_image,
                                            value_bg_color)

    # Generate audio
    gtts_audio_generator.GenerateAudio(args.debug_key,
                                       args.debug_value,
                                       args.path_to_key_audio,
                                       args.path_to_value_audio)

    # Mux
    ffmpeg_av_mux.AvMux(args.path_to_key_image, args.path_to_value_image,
                        args.path_to_key_audio, args.path_to_value_audio,
                        args.path_to_output)

    print "================================================================"
    print "Successfully completed."
    print "================================================================"

if __name__ == '__main__':
    # Define all Flags here
    argparser.add_argument("--debug", required=True, default=True)

    argparser.add_argument("--path_to_bgcolors_file")

    # Debugging related flags
    argparser.add_argument("--debug_key")
    argparser.add_argument("--debug_value")
    argparser.add_argument("--path_to_key_image")
    argparser.add_argument("--path_to_value_image")
    argparser.add_argument("--path_to_key_audio")
    argparser.add_argument("--path_to_value_audio")
    argparser.add_argument("--path_to_output")

    args = argparser.parse_args()

    if (args.debug):
        run_pipeline_debug(args)

    # Prod run.
