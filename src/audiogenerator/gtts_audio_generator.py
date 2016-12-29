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
# TODO: Pass the language and other configs as flags.
# TODO: Maybe edit the speed/accent of the audio.

from gtts import gTTS
import os

LANGUAGE = 'en'


def GenerateAudio(key_text, value_text, key_output_path, value_output_path):
    print "Generating Audio now."

    ttsKey = gTTS(text=key_text, lang=LANGUAGE)
    ttsKey.save(key_output_path)

    ttsValue = gTTS(text=value_text, lang=LANGUAGE)
    ttsValue.save(value_output_path)
