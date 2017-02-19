#!/bin/sh

########### USAGE #############
# time sh lasvegas_debug.sh
# time sh lasvegas_debug.sh -- --upload_to_youtube=false
###############################

# Run this script from ./lasvegas
echo "Running lasvegas_tool."


# clear folders except input.
rm -R ./test-data/*
mkdir ./test-data/audio/
mkdir ./test-data/image/
mkdir ./test-data/video/
# Activate virtual env
echo "Activating virtual environment."
source venv/bin/activate

python ./src/lasvegas_debug.py \
  --debug_key="Empressite" \
  --debug_value="Empressite is a mineral form of silver telluride, AgTe. It is a rare, grey, orthorhombic mineral with which can form compact masses, rarely as bipyrimidal crystals." \
  --path_to_bgcolors_file="./src/utils/bgcolor/modern_colors.txt" \
  --path_to_key_image="./test-data/image/key.png" \
  --path_to_value_image="./test-data/image/value.png" \
  --path_to_key_audio="./test-data/audio/key.mp3" \
  --path_to_value_audio="./test-data/audio/value.mp3" \
  --path_to_output="./test-data/video/final_output.mp4" \
  --video_privacy_status="public" \

# deactivate virtual env
echo "Dectivating virtual environment."
deactivate
