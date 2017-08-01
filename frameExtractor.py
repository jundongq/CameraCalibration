'''
This program is used to extract frames from videos.

Jundong Qiao, Univerisity at Buffalo, 09/15/2016. Updataed on 08/01/2017

The version of modules:
opencv 2.4.8

References:
1. OpenCV documentation
'''

import cv2
import os
import sys


def frameExtractor(videofile):
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

  success,image = vidcap.read()
  count = 0
  success = True
  while success:
    success,image = vidcap.read()
    print 'Read a new frame: ', success
    print count
    cv2.imwrite(os.path.join(data_dir, "%05d.png" % count), image)    # save frame as png file
    count += 1

#####################
###### Running ######
#####################
if __name__ == "__main__":
	print '~~~ Loading .MP4 file...'
	videofile = sys.argv[1]
	frameExtractor(videofile)

print '-----Frame Extration Done!'
