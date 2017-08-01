This project is for calibrating the camera, before using it for PTV analysis.
The order of using the code is:

1. take a video of the checkerboard with the camera to be calibrated.
2. use frameExtractor.py to resolve the videos into a sequence of images
3. use CamCalibration.py to return the camera matrix and distortion coefficients.
4. use imgUndistortion.py to apply the camera matrix and distortion coefficients to undistort the new images taken by the camera
