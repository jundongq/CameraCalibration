'''
This program is used to undistor images from the Sony RX10II camera, which is employed for fish tracking
& instantaneous velocity measurements for physical modeling of my PhD work.

Jundong Qiao, Univerisity at Buffalo, 09/15/2016

The version of modules:
numpy 1.11.0
opencv 2.4.8

References:
1. OpenCV documentation:
http://docs.opencv.org/trunk/dc/dbb/tutorial_py_calibration.html
http://docs.opencv.org/2.4/modules/imgproc/doc/geometric_transformations.html
2. Chapter 11, Learning OpenCV, Gary Bradski and Adrian Kaehler (2008)
'''

import numpy as np
import cv2
import glob
import os

print '-----Loading Calibration Data: cameraMatrix, distCoeffs.....'


calibrationData = np.load('calibration_data.npz')

distCoeffs   = calibrationData['distCoeffs']
cameraMatrix = calibrationData['cameraMatrix']

# close the file handle
calibrationData.close()

# grab all images 
images = glob.glob('ImgSamples/120/*.png')

# loop through all the available images, to save object points and image points of the corners
print "-----Image undistortion in process...."

for i, fname in enumerate(images):
	img = cv2.imread(fname)
	# undistort the image
	undistorted_img = cv2.undistort(img, cameraMatrix, distCoeffs, None)
	'''The function transforms an image to compensate radial and tangential lens distortion. Those pixels in the destination image, for which there is no correspondent pixels in the source image, are filled with zeros (black color).'''
	
	# making a new directory to strore undistorted images
	dirname = 'ImgSamples/Undistorted'
	if not os.path.exists(dirname):
		os.mkdir(dirname)
	
	# save the undistorted image to the new diretory
	cv2.imwrite(os.path.join(dirname,'Undistorted_%05d.png' %i), undistorted_img)
	cv2.imshow('Undistorted Image %s' % fname, undistorted_img)
	cv2.waitKey(500)
cv2.destroyAllWindows()

print '-----Undistortion Completed!'