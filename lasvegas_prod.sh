#!/bin/sh

########### USAGE #################
## time sh lasvegas_prod.sh ##
###################################

## Spawns a single worker which processes a shard of input data and uploads it to youtube.
echo "Starting a LaSVeGAS prod worker."


################################################################################
################################################################################
# IMPORTANT : PLEASE SPECIFY A SEPARATE worker_id FOR EACH WORKER.
################################################################################
################################################################################


python ./src/lasvegas_prod.py \
  --path_to_bgcolors_file="./src/utils/bgcolor/modern_colors.txt" \
  --audio_accent="en-us" \
  --path_to_worker_inputs="./src/channels/wikipedia/contentgenerator/input-shards/"\
  --path_to_worker_outputs="./prod-data/tmp/" \
  --path_to_worker_summary="./prod-data/summary/" \
  --upload_to_youtube=True \
  --worker_id=1
