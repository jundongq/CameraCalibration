import cv2
import os
import sys
import time

###
usage:
	python frameExtractory.py videofile sample_frequecy
###





def frameExtractor(videofile, sample_frequency):
	# Read video file
	vidcap = cv2.VideoCapture(videofile)

	"""
	Obtaining the video info
	"""
	if vidcap.isOpened():
		print "The imported file is readable."
		
	else:
		print "could not open the input file"

		print "converting MP4 file..."
		os.system('ffmpeg -i %s -c:v copy %s_Converted.mp4' %(videofile, videofile[:-4]))
		vidcap = cv2.VideoCapture('%s_Converted.MP4' % videofile[:-4])	

	length = int(vidcap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
	width  = int(vidcap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
	height = int(vidcap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
	fps    = vidcap.get(cv2.cv.CV_CAP_PROP_FPS)

	print 'The fps of the file is: ', fps

	"""
	Reading the video and saving it into images
	"""
	data_dir = '%s' %videofile[:-4]
	if not os.path.exists(data_dir):
	  os.makedirs(data_dir)

	count = 0
	while True:

		print count

		grabbed,image = vidcap.read()

		if not grabbed:

			print 'Failed to grab the frame'
			break

		print 'Read a new frame: grabbed!'
		count += 1
		if count%sample_frequency == 0:
			cv2.imwrite(os.path.join(data_dir, "%05d.png" % count), image)


#####################
###### Running ######
#####################
if __name__ == "__main__":
	print '~~~ Loading .MP4 file...'
	videofile = sys.argv[1]
	sample_frequency = sys.argv[2]
	
	vidcap = cv2.VideoCapture(videofile, sample_frequency)
	
	if vidcap.isOpened():
		print "The imported file is readable."

		t0 = time.time()
		frameExtractor(videofile)
		t1 = time.time()

		t = t1 - t0
		print "The process took %.2f mins." %(round(t/60., 2))

	else:
		print "Could not open the input file"

		print "Converting MP4 file..."
		os.system('ffmpeg -i %s -c:v copy %s_Converted.mp4' %(videofile, videofile[:-4]))
		vidcap = cv2.VideoCapture('%s_Converted.MP4' % videofile[:-4])	

		print 'Conversion Completed!'
		videofile_converted = '%s_Converted.MP4' % videofile[:-4]
		t0 = time.time()
		frameExtractor(videofile_converted)
		t1 = time.time()

		t = t1 - t0
		print "The process took %.2f mins." %(round(t/60., 2))
	
