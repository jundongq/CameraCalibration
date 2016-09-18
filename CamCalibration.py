'''
This program is used to calibrate the Sony RX10II camera, which is employed for fish tracking
& instantaneous velocity measurements for physical modeling of my PhD work.

Jundong Qiao, Univerisity at Buffalo, 09/13/2016

The version of modules:
numpy 1.11.0
opencv 2.4.8

References:
1. OpenCV documentation:
http://docs.opencv.org/2.4.8/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html#calibratecamera
http://docs.opencv.org/trunk/
http://docs.opencv.org/trunk/dc/dbb/tutorial_py_calibration.html
2. Chapter 11, Learning OpenCV, Gary Bradski and Adrian Kaehler (2008)
'''

import numpy as np
import cv2
import glob

# checking the version of modules
print "Numpy Version is:", np.__version__
print "OpenCV Version is:", cv2.__version__

# define the number of squares on the chess board (width and height)
s_w = 9
s_h = 6
# so the pattern of corners is
patternSize = (s_w, s_h)
# the window size for refining the coordinates of corners
windowSize = (11, 11)

# Termination criteria for the iterative process of looking for subpixel corner
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
'''Here 30 means the maximum number of iterations, 0.001 means the subpixel accuracy is 1/1000 of a pixel, which is the desired accuracy in parameters at which the iterative algorithm stops. '''

# initialize matrices for storing the physical coordinates of points on each image
objp = np.zeros((s_h*s_w,3), dtype=np.float32)
objp[:,:2] = np.mgrid[0:s_w, 0:s_h].T.reshape(-1,2)
'''In the case of a chessboard, for example, you might define the coordinates such that all of the points on the chessboard had a z-value of 0 '''
'''while the x- and y-coordinates are measured in centimeters.In the simplest case, we simply define each square of the chessboard to be of dimension one "unit" '''
'''so that the coordinates of the corners on the chessboard are just integer corner rows and columns. objp is in shape of (x, y, z) = (s_w-1, s_h-1, 0)'''

# create empty to store object points and image points from all images 3d points in real word space
objpoints = [] 
'''The returned objpoints is in shape of (#imgs, #objpoints, 3). This is a list of lists. For each img, there is a set of objpoints. Each of the objpoints contains 3 coordinate values, which consistes of a list.'''

imgpoints = [] 
'''The returned imgpoints contained 2d points in image plane, which is a list of lists (#imgs, #corners, 1, 2). One example of coordinates of a corner [[450, 550]], in shape of (1, 2), which means, the list contains 1 element, and this element is a list. This contained list contains 2 elements, which are the coordinates of the one corner'''

# grab all images 
images = glob.glob('ImgSamples/120/*.png')

# loop through all the available images, to save object points and image points of the corners
print "-----Corner refining in process...."	
for fname in images:
	img = cv2.imread(fname)
	
	# convert the image into grayscale
	gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	retval, corners = cv2.findChessboardCorners(gray_img, patternSize)
	'''retval: the type of returned value, True or False
	Number of inner corners per a chessboard row and column 
	( patternSize = cvSize(points_per_row,points_per_colum) = cvSize(columns,rows) )'''
	
	if retval == True:
		print 'Looping through image %s' % fname
		# save the object points in one image into the list objpoints
		objpoints.append(objp)

		# refine the corner coordinates
		cv2.cornerSubPix(gray_img, corners, windowSize, (-1, -1), criteria)
		'''@parameter corners inside of cv2.cornerSubPix() are InputOutputArray, 
		which is modified in place inside of the function'''
		
		# store the refined corner coordinates in imgpoints
		imgpoints.append(corners)

		# draw and display the corners
        cv2.drawChessboardCorners(img, patternSize, corners, retval)
        '''@parameter img is InputOutputArray, which is modified inside of the function
        @parameter retval is a boolean, which indicates whether patter was found or not'''
        
        cv2.imshow('ChessBoard Image %s' % fname,img)
        cv2.waitKey(500)

cv2.destroyAllWindows()
		
print "-----Camera calibration in process...."	

ret, cameraMatrix, distCoeffs, revcs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray_img.shape[::-1], None, None)
'''calibrateCamera returns the root mean square (RMS) re-projection error, usually it should be between 0.1 and 1.0 pixels in a good calibration.
The calculation is done by projecting the 3D chessboard points (objectPoints) into the image plane using the final set of calibration parameters (cameraMatrix, distCoeffs, rvecs and tvecs) and comparing the known position of the corners (imagePoints).

An RMS error of 1.0 means that, on average, each of these projected points is 1.0 px away from its actual position. The error is not bounded in [0, 1], it can be considered as a distance.

Reference: http://stackoverflow.com/questions/29628445/meaning-of-the-retval-return-value-in-cv2-calibratecamera

@parameters cameraMatrix, distCoeffs, revcs, tvecs are all InputOutputArrays
@parameter gray_img.shape[::-1] returns image size'''

print ret
print cameraMatrix
print distCoeffs

print '-----Saving the calibration results into a binary file...'

np.savez('calibration_data', RMS = ret, distCoeffs=distCoeffs, cameraMatrix=cameraMatrix)

if ret<=1.0:
	print '-----Calibration Done! The results are AWSOME!'
else:
	print '-----Calibration Done! It might need more work to improve the accuracy!'