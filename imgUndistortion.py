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
import sys
import time
import argparse

"""
Usage: ImgUndistortion.py -cp yourCameraMatrixfile -f yourImageFolder
"""

def img_undistort(camera_calibration, dirname):

	print '-----Loading Calibration Data: cameraMatrix, distCoeffs.....'
	calibrationData = np.load(camera_calibration)
	distCoeffs   = calibrationData['distCoeffs']
	cameraMatrix = calibrationData['cameraMatrix']
	# close the file handle
	calibrationData.close()

	# grab all images 
	images = glob.glob(dirname + '/sampledFrames/*.png')
	print len(images)
	# loop through all the available images, to save object points and image points of the corners
	print "-----Image undistortion in process...."

	# making a new directory to strore undistorted images
	dirname = dirname + '/Undistorted'
	if not os.path.exists(dirname):
		os.mkdir(dirname)

	for i, fname in enumerate(images):
		img = cv2.imread(fname)
		h,  w = img.shape[:2]
		# print h, w
		newcameramtx, roi=cv2.getOptimalNewCameraMatrix(cameraMatrix,distCoeffs,(w,h),1.,(w,h))
		# print newcameramtx
		# print roi
		
		# undistort the image
		# undistorted_img = cv2.undistort(img, cameraMatrix, distCoeffs, None)
		undistorted_img = cv2.undistort(img, cameraMatrix, distCoeffs, newcameramtx)
		'''The function transforms an image to compensate radial and tangential lens distortion. Those pixels in the destination image, for which there is no correspondent pixels in the source image, are filled with zeros (black color).'''
		
		# crop the image
		x,y,w,h = roi
		if x!= 0:
		
			undistorted_img = undistorted_img[y:y+h, x:x+w]
		
		# save the undistorted image to the new diretory
		cv2.imwrite(os.path.join(dirname,'Undistorted_%05d.png' %i), undistorted_img)
		#cv2.imshow('Undistorted Image %s' % fname, undistorted_img)
		#cv2.waitKey(500)
	#cv2.destroyAllWindows()

	print '-----Undistortion Completed!'

#####################
###### Running ######
#####################
if __name__ == "__main__":

	print '~~~~ Grabbing img files...'
	ap = argparse.ArgumentParser()
	ap.add_augment('-cp', '--cam_paras', required=True, help='a .npz file containing camera calibration data')
	ap.add_agument('-f', '--folder_name', required=True, help='a fold containing all .png files that need to be undistorted')
	args = vars(ap.parse_args())
	
	cam_ = args['cam_paras']
	dir_ = args['folder_name']

	t0 = time.time()

	img_undistort(cam_, dir_)

	t1 = time.time()

	t = t1 - t0
	print "The process took %.2f mins." %(round(t/60., 2))
