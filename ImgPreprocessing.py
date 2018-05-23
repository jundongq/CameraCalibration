import frameExtractor as fE
import imgUndistortion as iU
import imgReflectionRemove as iR

import argparse
import os
import time

"""


"""

def main(videofile, sample_frequency, camera_calibration):
	
	# folder name for sampled frames
	data_dir = '%s' %videofile[:-4]
	print [data_dir]
	
	data_dir_spl = os.path.join(data_dir, 'sampledFrames')
	if not os.path.exists(data_dir_spl):
		print 'sampling frames ...'
		### sample frames from video clips
		fE.frameExtractor(videofile, sample_frequency)
	
	data_dir_undis = os.path.join(data_dir, 'Undistorted')
	if not os.path.exists(data_dir_undis):
		print 'undistorting frames ...'
		### undistort sampled frames
		iU.img_undistort(camera_calibration, data_dir)
	
	data_dir_rm = os.path.join(data_dir, 'UndistortedPreprocessed')
	if not os.path.exists(data_dir_rm):
		print 'removing glares ...'
		### remove light reflection from imgs
		iR.reflectionRemove(data_dir)
	

if __name__ == '__main__':
	
	ap = argparse.ArgumentParser()
	ap.add_argument('-v', '--video', required=True, help='filename of one video clip')
	ap.add_argument('-n', '--frequency', type=int, required=True, \
					help='sample frequency of the video frames')
	ap.add_argument('-cp', '--cam_paras', required=True, \
					help='a .npz file containing camera calibration data')
	
	args = vars(ap.parse_args())
	
	videofile = args['video']
	spl_frequency = args['frequency']
	cam_paras = args['cam_paras']
	
	t0 = time.time()
	main(videofile, spl_frequency, cam_paras)
	t1 = time.time()

	t = t1 - t0
	print "The whole preprocessing took %.2f mins." %(round(t/60., 2))
