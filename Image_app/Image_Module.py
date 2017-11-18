from kzpy3.utils2 import *
CODE_PATH__ = opjh('kzpy3/Image_app')
pythonpaths([opjh('kzpy3'),opjh(CODE_PATH__)])
from Parameters_Module import *
from vis2 import *
exec(identify_file_str)



def Img(xmin=None,xmax=None,ymin=None,ymax=None,xsize=None,ysize=None,data_type=np.uint8,img=None):
	"""
	Note, because of the way image display is different from plotting display,
	there is a confusing switching of x and y in certain places.
	"""
	_ = {}
	_[XMIN] = xmin
	_[XMAX] = xmax
	_[YMIN] = ymin
	_[YMAX] = ymax
	_[DATA_TYPE] = data_type
	_[XSIZE] = xsize
	_[YSIZE] = ysize
	if img != None:
		_[IMG] = img
		_[XSIZE] = shape(img)[1]
		_[YSIZE] = shape(img)[0]
	else:
		_[IMG] = zeros((_[YSIZE],_[XSIZE],3),_[DATA_TYPE]) #!!!

	_[XSCALE] = _[XSIZE]/(1.0*_[XMAX]-_[XMIN])
	_[YSCALE] = _[YSIZE]/(1.0*_[YMAX]-_[YMIN])
	
	def _function_floats_to_pixels(x_=None,y_=None,no_reverse=True):
		x_ = na(x_)
		y_ = na(y_)
		xint = ((x_ -_[XMIN])*_[XSCALE]).astype(np.int64)
		yint = ((y_ -_[YMIN])*_[YSCALE]).astype(np.int64)
		if no_reverse:
			return xint,yint
		else:
			return _[YSIZE]-yint,xint
	_[FLOATS_TO_PIXELS] = _function_floats_to_pixels
	def _function_pixel_to_float(xint_=None,yint_=None):
		x_ = xint_ / (1.0*_[xsize]) * (_[xmax]-_[xmin]) + _[xmin]
		y_ = (_[ysize]-yint_) / (1.0*_[ysize]) * (_[ymax]-_[ymin]) + _[ymin]
		return x_,y_
	_[PIXEL_TO_FLOAT] = _function_pixel_to_float
	def _function_pts_plot(x_=None,y_=None,color_=(255,0,0),no_reverse=True):
		_[XSCALE] = _[XSIZE]/(1.0*_[XMAX]-_[XMIN])
		_[YSCALE] = _[YSIZE]/(1.0*_[YMAX]-_[YMIN])
		x_,y_ = _[FLOATS_TO_PIXELS](x_=x_,y_=y_,no_reverse=no_reverse)
		indicies_ = np.where(np.logical_and(y_>=0, y_<_[XSIZE]))
		x_ = x_[indicies_]
		y_ = y_[indicies_]        
		indicies_ = np.where(np.logical_and(x_>=0, x_<_[YSIZE]))
		# Note confusing reversals of x and y above and in this module
		x_ = x_[indicies_]
		y_ = y_[indicies_]    
		_[IMG][x_,y_,:] = color_
	_[PTS_PLOT] = _function_pts_plot
	return _





"""
def mouse_event(event, x_, y_, buttons, user_param):
	P[MOUSE_X] = x_
	P[MOUSE_Y] = y_
	if event == cv2.EVENT_MOUSEMOVE:
		P[MOUSE_MOVE_TIME] = time.time()
	elif event == cv2.EVENT_LBUTTONDOWN:
		#if y_ < P[Y_MOUSE_RANGE_PROPORTION] * P[Y_PIXEL_SIZE]:
		_do_center_time('center_time',_(P,IMAGE3,pixel_to_float)(xint,x_, yint,0)[0])
		for nv in P[ICONS].keys():
			P[ICONS][nv][check](x,x_, y,y_)


def _do_center_time(*args):
	Args = args_to_dictionary(args)
	center_timev = Args['center_time']
	True
	time_width_ = P[END_TIME] - P[START_TIME]
	P[START_TIME] = center_timev - time_width_/2
	P[END_TIME] = center_timev + time_width_/2







def Icon(*args):
	Args = args_to_dictionary(args)
	_ = {}
	_[x] = int(Args[x])
	_[y] = int(Args[y])
	_[img] = Args[img]
	_[path] = Args[path]
	_[Img] = Args[Img]
	_[name] = Args[name]
	True
	_[width] = shape(_[img])[0]
	_[height] = shape(_[img])[1]
	_[click_time] = False
	_[clicked] = False
	def _function_check(*args):
		Args = args_to_dictionary(args)
		x_ = Args[y]
		y_ = Args[x]
		#pd2s('checking',_[name],(x_,y_),'vs',(_[x],_[y]))
		True
		if x_ >= _[x]:
			if x_ <= _[x]+_[width]:
				if y_ >= _[y]:
					if y_ <= _[y]+_[height]:
						_[click_time] = time.time()
						_[clicked] = True
						print(_[name]+ ' clicked')
	def _function_show():
		True
		_[Img][img][_[x]:_[x]+_[width],_[y]:_[y]+_[height],:] = _[img]
	_[check] = _function_check
	_[show] = _function_show
	return _

"""
True


























#EOF
