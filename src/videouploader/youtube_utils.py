'''
Wrapper over Google's youtube_video_uploader.py which helps in 
uploading a video to youtube.

Before running point CLIENT_SECRETS_FILE in youtube_video_uploader.py
to valid 'client_secrets.json'

'''


import subprocess

from youtube_video_uploader import *

# CUSTOMIZE THIS FUNCTION PER PROJECT.
# Props for goodreads.
def constructVidProps(title, lines):
    title = title
    desc = '. '.join(lines)
    category = '''27'''

    tags = 'wikipedia, meaning, education, wiki, mean'
    # Add keywords by breaking the description into words.
    words_in_lines = map(str.split, lines)
    for i in range(len(words_in_lines)):
        if (len(words_in_lines[i]) > 2):
            tags += ', '.join(words_in_lines[i])

    return (title, desc, category, tags)


class Object(object):
    pass


def UploadVideo(state):
    # Note: state.upload_to_youtube is parsed as a string.
    if state.upload_to_youtube == "False":
        print "Skipping youtube upload since flag is not enabled."
        return

    title, desc, category, tags = constructVidProps(state.title, state.lines)
    file_path = str(state.path_to_output) + "/final_output.mp4"
    a = Object()
    a.title = str(title)
    a.description = str(desc)
    a.category = str(category)
    a.keywords = str(tags)
    a.file = file_path
    a.privacyStatus = "public"
    a.logging_level = ""

    UploadToYoutube(a)
