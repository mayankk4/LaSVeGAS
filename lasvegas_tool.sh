#!/bin/sh

########### USAGE #############
## time sh lasvegas_tool.sh ##
###############################

# Run this script from ./lasvegas
echo "Running the pipeline for a single input."


# clear folders except input.
rm -R ./test-data/*
mkdir ./test-data/audio/
mkdir ./test-data/image/
mkdir ./test-data/video/

# Activate virtual env
source venv/bin/activate


echo "Running the pipeline in debug mode."
python ./src/main.py

# deactivate virtual env
deactivate
