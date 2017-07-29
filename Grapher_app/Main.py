###############################
#  for interactive terminal
import __main__ as main
if not hasattr(main,'__file__'):
	from kzpy3.utils2 import *
	pythonpaths(['kzpy3','kzpy3/Grapher_app','kzpy3/teg9'])
#
###############################
from Parameters_Module import *
from kzpy3.vis2 import *
exec(identify_file_str)

_ = dictionary_access

for a in Args.keys():
    _(P,a,equals,_(Args,a)) #P[a] = Args[a]




def Image2(*args):
	Args = args_to_dictionary(args)
	D = {}
	D[xmin] = Args[xmin] 
	D[xmax] = Args[xmax]
	D[ymin] = Args[ymin]
	D[ymax] = Args[ymax]
	D[xsize] = Args[xsize]
	D[ysize] = Args[ysize]
	if data_type in Args:
		D[data_type] = Args[data_type]
	else:
		D[data_type] = np.uint8
	True
	D[dic_type] = inspect.stack()[0][3]
	D[purpose] = d2s(D[dic_type],':','An image which translates from float coordinates.')
	D[xscale] = D[xsize]/(1.0*D[xmax]-D[xmin])
	D[yscale] = D[ysize]/(1.0*D[ymax]-D[ymin])
	D[img] = zeros((D[ysize],D[xsize],3),D[data_type]) #!!!
	def _function_floats_to_pixels(*args):
		Args = args_to_dictionary(args)
		xv = array(Args[x])
		yv = array(Args[y])
		xintv = ((xv-D[xmin])*D[xscale]).astype(np.int64)
		yintv = ((yv-D[ymin])*D[yscale]).astype(np.int64)
		return D[ysize]-yintv,xintv #!!!
	D[floats_to_pixels] = _function_floats_to_pixels
	def _function_pixels_to_floats(*args):
		Args = args_to_dictionary(args)
		return 'not implemented'
	D[pixels_to_floats] = _function_pixels_to_floats
	def _function_pts_plot(*args):
		Args = args_to_dictionary(args)
		xv,yv,colorv = Args[x],Args[y],Args[color]
		True
		D[xscale] = D[xsize]/(1.0*D[xmax]-D[xmin])
		D[yscale] = D[ysize]/(1.0*D[ymax]-D[ymin])
		xv,yv = D[floats_to_pixels](x,xv,y,yv)
		I[img][xv,yv,:] = colorv
		"""
		for j in range(len(xv)):
			#try:
			I[img][xv[j],yv[j],:] = colorv
			#except: pass
		"""
	D[pts_plot] = _function_pts_plot
	def _function_lines_plot(*args):
		Args = args_to_dictionary(args)
		xv,yv = Args[x],Args[y]
		True
		xv,yv = D[floats_to_pixels](x,xv,y,yv)
		for j in range(len(xv)-1):
			try: cv2.line(I[img],(yv[j],xv[j]),(yv[j+1],xv[j+1]),(255)) # reversing x and y because of the way images are shown.
			except: pass
	D[lines_plot] = _function_lines_plot
	def _apply_fun(f):
		for x in range(0,2*D['origin']):
			for y in range(0,2*D['origin']):
				xy_float = D['pixel_to_float']((x,y))
				D['img'][x][y] = f(xy_float[0],xy_float[1])      
				D['apply_fun'] = _apply_fun
	def _show(name=None):
		if name == None:
			name = D['name']
			mi(D['img'],name)
			#prin(t d2s('name =',name))
	D['show'] = _show
	def _clear():
		D['img'] *= 0.0
	return D


if False:
	imgv=imread('/home/karlzipser/Desktop/cameras.png' )

	I=Image2(xmin,-2,xmax,2, ymin,0,ymax,7, xsize,400,ysize,400)
	i = 0
	while i < 100:
		I[img] *= 0
		I[img][:400,:400,:] = imgv[:400,:400,:3].copy()
		yrv = arange(0,7,0.06)
		xrv = np.sin(yrv+i)
		I[lines_plot](x,xrv,y,yrv)
		mci(I[img],color_mode=cv2.COLOR_RGB2BGR,delay=16)
		i += 0.06



if True:
	#o=lo('/home/karlzipser/Desktop/bair_car_data_Main_Dataset/meta/furtive_24Aug2016_Tilden/preprocessed_data.pkl' )
	o=lo('/home/karlzipser/Desktop/bdd_car_data_July2017_LCR/meta/direct_local_LCR_10Jul17_09h36m15s_Mr_Yellow/preprocessed_data.pkl')
	xv,yv = get_key_sorted_elements_of_dic(o['steer'])
	xv = np.array(xv)
	yv = np.array(yv)
	xv -= xv[0]

	I=Image2(xmin,0, xmax,300, ymin,-1, ymax,100, xsize,1800,ysize,200)
	while I[xmax] < xv.max():
		I[xmin]+=170/1000.
		I[xmax]+=170/1000.
		I[img] *= 0
		indiciesv = np.where(np.logical_and(xv>=I[xmin], xv<I[xmax]))
		xsv = xv[indiciesv]
		ysv = yv[indiciesv]
		baselinev = ysv*0.0+49
		I[pts_plot](x,xsv,y,baselinev,color,(0,0,255))
		#I[pts_plot](x,xsv,y,baselinev,color,(0,0,255))
		I[pts_plot](x,xsv,y,ysv,color,(0,255,0))
		mci(I[img],color_mode=cv2.COLOR_RGB2BGR,delay=17)

#raw_input()

"""
# https://stackoverflow.com/questions/13869173/numpy-find-elements-within-range
a = np.array([1, 3, 5, 6, 9, 10, 14, 15, 56])
np.where(np.logical_and(a>=6, a<=10))
"""



def _Image2(*args):
	Args = args_to_dictionary(args)
	D = {}
	D[xmin] = Args[xmin] 
	D[xmax] = Args[xmax]
	D[ymin] = Args[ymin]
	D[ymax] = Args[ymax]
	D[xsize] = Args[xsize]
	D[ysize] = Args[ysize]
	if data_type in Args:
		D[data_type] = Args[data_type]
	else:
		D[data_type] = np.uint8
	True
	D[dic_type] = inspect.stack()[0][3]
	D[purpose] = d2s(D[dic_type],':','An image which translates from float coordinates.')
	D[xscale] = D[xsize]/(1.0*D[xmax]-D[xmin])
	D[yscale] = D[ysize]/(1.0*D[ymax]-D[ymin])
	D[img] = zeros((D[xsize],D[ysize],3),D[data_type])
	def _function_floats_to_pixels(*args):
		Args = args_to_dictionary(args)
		xv = array(Args[x])
		yv = array(Args[y])
		xintv = ((xv-D[xmin])*D[xscale]).astype(np.int64)
		yintv = ((yv-D[ymin])*D[yscale]).astype(np.int64)
		return xintv,yintv
	D[floats_to_pixels] = _function_floats_to_pixels
	def _function_pixels_to_floats(*args):
		Args = args_to_dictionary(args)
		return 'not implemented'
	D[pixels_to_floats] = _function_pixels_to_floats
	def _function_pts_plot(*args):
		Args = args_to_dictionary(args)
		xv,yv = Args[x],Args[y]
		True
		D[xscale] = D[xsize]/(1.0*D[xmax]-D[xmin])
		D[yscale] = D[ysize]/(1.0*D[ymax]-D[ymin])
		xv,yv = D[floats_to_pixels](x,xv,y,yv)
		for j in range(len(xv)):
			try:
				I[img][xv[j],yv[j],:] = [255,0,0]
			except: pass
	D[pts_plot] = _function_pts_plot
	def _function_lines_plot(*args):
		Args = args_to_dictionary(args)
		xv,yv = Args[x],Args[y]
		True
		xv,yv = D[floats_to_pixels](x,xv,y,yv)
		for j in range(len(xv)-1):
			try: cv2.line(I[img],(yv[j],xv[j]),(yv[j+1],xv[j+1]),(255)) # reversing x and y because of the way images are shown.
			except: pass
	D[lines_plot] = _function_lines_plot
	def _apply_fun(f):
		for x in range(0,2*D['origin']):
			for y in range(0,2*D['origin']):
				xy_float = D['pixel_to_float']((x,y))
				D['img'][x][y] = f(xy_float[0],xy_float[1])      
				D['apply_fun'] = _apply_fun
	def _show(name=None):
		if name == None:
			name = D['name']
			mi(D['img'],name)
			#prin(t d2s('name =',name))
	D['show'] = _show
	def _clear():
		D['img'] *= 0.0
	return D
#EOF