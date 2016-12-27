'''
This does not seem to work with Mac or pYTHON 2.7.

'''

import pyttsx

engine = pyttsx.init()
voices = engine.getProperty('voices')

engine.setProperty('voice', voices[0].id) #change index to change voices
engine.say("I'm a little teapot...")

engine.runAndWait()
