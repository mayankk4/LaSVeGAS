''' Pipeline runner for Wikipedia channel.

Please use lasvegas_wikipedia.sh to run the pipeline.

'''
import os
import subprocess

from random import randint
from oauth2client.tools import argparser

# local libraries
from lasvegas_state import *
from lasvegas_worker import *

from channels.wikipedia.executor import *

# List of colours which is read into memory from a text file.
colors = []


def validate_prod_args(args):
    if not args.path_to_bgcolors_file:
        exit("Please specify a valid file using --path_to_bgcolors_file.")
    if not os.path.exists(args.path_to_bgcolors_file):
        exit("Please specify a valid file using --path_to_bgcolors_file.")
    if not args.audio_accent:
        exit("Please add --audio_accent.")
    if not args.worker_id:
        exit("Please add --worker_id.")

    if not args.path_to_worker_inputs:
        exit("Please add --path_to_worker_inputs.")
    if not args.path_to_worker_outputs:
        exit("Please add path_to_worker_outputs.")

    if not args.path_to_worker_summary:
        exit("Please add --path_to_worker_summary.")



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

    worker_id = args.worker_id
    print "================================================================"
    print "Running worker: " + worker_id
    print "================================================================"

    # Read the colors file into memory once
    read_bgcolors(args.path_to_bgcolors_file)
    print "Read " + str(len(colors)) + " colors for background."


    # Create various paths.
    input_file = args.path_to_worker_inputs + "input_shard_" + worker_id
    # Note: no / at the end of output path
    output_path = args.path_to_worker_outputs + "worker-" + worker_id
    sumamry_file = args.path_to_worker_summary + "summary_worker_" + worker_id + ".txt"

    print "Worker input file: " + input_file
    print "Worker summary file: " + sumamry_file
    print "Worker temp folder path: " + output_path
    create_summary_path_command = "mkdir -p " + args.path_to_worker_summary
    subprocess.call(create_summary_path_command, shell=True)
    make_tmp_dir_command = "mkdir -p " + output_path
    subprocess.call(make_tmp_dir_command, shell=True)
    clear_tmp_dir_command = "rm -Rf " + output_path + "/*"
    subprocess.call(clear_tmp_dir_command, shell=True)

    # TODO: Update pipeline to set the state status everywhere.

    # key_value_pairs = pip_lifecycle.GetAllKeyValues(args.path_to_content)
    key_values_pairs = {
        "Empressite":  [
            "Empressite is a mineral form of silver telluride, AgTe. It is a rare, grey, orthorhombic mineral with which can form compact masses.",
            "Empressite is a mineral form of silver telluride, AgTe. It is a rare, grey, orthorhombic mineral with which can form compact masses.",
            ],
    }

    # For all the key,value in content file
    for key, values in key_values_pairs.iteritems():
        print "================================================================"
        print "Running for title: " + key
        print "Running for values: " + str(values)
        print "================================================================"

        # Clear all data in the temp folder.
        subprocess.call(clear_tmp_dir_command, shell=True)

        # Choose bgcolour
        bg_color = tuple(
            map(int, colors[randint(0, len(colors) - 1)].split(',')))

        state = VideoGenerationState(
            key, values, bg_color, args.audio_accent, output_path, args.upload_to_youtube)
        # ProcessState(state)

        # Write final status to the summary file.
        update_summary_command = "echo \"" + state.status + " | " + key + "\" >> " + sumamry_file
        subprocess.call(update_summary_command, shell=True)


        subprocess.call(clear_tmp_dir_command, shell=True)

        print "================================================================"
        print "Run successfully completed for title: " + key
        print "================================================================"

    print "Finished running the pipeline."


if __name__ == '__main__':
    # Define all Flags here
    argparser.add_argument("--path_to_bgcolors_file")
    # Can use en-us, en-uk or en-au.
    argparser.add_argument("--audio_accent")

    argparser.add_argument("--worker_id")

    argparser.add_argument("--path_to_worker_inputs")
    argparser.add_argument("--path_to_worker_outputs")
    argparser.add_argument("--path_to_worker_summary")

    argparser.add_argument("--upload_to_youtube", default=False)

    args = argparser.parse_args()
    run_pipeline_prod(args)
