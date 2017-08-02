from Names_Module import *
exec(identify_file_str)

_ = dictionary_access

P = {}

_(P,VERBOSE,equals,True)
_(P,EXAMPLE1,equals,0)
_(P,EXAMPLE2,equals,0)
_(P,EXAMPLE3,equals,0)
_(P,EXAMPLE4,equals,0)

_(P,EXAMPLE5,equals,1)



P[START_TIME] = 0
#P[END_TIME] = maxval


P[TOPICS] = {
	steer:{maxval:120,minval:-1,color:(255,0,0)},
	motor:{maxval:70,minval:-1,color:(0,255-32,32)},
	state:{maxval:6,minval:-1,color:(128,128,128)},
	encoder:{maxval:4,minval:-1,color:(0,128,128)},
	acc_x:{maxval:10,minval:-10,color:(128,128,0)},
	acc_y:{maxval:10,minval:-10,color:(128-32,128+32,0)},
	acc_z:{maxval:10,minval:-10,color:(128-64,128+64,0)},
	gyro_x:{maxval:180,minval:-180,color:(128,128,0)},
	gyro_y:{maxval:180,minval:-180,color:(128-32,128+32,0)},
	gyro_z:{maxval:180,minval:-180,color:(128-64,128+64,0)},
	gyro_heading_x:{maxval:360,minval:-180,color:(255,200,200)},

	}
P[VERTICAL_LINE_PROPORTION] = 0.5

P[X_PIXEL_SIZE] = 2000
P[Y_PIXEL_SIZE] = 2000
P[SCREEN_X] = 1500
P[SCREEN_Y] = 150
P[MOUSE_MOVE_TIME] = 0
P[MOUSE_X] = 0
P[MOUSE_Y] = 0
P[REAL_TIME_DTV] = -2/30.

P[ICONS] = []
"""
	 u'acc_y_meo',
	 u'acc_z_meo',
	 u'encoder_meo',
	 u'gyro_heading_x_meo',
	 u'gyro_heading_y_meo',
	 u'gyro_heading_y_meo',
	 u'gyro_x_meo',
	 u'gyro_z_meo',
	 u'left_ts_deltas',
	 u'motor',
	 u'state',
	 u'steer',
	 #u'right_ts',
	 ]
"""


P[CV2_KEY_COMMANDS] = {
	'p':("P[START_TIME] -= P[REAL_TIME_DTV]; P[END_TIME] -= P[REAL_TIME_DTV]",
		"Time step forward,real time"),
	'm':("P[START_TIME] -= P[REAL_TIME_DTV]/2.0; P[END_TIME] -= P[REAL_TIME_DTV]/2.0",
		"Time step forward,real time"),
	'l':("P[START_TIME] -= dtv; P[END_TIME] -= dtv",
		"Time step forward"),
	'h':("P[START_TIME] += dtv; P[END_TIME] += dtv",
		"Time step back"),
	'u':("P[START_TIME] += P[REAL_TIME_DTV]; P[END_TIME] += P[REAL_TIME_DTV]",
		"Time step back, real time"),
	'v':("P[START_TIME] += P[REAL_TIME_DTV]/2.0; P[END_TIME] += P[REAL_TIME_DTV]/2.0",
		"Time step back, real time"),
	'j':("P[START_TIME] += 100.0*dtv; P[END_TIME] -= 100.0*dtv",
		"Time scale out"),
	'k':("P[START_TIME] -= 100.0*dtv; P[END_TIME] += 100.0*dtv",
		"Time scale in"),
	' ':("""
P[VERTICAL_LINE_PROPORTION]=0.5
P[START_TIME],P[END_TIME] = P[START_TIME_INIT],P[END_TIME_INIT]
yminv,ymaxv = yminv_init,ymaxv_init
show_menuv = True""",
		"Reset"),
	'a':("show_menuv = True","Menu"),



	'q':("sys.exit()","Quit"),
}

P[TEMP_RUN_NUMBER] = 0
P[DATASET_PATH] = opjD('bdd_car_data_July2017_LCR')
def temp_get_files(i):
	run_namev = ['direct_local_LCR_28Jul17_10h22m41s_Mr_Yellow',
		'direct_local_LCR_29Jul17_18h09m32s_Mr_Yellow',
		'direct_local_VAL_LCR_28Jul17_10h44m46s_Mr_Yellow'][i]
	run_pathv = opj(P[DATASET_PATH],'h5py',run_namev)

	return run_namev,opj(run_pathv,'left_timestamp_metadata.h5py'),opj(run_pathv,'original_timestamp_data.h5py')






#EOF