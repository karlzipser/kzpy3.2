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
P[TOPICS] = {steer:{maxval:100,minval:-1}}
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

	#'u':("ymaxv += dvalv","y max increase"),
	#'n':("ymaxv -= dvalv","y max decrease"),
	#'y':("yminv += dvalv","y min increase"),
	#'b':("yminv -= dvalv","y min decrease"),

	#'t':("xpixelsv += dxpixelsv; xpixelsv=int(xpixelsv)","increase width"),
	#'v':("xpixelsv -= dxpixelsv; xpixelsv=int(xpixelsv)","decrease width"),

	#'r':("ypixelsv += dypixelsv; ypixelsv=int(ypixelsv)","increase height"),
	#'c':("ypixelsv -= dypixelsv; ypixelsv=int(ypixelsv)","decrease height"),

	#'e':("P[VERTICAL_LINE_PROPORTION] += dproportv","increase vertical line proportion"),
	#qqqqqqqqqqqqqqq'x':("P[VERTICAL_LINE_PROPORTION] -= dproportv","decrease vertical line proportion"),

	' ':("P[VERTICAL_LINE_PROPORTION]=0.5;P[START_TIME],P[END_TIME],yminv,ymaxv,xpixelsv,ypixelsv = P[START_TIME_INIT],P[END_TIME_INIT],yminv_init,ymaxv_init,xpixelsv_init,ypixelsv_init;show_menuv = True","Reset"),
	'a':("show_menuv = True","Menu"),
	
	#'2':("screen_yv+=10;cv2.moveWindow(kv,screen_xv,screen_yv)","Move window down"),
	#'8':("screen_yv-=10;cv2.moveWindow(kv,screen_xv,screen_yv)","Move window up"),
	#'4':("screen_xv-=10;cv2.moveWindow(kv,screen_xv,screen_yv)","Move window left"),
	#'6':("screen_xv+=10;cv2.moveWindow(kv,screen_xv,screen_yv)","Move window right"),
	#'w':("print 'here';do_center_time(center_time, I[pixel_to_float](xint,int(P[VERTICAL_LINE_PROPORTION]*xpixelsv), yint,0)[0]);P[VERTICAL_LINE_PROPORTION]=0.5","Center on vertical line"),
	'q':("sys.exit()","Quit"),
}

#EOF