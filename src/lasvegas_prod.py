'''
*Binary* which runs a single worker which reads a shard of input, generates and
uploads the video to youtube, and writes the final status of each processed key
to a summary text file.

Required flags:
--worker_id
    The UNIQUE id for this worker. Note that this *must* be unique among all
    workers running simultaneously.

--path_to_worker_inputs
    Path to input files. The expectation here is that the input is pre-sharded
    and each worker gets a separate shard of the input, not shared with any
    other worker. Terminated by "/"

    Expected input shard-name for worker with id worker_id:
    path_to_worker_inputs + input_shard_ + worker_id


--path_to_worker_outputs=
    Path to temp output folders. The path is common for all workers, however each
    worker will creat a separate sub-folder. This is needed to store various
    intermediate outputs as well as the final video just before uploading to
    youtube.
    Note that the temp folder is cleared before processing each input. This is
    done in order to save un-necessary storage.

--path_to_worker_summary
    Path to summary files. The path is common for all workers, however each
    worker will creat a separate summary file.

--upload_to_youtube
--path_to_bgcolors_file
--audio_accent

Example invocation:
python ./src/lasvegas_prod.py \
  --path_to_bgcolors_file="./src/utils/bgcolor/modern_colors.txt" \
  --audio_accent="en-us" \
  --path_to_worker_inputs="./src/channels/wikipedia/contentgenerator/input-shards/"\
  --path_to_worker_outputs="./prod-data/tmp/" \
  --path_to_worker_summary="./prod-data/summary/" \
  --upload_to_youtube=false \
  --worker_id=1


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
    sumamry_file = args.path_to_worker_summary + \
        "summary_worker_" + worker_id + ".txt"
    print "Worker input file: " + input_file
    print "Worker summary file: " + sumamry_file
    print "Worker temp folder path: " + output_path
    create_summary_path_command = "mkdir -p " + args.path_to_worker_summary
    subprocess.call(create_summary_path_command, shell=True)
    make_tmp_dir_command = "mkdir -p " + output_path
    subprocess.call(make_tmp_dir_command, shell=True)
    clear_tmp_dir_command = "rm -Rf " + output_path + "/*"
    subprocess.call(clear_tmp_dir_command, shell=True)

    # Records stats for this worker.
    WORKER_ERROR_COUNT = 0
    WORKER_KEYS_PROCESSED = 0

    # TODO: Read KV pairs from a content dump.
    key_values_pairs = {
        "Empressite":  [
            "testing123",
            # "Empressite is a mineral form of silver telluride, AgTe. It is a rare, grey, orthorhombic mineral with which can form compact masses.",
            # "Empressite is a mineral form of silver telluride, AgTe. It is a rare, grey, orthorhombic mineral with which can form compact masses.",
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
        ProcessState(state)

        # Write final status to the summary file.
        update_summary_command = "echo \"" + \
            state.status + " |||" + key + "\" >> " + sumamry_file
        subprocess.call(update_summary_command, shell=True)

        WORKER_KEYS_PROCESSED += 1
        if state.status != "OK":
            WORKER_ERROR_COUNT += 1
            if (WORKER_ERROR_COUNT > 10):
                break

        subprocess.call(clear_tmp_dir_command, shell=True)

        print "================================================================"
        print "Run successfully completed for title: " + key
        print "================================================================"

    print "Finished running the pipeline."
    print "Total keys processed: " + str(WORKER_KEYS_PROCESSED)
    print "Total errors: " + str(WORKER_ERROR_COUNT)


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
