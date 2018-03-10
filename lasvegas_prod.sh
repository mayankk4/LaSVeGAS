#!/bin/sh

########### USAGE #################
## time sh lasvegas_wikipedia.sh ##
###################################

## Spawns a single worker which processes a subset of data and uploads it to youtube.
# Run this script from ./lasvegas
echo "Running lasvegas_tool over production data."


################################################################################
################################################################################
# IMPORTANT : PLEASE SPECIFY A SEPARATE path_to_output FOR EACH WORKER.
################################################################################
################################################################################


python ./src/lasvegas_prod.py \
  --path_to_bgcolors_file="./src/utils/bgcolor/modern_colors.txt" \
  --audio_accent="en-us" \
  --path_to_worker_inputs="./src/channels/wikipedia/contentgenerator/input-shards/"\
  --path_to_worker_outputs="./prod-data/tmp/" \
  --path_to_worker_summary="./prod-data/summary/" \
  --upload_to_youtube=false \
  --worker_id=1
