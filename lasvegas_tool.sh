#!/bin/sh

########### USAGE #############
## time sh lasvegas_tool.sh ##
###############################

# Run this script from ./lasvegas
echo "Running the pipeline for a single input."


# clear folders except input.
rm ./test-data/audio/*
rm ./test-data/image/*
rm ./test-data/video/*


# Activate virtual env
source venv/bin/activate


echo "Running the pipeline."
python ./src/main.py

# deactivate virtual env
deactivate


echo "Bye."
