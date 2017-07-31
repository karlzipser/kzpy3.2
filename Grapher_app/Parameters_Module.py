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
P[TOPICS] = {acc_x_meo:{maxval:maxval,minval:minval}}
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
	'l':("start_tv -= dtv; end_tv -= dtv","Time step forward"),
	'j':("start_tv += dtv; end_tv += dtv","Time step back"),
	'i':("start_tv += dtv; end_tv -= dtv","Time scale out"),
	'm':("start_tv -= dtv; end_tv += dtv","Time scale in"),
	'u':("ymaxv += dvalv","y max increase"),
	'n':("ymaxv -= dvalv","y max decrease"),
	'y':("yminv += dvalv","y min increase"),
	'b':("yminv -= dvalv","y min decrease"),
	't':("xpixelsv += dxpixelsv; xpixelsv=int(xpixelsv)","increase width"),
	'v':("xpixelsv -= dxpixelsv; xpixelsv=int(xpixelsv)","decrease width"),
	#'r':("xpixelsv += dxpixelsv; xpixelsv=int(xpixelsv)",""),
	#eeeeeee'c':("xpixelsv -= dxpixelsv; xpixelsv=int(xpixelsv)",""),
	'r':("ypixelsv += dypixelsv; ypixelsv=int(ypixelsv)","increase height"),
	'c':("ypixelsv -= dypixelsv; ypixelsv=int(ypixelsv)","decrease height"),
	' ':("start_tv,end_tv,yminv,ymaxv,xpixelsv,ypixelsv = start_tv_init,end_tv_init,yminv_init,ymaxv_init,xpixelsv_init,ypixelsv_init;show_menuv = True","Reset"),
	'a':("show_menuv = True","Menu"),
	'2':("screen_yv+=10;cv2.moveWindow(kv,screen_xv,screen_yv)","Move window down"),
	'8':("screen_yv-=10;cv2.moveWindow(kv,screen_xv,screen_yv)","Move window up"),
	'4':("screen_xv-=10;cv2.moveWindow(kv,screen_xv,screen_yv)","Move window left"),
	'6':("screen_xv+=10;cv2.moveWindow(kv,screen_xv,screen_yv)","Move window right"),


	'':("",""),
	'':("",""),
	'':("",""),
	'':("",""),
	'':("",""),
	'':("",""),
	'':("",""),
	'':("",""),
	'q':("sys.exit()","Quit"),
}

#EOF