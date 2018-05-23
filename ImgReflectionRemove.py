import numpy as np
import glob
import cv2
import sys
import os
import csv
import time
import argparse

def enhanceContrast(img):
	""" input as BGR space img, output as enhanced RGB img """

	image  = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


	# converting RGB to LAB color space
	lab_img = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
	L, A, B = cv2.split(lab_img)

	# apply CLAHE to L-channel
	clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
	cl_img = clahe.apply(L)

	# convert 1-channel to 3-channel
	cl_img = cv2.cvtColor(cl_img, cv2.COLOR_GRAY2RGB)

	return cl_img

def removeGlare(img, satThreshold = 180, glareThreshold=240):
	"""This function is used to remove light reflection on water surface during experiments,
	it return a np.ndarray() in shape of (height, width, channel).
	credit: http://www.amphident.de/en/blog/preprocessing-for-automatic-pattern-identification-in-wildlife-removing-glare.html
	input: image 
	output: clean image"""

	image     = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
	h, s, v   = cv2.split(hsv_image)

	# return 1/0, 1 indicates satuation <180, 0 indicates satuation >180, which do not need to be inpainted.
	# so nonSat serves as a mask, find all pixels that are not very saturated
	# all non saturated pixels need to be set as 1 (non-zero), which will be inpainted
	nonSat = s < satThreshold

	# Slightly decrease the area of the non-satuared pixels by a erosion operation.
	# return a kernel with designated shape, using erosion to minorly change the mask
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
	nonSat = cv2.erode(nonSat.astype(np.uint8), kernel)

	# Set all brightness values, where the pixels are still saturated to 0.
	# Only non-zero pixels in the mask need to be inpainted. So the saturated pixels set as 0 (no need to inpaint)
	v2 = v.copy()

	# set all saturated pixels, which do not need to be inpainted as 0
	v2[nonSat == 0] = 0

	#  glare as a mask filter out very bright pixels.
	glare = v2 > glareThreshold
	# Slightly increase the area for each pixel
	glare = cv2.dilate(glare.astype(np.uint8), kernel)
	glare = cv2.dilate(glare.astype(np.uint8), kernel)

	clean_image = cv2.inpaint(image, glare, 3, cv2.INPAINT_TELEA)

	return clean_image

def reflectionRemove(folder_name):

	# grab all images 
	# folder_name = 'FishBehavior_101817_4_Converted'
	images = glob.glob(folder_name+'/Undistorted/*.png')

	# loop through all the available images, to save object points and image points of the corners
	
	print "-----Preprocessing images for PTV analysis in process...."

	dirname = folder_name + '/UndistortedPreprocessed'
	if not os.path.exists(dirname):
		os.mkdir(dirname)

	for i, fname in enumerate(images):

		img = cv2.imread(fname)
		img = removeGlare(img)
		img = enhanceContrast(img)
		
		# save the undistorted image to the new diretory
		cv2.imwrite(os.path.join(dirname,'preprocessStreams_%05d.png' %i), img)
	# 	cv2.imshow('UndistortedPreprocessed %s' % fname, img)
	# 	cv2.waitKey(500)
	# 	cv2.destroyAllWindows()

	print '-----Preprocessing Completed!'


###### Run ######

if __name__ == "__main__":
	print '~~~ Loading Undistorted Images ...'
	ap = argparse.ArgumentParser()
	ap.add_argument('-f', '--file', required=True, help='folder name in which images need to be adjusted by removing light refelction')
	args = vars(ap.parse_args())
	
	folder_name = args['file']

	t0 = time.time()
	reflectionRemove(folder_name)
	t1 = time.time()

	t = t1 - t0
	print "The process took %.2f mins." %(round(t/60., 2))

