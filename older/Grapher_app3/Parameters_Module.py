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
P[END_TIME] = maxval
#P[TOPICS] = {acc_x_meo:{maxval:maxval,minval:minval}}
P[TOPICS] = {
#	steer:{maxval:100,minval:-1-500},
	motor:{maxval:100,minval:-1},
	}
P[VERTICAL_LINE_PROPORTION] = 0.5

P[X_PIXEL_SIZE] = 2000
P[Y_PIXEL_SIZE] = 500
P[SCREEN_X] = 1500
P[SCREEN_Y] = 50
P[MOUSE_MOVE_TIME] = 0
P[MOUSE_X] = 0
P[MOUSE_Y] = 0

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
	'l':("P[START_TIME] -= dtv; P[END_TIME] -= dtv","Time step forward"),
	'j':("P[START_TIME] += dtv; P[END_TIME] += dtv","Time step back"),
	'i':("P[START_TIME] += 100.0*dtv; P[END_TIME] -= 100.0*dtv","Time scale out"),
	'm':("P[START_TIME] -= 100.0*dtv; P[END_TIME] += 100.0*dtv","Time scale in"),
	' ':("""
P[VERTICAL_LINE_PROPORTION]=0.5
P[START_TIME],P[END_TIME] = P[START_TIME_INIT],P[END_TIME_INIT]
yminv,ymaxv,xpixelsv,ypixelsv = yminv_init,ymaxv_init,xpixelsv_init,ypixelsv_init
show_menuv = True""",
		"Reset"),
	'a':("show_menuv = True","Menu"),
	'q':("sys.exit()","Quit"),
}



P[L_FILE] = opjD('bdd_car_data_July2017_LCR/h5py/direct_local_LCR_29Jul17_18h09m32s_Mr_Yellow/left_timestamp_metadata.h5py')
P[O_FILE] = opjD('bdd_car_data_July2017_LCR/h5py/direct_local_LCR_29Jul17_18h09m32s_Mr_Yellow/original_timestamp_data.h5py')








#EOF