
import subprocess

''' Useful commands

# Muxing audio with a silent video
ffmpeg -y -i key.mp3  -r 30 -i silent_video.avi  -filter:a aresample=async=1 -c:a flac -c:v copy output.mkv

# Muxing images and audio and then joining the videos.
ffmpeg -i key.png -i key.mp3 -c:a flac -c:v copy key.mkv
ffmpeg -i value.png -i value.mp3 -c:a flac -c:v copy value.mkv

# Joining the files
#  With an input file list
    fmpeg -f concat -i mylist.txt -c copy output.mkv
#  General
    rm tmp.txt
    printf "file 'key.mkv'\nfile 'value.mkv'\n" > tmp.txt
    ffmpeg -f concat -i - -c copy final_output.mkv

'''


def AvMux(key_image_path, value_image_path, key_audio_path, value_audio_path, output_path):
    print "Muxing the audio with the silent video."

    cmd0 = "mkdir tmp"
    cmd1 = "ffmpeg  -y -loop 1 -i " + key_image_path + " -i " + \
        key_audio_path + " -c:v libx264 -c:a aac -strict experimental -b:a 348k -shortest tmp/key.mp4"
    cmd2 = "ffmpeg  -y -loop 1 -i " + value_image_path + " -i " + \
        value_audio_path + \
        " -c:v libx264 -c:a aac -strict experimental -b:a 348k -shortest tmp/value.mp4"
    cmd3 = "rm tmp/input_list.txt"
    cmd4 = "printf 'file \'key.mp4\'\nfile \'value.mp4\'\n' > tmp/input_list.txt"
    cmd5 = "ffmpeg -y -f concat -i tmp/input_list.txt -c copy tmp/tmp.mp4"
    cmd6 = "ffmpeg -y -i tmp/tmp.mp4 -codec:v libx264 -crf 21 -bf 2 -flags +cgop -pix_fmt yuv420p -codec:a aac " + \
        "-strict -2 -b:a 348k -r:a 48000 -movflags faststart " + output_path
    cmd7 = "rm -rf tmp"

    # This is a blocking call.
    subprocess.call(cmd0, shell=True)
    subprocess.call(cmd1, shell=True)
    subprocess.call(cmd2, shell=True)
    subprocess.call(cmd3, shell=True)
    subprocess.call(cmd4, shell=True)
    subprocess.call(cmd5, shell=True)
    subprocess.call(cmd6, shell=True)
    subprocess.call(cmd7, shell=True)

    print "Done processing."
    print output_path
