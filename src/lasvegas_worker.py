''' A library which processes a single state.

'''

# local libraries
from imagegenerator import *
from audiogenerator import *
from videogenerator import *
from videouploader import *


def ProcessState(state):
    try:
        # Generate images
        image_generator.GenerateImages(state)

        # Generate audio
        audio_generator.GenerateAudios(state)

        # Mux
        ffmpeg_av_mux.AvMux(state)

        # Upload
        youtube_utils.UploadVideo(state)
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as e:
        print(str(e))
        state.status = "ERROR"

    print "Successfully completed uploading for key: " + state.title
