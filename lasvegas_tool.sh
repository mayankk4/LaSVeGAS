#!/bin/sh

########### USAGE #############
## time sh lasvegas_tool.sh ##
###############################

# Run this script from ./lasvegas
echo "Running the pipeline for a single input."

# clear folders except input.
# rm ./test-data/audio/*
# rm ./test-data/image/*
rm ./test-data/video/*


# Activate virtual env
source venv/bin/activate


# generate image

# generate audio

# generate video
echo "Generating video."
python ./video-generator/opencv-video-generator.py


# deactivate virtual env
deactivate


echo "Bye."
