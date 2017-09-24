#!/bin/sh

########### USAGE #############
# time sh lasvegas_debug.sh
###############################

# Run this script from ./lasvegas
echo "Running lasvegas_tool."


# clear folders except input.
rm -R ./test-data/*

# Activate virtual env
echo "Activating virtual environment."
source venv/bin/activate

python ./src/lasvegas_debug.py \
  --path_to_bgcolors_file="./src/utils/bgcolor/modern_colors.txt" \
  --path_to_output="./test-data" \
  --audio_accent="en-us" \

# deactivate virtual env
echo "Dectivating virtual environment."
deactivate
