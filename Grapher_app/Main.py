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
		xv,yv = D[floats_to_pixels](x,xv,y,yv)
		for j in range(len(xv)):
			try: I[img][xv[j],yv[j],:] = [255,0,0]
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


if True:
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



if False:
	o=lo('/home/karlzipser/Desktop/bair_car_data_Main_Dataset/meta/furtive_24Aug2016_Tilden/preprocessed_data.pkl' )
	xv,yv = get_key_sorted_elements_of_dic(o['steer'])
	xv = np.array(xv)
	xv -= xv[0]
	I=Image2(xmin,0, xmax,100, ymin,-10, ymax,110, xsize,3000,ysize,1000)


	for j in range(0,100000,1):
		xl = []
		yl = []
		for i in range(len(xv)):

			if xv[i] > 0 + j:
				if xv[i] < 100:
					xl.append(xv[i])
					yl.append(yv[i])
		print len(xl)
		I[img] *=0
		I[pts_plot](x,xl,y,yl)
		mci(I[img],color_mode=cv2.COLOR_RGB2BGR,delay=16)

raw_input()

#EOF