import subprocess

#
#
# The class is the wrapper over google's youtube_video_uploader.py which supports video upload functionality on youtube
# Upload video example:
# python youtube_video_uploader.py --title 'test' --description 'valid description of the video' --file  final_output.mp4
# Before running point CLIENT_SECRETS_FILE to valid 'client_secrets.json'
#
#


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


def UploadVideo(state):
    # Note: state.upload_to_youtube is parsed as a string.
    if state.upload_to_youtube == "False":
        print "Skipping youtube upload since flag is not enabled."
        return

    title, desc, category, tags = constructVidProps(state.title, state.lines)
    upload_cmd = ("python src/videouploader/youtube_video_uploader.py "
                  " --title '" + str(title) + "'"
                  " --description '" + str(desc) + "'"
                  " --category '" +
                  str(category) + "'"
                  " --keywords '" +
                  str(tags) + "'"
                  " --file '" +
                  str(state.path_to_output) + "/final_output.mp4" + "'"
                  " --privacyStatus '" + "public") + "'"
    subprocess.call(upload_cmd, shell=True)
