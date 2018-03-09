
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


def AvMux(state):
    print "Muxing the audio with the silent video."

    # subprocess is a blocking call.
    cmd0 = "cp ./static/outro.mp4 " + state.path_to_output + "/outro.mp4"
    subprocess.call(cmd0, shell=True)

    # Video for the key
    key_image_path = state.path_to_output + "/key_image.png"
    key_audio_path = state.path_to_output + "/key_audio.mp3"
    key_output_path = state.path_to_output + "/key_video.mp4"

    cmd1 = "ffmpeg  -loglevel 0 -hide_banner -y -loop 1 -i " + key_image_path + " -i " + \
        key_audio_path + " -c:v libx264 -c:a aac -strict experimental -b:a 348k -shortest " + key_output_path
    subprocess.call(cmd1, shell=True)

    # Individual videos for each value
    i = 0
    for i in range(len(state.values)):
        value_image_path = state.path_to_output + \
            "/value_image" + str(i) + ".png"
        value_audio_path = state.path_to_output + \
            "/value_audio" + str(i) + ".mp3"
        value_output_path = state.path_to_output + \
            "/value_video" + str(i) + ".mp4"
        cmd2 = "ffmpeg  -loglevel 0 -hide_banner -y -loop 1 -i " + value_image_path + " -i " + \
            value_audio_path + \
            " -c:v libx264 -c:a aac -strict experimental -b:a 348k -shortest " + value_output_path
        subprocess.call(cmd2, shell=True)

    # Create a list of input files for `melt`
    input_video_files_list = state.path_to_output + "/key_video.mp4 "
    for i in range(len(state.values)):
        input_video_files_list += state.path_to_output + "/value_video" + str(i) + ".mp4 "
    input_video_files_list += state.path_to_output + "/outro.mp4"  # Add outro


    cmd5 = "melt " + input_video_files_list + " -consumer avformat:" + state.path_to_output + "/tmp.mp4 acodec=libmp3lame vcodec=libx264"
    subprocess.call(cmd5, shell=True)

    output_path = state.path_to_output + "/final_output.mp4"
    cmd6 = "ffmpeg   -loglevel 0 -hide_banner -y -i " + state.path_to_output + "/tmp.mp4 -codec:v libx264 -crf 21 -bf 2 -flags +cgop -pix_fmt yuv420p -codec:a aac " + \
        "-strict -2 -b:a 348k -r:a 48000 -movflags faststart " + output_path
    subprocess.call(cmd6, shell=True)

    print "Done processing."
    print output_path
