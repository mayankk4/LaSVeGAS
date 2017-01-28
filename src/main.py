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
from videouploader import *
from pipelineexecutor import *



# List of colours which is read into memory from a text file.
colors = []

def validate_debug_args(args):
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
    	exit("9: Please check video_privacy_status: {'public', 'private', 'unlisted'} ")


def validate_prod_args(args):
    if not args.path_to_bgcolors_file:
    	exit("1: Please specify a valid file using --path_to_bgcolors_file.")
    if not os.path.exists(args.path_to_bgcolors_file):
    	exit("2: Please specify a valid file using --path_to_bgcolors_file.")
    if not args.path_to_content:
    	exit("3: Please check path_to_content.")
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
    	exit("9: Please check video_privacy_status: {'public', 'private', 'unlisted'} ")
    if not args.path_to_status_file:
    	exit("10: Please check path_to_status_file.")


def read_bgcolors(path_to_bgcolors_file):
    with open(path_to_bgcolors_file) as f:
        for line in f:
            if (line.startswith('rgb')):
                colors.append(line.split('(')[1].split(')')[0])


def run_pipeline_debug(args):
	 	#Validate the args
    validate_debug_args(args)

    # Read the colors file into memory once
    read_bgcolors(args.path_to_bgcolors_file)
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

    # Upload
    youtube_utils.UploadVideo(args.debug_key, args.debug_value, args.path_to_output, args.video_privacy_status)


    print "================================================================"
    print "Successfully completed."
    print "================================================================"


#
# TODO: try-catch for error free run
#
def run_pipeline_prod(args):

    #Validate the args
    validate_prod_args(args)

		#Load candidate datasets for upload
    key_value_pairs = pip_lifecycle.GetAllKeyValues(args.path_to_content)

    #For all the key,value in content file
    for key, value in key_value_pairs.iteritems():
    	print "Running for key: " + key

    	#Starting the execution with status as RUNNING(1)
    	started, message = pip_lifecycle.StartExecution(key, args.path_to_status_file)
    	if not started:
    		print message
    		continue

    	# Read the colors file into memory once
    	read_bgcolors(args.path_to_bgcolors_file)
    	print "Read " + str(len(colors)) + " colors for background."


    	# Choose bgcolour
    	key_bg_color = tuple(
	        map(int, colors[randint(0, len(colors) - 1)].split(',')))
    	value_bg_color = tuple(
	        map(int, colors[randint(0, len(colors) - 1)].split(',')))


    	# Generate images
    	pil_key_image_generator.GenerateImage(key, args.path_to_key_image,
	                                          key_bg_color)

    	pil_value_image_generator.GenerateImage(value, args.path_to_value_image,

	                                            value_bg_color)
    	# Generate audio
    	gtts_audio_generator.GenerateAudio(key, value,
	                                       args.path_to_key_audio, args.path_to_value_audio)

    	# Mux
    	ffmpeg_av_mux.AvMux(args.path_to_key_image, args.path_to_value_image,
	                        args.path_to_key_audio, args.path_to_value_audio,
	                        args.path_to_output)

    	# Upload
    	youtube_utils.UploadVideo(key, value, args.path_to_output, args.video_privacy_status)


    	#Ending the execution with status SUCCESS(3)
    	pip_lifecycle.EndExecution(key, args.path_to_status_file)

    	print "================================================================"
    	print "Run successfully completed for " + key
    	print "================================================================"

    print "Finished running the pipeline"


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
    argparser.add_argument("--video_privacy_status")
    argparser.add_argument("--path_to_content")
    argparser.add_argument("--path_to_status_file")

    args = argparser.parse_args()
    print args.path_to_bgcolors_file
    if args.debug.lower() in ("yes", "true", "t", "1"):
    	run_pipeline_debug(args)
    else:
    	run_pipeline_prod(args)
