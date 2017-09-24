''' Pipeline runner for Wikipedia channel.

Please use lasvegas_wikipedia.sh to run the pipeline.

'''
import os

from random import randint
from oauth2client.tools import argparser

# local libraries
from lasvegas_state import *
from lasvegas_worker import *

from wikipedia/executor import *

# List of colours which is read into memory from a text file.
colors = []


def validate_prod_args(args):
    if not args.path_to_bgcolors_file:
        exit("Please specify a valid file using --path_to_bgcolors_file.")
    if not os.path.exists(args.path_to_bgcolors_file):
        exit("Please specify a valid file using --path_to_bgcolors_file.")

    if not args.path_to_output:
        exit("Please add --path_to_output.")

    if not args.path_to_content:
        exit("Please add path_to_content.")

    if not args.path_to_status_file:
        exit("Please add --path_to_status_file.")


def read_bgcolors(path_to_bgcolors_file):
    with open(path_to_bgcolors_file) as f:
        for line in f:
            if (line.startswith('rgb')):
                colors.append(line.split('(')[1].split(')')[0])


#
# TODO: try-catch for error free run
#
def run_pipeline_prod(args):
    # Validate the args
    validate_prod_args(args)

    # Read the colors file into memory once
    read_bgcolors(args.path_to_bgcolors_file)
    print "Read " + str(len(colors)) + " colors for background."

    # Load candidate datasets for upload
    key_value_pairs = pip_lifecycle.GetAllKeyValues(args.path_to_content)

    # For all the key,value in content file
    for key, value in key_value_pairs.iteritems():
        print "================================================================"
        print "Running for title: " + key
        print "================================================================"

        # Starting the execution with status as RUNNING(1)
        started, message = pip_lifecycle.StartExecution(
            key, args.path_to_status_file)
        if not started:
            print message
            continue


        # Choose bgcolour
        bg_color = tuple(
            map(int, colors[randint(0, len(colors) - 1)].split(',')))


        #TODO: UPDATE THIS TO ADD A LIST OF LINES TO VALUE INSTEAD OF A SINGLE VALUE.
        state = VideoGenerationState(key, [value,], bg_color, args.audio_accent, args.path_to_output, args.upload_to_youtube)
        ProcessState(state)

        # Ending the execution with status SUCCESS(3)
        pip_lifecycle.EndExecution(key, args.path_to_status_file)
        
        #TODO: RUN CLEANUPS HERE - CLEAR THE DIRECTORY.

        print "================================================================"
        print "Run successfully completed for title: " + key
        print "================================================================"

    print "Finished running the pipeline."


if __name__ == '__main__':
    # Define all Flags here
    argparser.add_argument("--upload_to_youtube", default=False)

    argparser.add_argument("--path_to_bgcolors_file")

    # Can use en-us, en-uk or en-au.
    argparser.add_argument("--audio_accent")

    # Debugging related flags
    argparser.add_argument("--path_to_output")

    argparser.add_argument("--path_to_content")
    argparser.add_argument("--path_to_status_file")

    args = argparser.parse_args()

    run_pipeline_prod(args)
