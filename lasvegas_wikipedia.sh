#!/bin/sh

########### USAGE #################
## time sh lasvegas_wikipedia.sh ##
###################################

# Run this script from ./lasvegas
echo "Running lasvegas_tool for wikipedia."


################################################################################
################################################################################
# IMPORTANT : PLEASE SPECIFY A SEPARATE path_to_output FOR EACH WORKER.
################################################################################
################################################################################

# clear folders except input.
rm -R ./test-data/*
# Activate virtual env
echo "Activating virtual environment."
source venv/bin/activate

echo '{}' > ./src/channels/wikipedia/contentgenerator/video_status

python ./src/channels/wikipedia/main.py \
  --path_to_bgcolors_file="./src/utils/bgcolor/modern_colors.txt" \
  --path_to_output="./test-data" \
  --path_to_content="./src/channels/wikipedia/contentgenerator/video_contents"\
  --path_to_status_file="./src/channels/wikipedia/contentgenerator/video_status"


# deactivate virtual env
echo "Dectivating virtual environment."
deactivate
