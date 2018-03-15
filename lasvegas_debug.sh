#!/bin/sh

########### USAGE #############
# time sh lasvegas_debug.sh
###############################

# Run this script from ./lasvegas
echo "Running lasvegas_tool."


rm -R ./test-data/*

python ./src/lasvegas_debug.py \
  --path_to_bgcolors_file="./src/utils/bgcolor/modern_colors.txt" \
  --path_to_output="./test-data" \
  --upload_to_youtube=False \
  --audio_accent="en-us" \
