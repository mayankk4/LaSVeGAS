''' A worker which processes a single state. Multiple workers may
 be spawned parallely provided each one works in a different directory.

'''

# local libraries
from imagegenerator import *
from audiogenerator import *
from videogenerator import *
from videouploader import *


def ProcessState(state):
    # Generate images
    image_generator.GenerateImages(state)

    # Generate audio
    audio_generator.GenerateAudios(state)

    # Mux
    ffmpeg_av_mux.AvMux(state)

    # Upload
    youtube_utils.UploadVideo(state)

    print "================================================================"
    print "Successfully completed for key: " + state.title
    print "================================================================"
