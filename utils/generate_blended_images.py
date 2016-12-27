"""  This script helps smooth out consecutive ffmpeg input frames.

""" 

from os import listdir
from os.path import isfile, join
import subprocess

imgPath = '' 		   # this is the dir that contains source images
outputPath = ''        # this is the dir we're dumping copies + blended images into

imgFiles = [ f for f in listdir(imgPath) if isfile(join(imgPath,f)) and f[-3:] == 'jpg' ]


def copyImageToOutput(srcImg):
	subprocess.call("cp %s %s/" % (srcImg, outputPath), shell=True)

iterImgs = iter(imgFiles)
for currentImg in iterImgs:
	try:
		# if the iterator will let us, grab the next file (and advance the iterator pointer)
		nextImg = next(iterImgs)
		copyImageToOutput(nextImg)
		# use imagemagick to composite the two images and dump the result into the output dir
		subprocess.call("composite -dissolve 50 -gravity South %s %s %s/%s_blended.jpg" % (currentImg, nextImg, outputPath, currentImg), shell=True)
	except StopIteration, e:
		# the iterator tried to get the 'next' image WHEN THERE WAS NO SUCH IMAGE
		# lol
		print 'hit the last image..'
		pass

	# dump the current image to the output dir
	copyImageToOutput(currentImg)