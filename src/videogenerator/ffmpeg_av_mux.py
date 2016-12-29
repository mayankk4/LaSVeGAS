
import subprocess

def AvMux(path_to_audio, path_to_silent_video, output_path):
    print "Muxing the audio with the silent video. Output at:"
    print output_path
    cmd = "ffmpeg -y -i " + path_to_audio + " -r 30 -i " + path_to_silent_video + " -filter:a aresample=async=1 -c:a flac -c:v copy " + output_path
    subprocess.call(cmd, shell=True)
