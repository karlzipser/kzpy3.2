from kzpy3.utils2 import *
CODE_PATH__ = opjh('kzpy3/Grapher_app')
pythonpaths([opjh('kzpy3'),opjh(CODE_PATH__)])
from Parameters_Module import *
from vis2 import *
exec(identify_file_str)

_ = dictionary_access

def Graph_Image(*args):
	"""
	Note, because of the way image display is different from plotting display,
	there is a confusing switching of x and y in certain places.
	"""
	Args = args_to_dictionary(args)
	D = {}
	for p_ in [xmin,xmax,ymin,ymax,xsize,ysize]:
		D[p_] = Args[p_]
	if data_type in Args:
		D[data_type] = Args[data_type]
	else:
		D[data_type] = np.uint8
	if Img in Args:
		D[img] = Args[Img][img]
	else:
		D[img] = zeros((D[ysize],D[xsize],3),D[data_type]) #!!!
	True
	D[dic_type] = inspect.stack()[0][3]
	D[purpose] = d2s(D[dic_type],':','An image which translates from float coordinates.')
	D[xscale] = D[xsize]/(1.0*D[xmax]-D[xmin])
	D[yscale] = D[ysize]/(1.0*D[ymax]-D[ymin])
	
	def _function_floats_to_pixels(*args):
		Args = args_to_dictionary(args)
		x_ = array(Args[x])
		y_ = array(Args[y])
		if NO_REVERSE in Args:
			no_reverse = Args[NO_REVERSE]
		else:
			no_reverse = False
		True
		xint_ = ((x_-D[xmin])*D[xscale]).astype(np.int64)
		yint_ = ((y_-D[ymin])*D[yscale]).astype(np.int64)
		if no_reverse:
			return xint_,yint_
		else:
			return D[ysize]-yint_,xint_
	D[floats_to_pixels] = _function_floats_to_pixels
	def _function_pixel_to_float(*args):
		Args = args_to_dictionary(args)
		xint_ = Args[xint]
		yint_ = Args[yint]
		x_ = xint_ / (1.0*D[xsize]) * (D[xmax]-D[xmin]) + D[xmin]
		y_ = (D[ysize]-yint_) / (1.0*D[ysize]) * (D[ymax]-D[ymin]) + D[ymin]

		return x_,y_
	D[pixel_to_float] = _function_pixel_to_float
	def _function_pts_plot(*args):
		Args = args_to_dictionary(args)
		x_,y_,color_ = Args[x],Args[y],Args[color]
		if NO_REVERSE in Args:
			no_reverse = Args[NO_REVERSE]
		else:
			no_reverse = False		
		True
		D[xscale] = D[xsize]/(1.0*D[xmax]-D[xmin])
		D[yscale] = D[ysize]/(1.0*D[ymax]-D[ymin])
		x_,y_ = D[floats_to_pixels](x,x_,y,y_,NO_REVERSE,no_reverse)
		indicies_ = np.where(np.logical_and(y_>=0, y_<D[xsize]))
		x_ = x_[indicies_]
		y_ = y_[indicies_]        
		indicies_ = np.where(np.logical_and(x_>=0, x_<D[ysize]))
		# Note confusing reversals of x and y above and in this module
		x_ = x_[indicies_]
		y_ = y_[indicies_]    
		D[img][x_,y_,:] = color_
	D[ptsplot] = _function_pts_plot
	return D

#EOF
