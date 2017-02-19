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

from gtts import gTTS
import os


def GenerateAudio(text, output_path, audio_accent):
    print "Generating Audio now."

    ttsKey = gTTS(text=text, lang=audio_accent)
    ttsKey.save(output_path)
