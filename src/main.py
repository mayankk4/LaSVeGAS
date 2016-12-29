''' Pipeline runner.

Please use lasvegas_tool.sh to run the pipeline in debug mode.

1. Read the dump.

2. For each KV-pair in the dump,
    - generate image files
    - generate audio files
    - generate video file using images

'''
from imagegenerator import *
from audiogenerator import *
from videogenerator import *

# TODO: Pass these in as flags.
PATH_TO_DUMP_INPUT = "./test-data/input/input.txt"
KEY_IMAGE_PATH = "./test-data/image/key.png"
VALUE_IMAGE_PATH = "./test-data/image/value.png"
KEY_AUDIO_PATH = "./test-data/audio/key.mp3"
VALUE_AUDIO_PATH = "./test-data/audio/value.mp3"
SILENT_VIDEO_PATH = "./test-data/video/silent_video.avi"
FINAL_OUTPUT_PATH = "./test-data/video/final_output.mkv"

# TODO: read input text from the dump instead
INPUT_KEY = '''Empressite'''
INPUT_VALUE = '''Empressite is a mineral form of silver telluride, AgTe. It is a rare, grey, orthorhombic mineral with which can form compact masses, rarely as bipyrimidal crystals.'''

# Generate images
pil_key_image_generator.GenerateImage(INPUT_KEY, KEY_IMAGE_PATH)
pil_value_image_generator.GenerateImage(INPUT_VALUE, VALUE_IMAGE_PATH)

# Generate audio
gtts_audio_generator.GenerateAudio(
    INPUT_KEY, INPUT_VALUE, KEY_AUDIO_PATH, VALUE_AUDIO_PATH)

# Generate video
opencv_silent_video_generator.GenerateSilentVideo(
    KEY_IMAGE_PATH, VALUE_IMAGE_PATH, SILENT_VIDEO_PATH)

# Mux
ffmpeg_av_mux.AvMux(VALUE_AUDIO_PATH, SILENT_VIDEO_PATH, FINAL_OUTPUT_PATH)
