''' This is a way to generate a video from Images using OpenCV.

References:
OpenCV documentation:
http://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html
PyAudio:
http://people.csail.mit.edu/hubert/pyaudio/

Notes:
I have not been able to find a good way to add Audio along with the Images. One
solution is to separately generate a video using OpenCV and an audio track using
pyaudio and then use ffmpeg to mux them together. However, I could also use
ffmpeg directly if it allows us to do both in one shot. Benchmarkings should
make things clearer once both impls are available.

Benchmark results:
1fps  : 0.6s,    160KB  (no blending)
10 fps: 3.3s,    330KB  (no blending)
10 fps: 5.5s,    1.3 MB (3 second blend)
60 fps: 16.s,    1.6MB  (no blending)
60 fps: 31s,     4.9MB  (3 second blending)

'''

# todo(kmayank):
# Add flags for fps codec and other configs

from PIL import Image
import numpy
import cv2

FPS = 5
KEY_IMAGE_DURATION = 2
VALUE_IMAGE_DURATION = 3


def GenerateSilentVideo(key_image_path, value_image_path, output_path):
    print "Generating a silent video now."
    # Load up the first and second demo images
    keyImage = Image.open(key_image_path)
    valueImage = Image.open(value_image_path)

    # Grab the stats from image1 to use for the resultant video
    # We expect both the images to be of the same size.
    height, width, layers = numpy.array(keyImage).shape

    # Create the OpenCV VideoWriter
    video = cv2.VideoWriter(output_path,  # Filename
                            -1,  # codec
                            FPS,  # FPS
                            (width, height))

    # Write image1 - 2 seconds
    for i in xrange(0, FPS * KEY_IMAGE_DURATION):
        video.write(cv2.cvtColor(numpy.array(keyImage), cv2.COLOR_RGB2BGR))

    # Uncomment to add transition.
    # Transition - 3 second
    # for i in xrange(0,180):
    #     mergedImage = Image.blend(image1, image2, i/180.0) # NOTE: denominator needs float.
    #     video.write(cv2.cvtColor(numpy.array(mergedImage), cv2.COLOR_RGB2BGR))

    # Write image2 - 6 seconds
    for i in xrange(0, FPS * VALUE_IMAGE_DURATION):
        video.write(cv2.cvtColor(numpy.array(valueImage), cv2.COLOR_RGB2BGR))

    # Release the video for it to be committed to a file
    video.release()
