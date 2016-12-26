from PIL import Image
import numpy, cv2

# Load up the first and second demo images
image1 = Image.open("demo3_1.jpg")
image2 = Image.open("demo3_2.jpg")

# Grab the stats from image1 to use for the resultant video
height, width, layers =  numpy.array(image1).shape

# Create the OpenCV VideoWriter
video = cv2.VideoWriter("demo3_4.avi", # Filename
                        -1, # Negative 1 denotes manual codec selection. You can make this automatic by defining the "fourcc codec" with "cv2.VideoWriter_fourcc"
                        10, # 10 frames per second is chosen as a demo, 30FPS and 60FPS is more typical for a YouTube video
                        (width,height) # The width and height come from the stats of image1
                        )

# We'll have 30 frames be the animated transition from image1 to image2. At 10FPS, this is a whole 3 seconds
for i in xrange(0,30):
    images1And2 = Image.blend(image1, image2, i/30.0)

    # Conversion from PIL to OpenCV from: http://blog.extramaster.net/2015/07/python-converting-from-pil-to-opencv-2.html
    video.write(cv2.cvtColor(numpy.array(images1And2), cv2.COLOR_RGB2BGR))

# And back from image2 to image1...
for i in xrange(0,30):
    images2and1 = Image.blend(image2, image1, i/30.0)
    video.write(cv2.cvtColor(numpy.array(images2and1), cv2.COLOR_RGB2BGR))

# Release the video for it to be committed to a file
video.release()
