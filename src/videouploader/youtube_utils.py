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

    keywords = 'wikipedia, meaning, education, wiki, means, definition, pronunciation, pronounce'
    return (title, desc, category, keywords)


class Object(object):
    pass


def UploadVideo(state):
    # Note: state.upload_to_youtube is parsed as a string.
    if state.upload_to_youtube == "False":
        print "Skipping youtube upload since flag is not enabled."
        return

    title, desc, category, keywords = constructVidProps(
        state.title, state.lines)
    file_path = str(state.path_to_output) + "/final_output.mp4"
    args = Object()
    args.title = str(title)
    args.description = str(desc)
    args.category = str(category)
    args.keywords = str(keywords)
    args.file = file_path
    args.privacyStatus = "public"
    args.logging_level = ""

    UploadToYoutube(args)
