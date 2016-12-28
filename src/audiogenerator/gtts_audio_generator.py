''' A text to mp3 converter.

Notes:
The library has some tts support for convert Chemical formulae, although kind of
inaccurate. TTS support for math formulae (a^{2}+b^{2}=c^{2}) seems to be
lacking.

Benchmark:
For a small 2 line paragraph (~200 characters)
time <5s
file-size <100KB

'''
# TODO: Pass the text/language as flags.
# TODO: Maybe edit the speed/accent of the audio.

from gtts import gTTS
import os

LANGUAGE = 'en'

def GenerateAudio():
    print "Generating Audio."
    keyText = "Empressite."
    valueText = "Empressite is a mineral form of silver telluride, AgTe. It is a rare, grey, orthorhombic mineral with which can form compact masses, rarely as bipyrimidal crystals."

    ttsKey = gTTS(text=keyText, lang=LANGUAGE)
    ttsKey.save("./test-data/audio/key.mp3")

    ttsValue = gTTS(text=valueText, lang=LANGUAGE)
    ttsValue.save("./test-data/audio/value.mp3")
