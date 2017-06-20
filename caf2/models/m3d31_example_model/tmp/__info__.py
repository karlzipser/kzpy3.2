
CAFFE_MODE = 'train'
CAFFE_TRAIN_DATA = opjD('RPi3_data/all_runs_dics/runs_scale_50_BW')
CAFFE_TEST_DATA = opjD('RPi3_data/all_runs_dics/runs_scale_50_BW') # note, no separate test data at this moment.
CAFFE_FRAME_RANGE = (-15,-6)
USE_REVERSE_CONTRAST = True
USE_BOTTOM_HALF = True
USE_NOISE = True
USE_JITTER = True
jitter = 6
input_size = (1,9,56-jitter,150-jitter)

