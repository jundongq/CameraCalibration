'''
This program is used to extract frames from videos.

Jundong Qiao, Univerisity at Buffalo, 09/15/2016

The version of modules:
opencv 2.4.8

References:
1. OpenCV documentation
'''

import cv2
import os

# load the video
vidcap = cv2.VideoCapture('ImgSamples/C0009.MP4')
'''obtaining the video info'''

if not vidcap.isOpened(): 
    print '-----Could not open the input video!'

print '-----Converting the video into readable format......'
os.system('ffmpeg -i ImgSamples/C0009.MP4 -c:v copy ImgSamples/C0009_Converted.mp4')
print '-----Video convertion completed!'
print '-----Loading the converted video......'
vidcap = cv2.VideoCapture('ImgSamples/C0009_Converted.MP4')	

length = int(vidcap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
width  = int(vidcap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
height = int(vidcap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
fps    = vidcap.get(cv2.cv.CV_CAP_PROP_FPS)

print '-----The fps of the file is: ', fps

#success,image = vidcap.read()
'''Reading the video and saving it into images'''
#success = True
count = 0
while True:
  success,image = vidcap.read()
  print 'Read a new frame: ', success
  count += 1
  # make a new directory to store the extracted frames from the video
  dirname = 'ImgSamples/ResolvedRawImgs'
  if not os.path.exists(dirname):
  	os.mkdir(dirname)
  
  # save the undistorted image to the new diretory
  cv2.imwrite(os.path.join(dirname,'RawImg_%05d.png' %count), image)

print '-----Frame Extration Done!'