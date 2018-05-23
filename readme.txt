This project is for calibrating the camera, before using it for PTV analysis.
The order of using the code is:

1. take a video of the checkerboard with the camera to be calibrated. The checkerboard image attached is from 'https://github.com/opencv/opencv/blob/master/doc/pattern.png'
2. use frameExtractor.py to resolve the videos into a sequence of images
3. use CamCalibration.py to return the camera matrix and distortion coefficients.
4. use imgUndistortion.py to apply the camera matrix and distortion coefficients to undistort the new images taken by the camera

###
5. After image distortion, use imgReflectionRemove.py to remove glares and to enhance image contrast.
6. ImgPreprocessing.py integrate frame extraction, image undistortion and glare removal processes together.
