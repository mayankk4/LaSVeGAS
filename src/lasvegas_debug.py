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

from lasvegas_state import *

# List of colours which is read into memory from a text file.
colors = []

def validate_args(args):
    if not args.path_to_bgcolors_file:
        exit("Please specify a valid file using --path_to_bgcolors_file.")
    if not os.path.exists(args.path_to_bgcolors_file):
        exit("Please specify a valid file using --path_to_bgcolors_file.")

    if not args.audio_accent:
        exit("Please add --audio_accent.")

    if not args.path_to_output:
        exit("Please add --path_to_output.")


def read_bgcolors(path_to_bgcolors_file):
    with open(path_to_bgcolors_file) as f:
        for line in f:
            if (line.startswith('rgb')):
                colors.append(line.split('(')[1].split(')')[0])


def run_pipeline(args):
    # CUSTOMIZE THESE PARAMETERS FOR THE VIDEO
    key = "Empressite"
    values = [
        "Empressite is a mineral form of silver telluride, AgTe.",
        "It is a rare, grey, orthorhombic mineral with which can form compact masses, rarely as bipyrimidal crystals.",
        "Empressite is a mineral form of silver telluride, AgTe.",
        "It is a rare, grey, orthorhombic mineral with which can form compact masses, rarely as bipyrimidal crystals.",
        "Empressite is a mineral form of silver telluride, AgTe.",
        "It is a rare, grey, orthorhombic mineral with which can form compact masses, rarely as bipyrimidal crystals.",
    ]
    
    
    # Validate the args
    validate_args(args)

    # Read the colors file into memory once
    read_bgcolors(args.path_to_bgcolors_file)
    print "[DEBUG] Read " + str(len(colors)) + " colors for background."

    # Choose bgcolour
    bg_color = tuple(
        map(int, colors[randint(0, len(colors) - 1)].split(',')))
    print "[DEBUG] Background color: "
    print bg_color

    state = VideoGenerationState(key, values, bg_color, args.audio_accent, args.path_to_output)

    # Generate images
    image_generator.GenerateImages(state)

    # Generate audio
    audio_generator.GenerateAudios(state)

    # Mux
    ffmpeg_av_mux.AvMux(state)

    # Upload
    # if args.upload_to_youtube:
    #     youtube_utils.UploadVideo(
    #         args.debug_key, args.debug_value, args.path_to_output, "public")
    # else:
    #     print "Skipping youtube upload since flag is not enabled."

    print "================================================================"
    print "Successfully completed."
    print "================================================================"


if __name__ == '__main__':
    # Define all Flags here
    argparser.add_argument("--upload_to_youtube", default=False)

    argparser.add_argument("--path_to_bgcolors_file")

    # Can use en-us, en-uk or en-au.
    argparser.add_argument("--audio_accent")

    # Debugging related flags
    argparser.add_argument("--path_to_output")

    args = argparser.parse_args()

    # Run the pipeline in debugging mode.
    run_pipeline(args)
