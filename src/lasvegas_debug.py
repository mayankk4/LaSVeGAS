''' Pipeline runner for Debugging.

Please use lasvegas_debug.sh to run the pipeline in debug mode.

'''
import os

from random import randint
from oauth2client.tools import argparser

# local libraries
from imagegenerator import *
from audiogenerator import *
from videogenerator import *
from videouploader import *

# List of colours which is read into memory from a text file.
colors = []


def validate_args(args):
    if not args.path_to_bgcolors_file:
        exit("Please specify a valid file using --path_to_bgcolors_file.")
    if not os.path.exists(args.path_to_bgcolors_file):
        exit("Please specify a valid file using --path_to_bgcolors_file.")

    if not args.debug_key:
        exit("1: Please check debug_key.")
    if not args.debug_value:
        exit("2: Please check debug_value.")
    if not args.path_to_key_image:
        exit("4: Please check path_to_key_image.")
    if not args.path_to_value_image:
        exit("5: Please check path_to_value_image.")
    if not args.path_to_key_audio:
        exit("6: Please check path_to_key_audio.")
    if not args.path_to_value_audio:
        exit("7: Please check path_to_value_audio.")
    if not args.path_to_output:
        exit("8: Please check path_to_output.")
    if not args.video_privacy_status:
        exit(
            "9: Please check video_privacy_status: {'public', 'private', 'unlisted'} ")


def read_bgcolors(path_to_bgcolors_file):
    with open(path_to_bgcolors_file) as f:
        for line in f:
            if (line.startswith('rgb')):
                colors.append(line.split('(')[1].split(')')[0])


def run_pipeline(args):
    # Validate the args
    validate_args(args)

    # Read the colors file into memory once
    read_bgcolors(args.path_to_bgcolors_file)
    print "Read " + str(len(colors)) + " colors for background."

    # Choose bgcolour
    bg_color = tuple(
        map(int, colors[randint(0, len(colors) - 1)].split(',')))

    # Generate images
    pil_key_image_generator.GenerateImage(args.debug_key,
                                          args.path_to_key_image,
                                          bg_color)
    pil_value_image_generator.GenerateImage(args.debug_value,
                                            args.path_to_value_image,
                                            bg_color)

    # Generate audio
    gtts_audio_generator.GenerateAudio(args.debug_key,
                                       args.debug_value,
                                       args.path_to_key_audio,
                                       args.path_to_value_audio)

    # Mux
    ffmpeg_av_mux.AvMux(args.path_to_key_image, args.path_to_value_image,
                        args.path_to_key_audio, args.path_to_value_audio,
                        args.path_to_output)

    # Upload
    if args.upload_to_youtube.lower() in ("yes", "true", "t", "1"):
        youtube_utils.UploadVideo(
            args.debug_key, args.debug_value, args.path_to_output, args.video_privacy_status)
    else:
        print "Skipping youtube upload since flag is not enabled."

    print "================================================================"
    print "Successfully completed."
    print "================================================================"


if __name__ == '__main__':
    # Define all Flags here
    argparser.add_argument("--upload_to_youtube", default=False)

    argparser.add_argument("--path_to_bgcolors_file")

    # Debugging related flags
    argparser.add_argument("--debug_key")
    argparser.add_argument("--debug_value")
    argparser.add_argument("--path_to_key_image")
    argparser.add_argument("--path_to_value_image")
    argparser.add_argument("--path_to_key_audio")
    argparser.add_argument("--path_to_value_audio")
    argparser.add_argument("--path_to_output")
    argparser.add_argument("--video_privacy_status")

    args = argparser.parse_args()

    # Run the pipeline in debugging mode.
    run_pipeline(args)
