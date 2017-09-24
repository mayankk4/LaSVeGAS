''' Generates mp3 outputs for the given VideoGenerationState.

The videos are generated in the following format

<path_to_output>/key_audio.mp3

<path_to_output>/value_audio0.mp3
<path_to_output>/value_audio1.mp3
<path_to_output>/value_audio2.mp3
...

'''

from audiogenerator import gtts_audio_generator

def GenerateAudios(state):
    gtts_audio_generator.GenerateAudio(state.title,
                                       state.path_to_output + "/key_audio.mp3",
                                       state.accent)


    for i in range(len(state.values)):
        gtts_audio_generator.GenerateAudio(state.values[i],
                                           state.path_to_output + "/value_audio" + str(i) + ".mp3",
                                           state.accent)
