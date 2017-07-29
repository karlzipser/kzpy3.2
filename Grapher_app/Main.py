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
import Graph_Module
exec(identify_file_str)

_ = dictionary_access

for a in Args.keys():
    _(P,a,equals,_(Args,a)) #P[a] = Args[a]








if False:
	imgv=imread('/home/karlzipser/Desktop/cameras.png' )

	I = Graph_Module.Image(xmin,-2,xmax,2, ymin,0,ymax,7, xsize,400,ysize,400)
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

	xLv,yLv = get_key_sorted_elements_of_dic(o['left_image'])
	xLv = np.array(xLv)
	yLv = np.array(yLv)
	xLv -= xLv[0]
	ySv = np.interp(xLv,xv,yv)

	imgv = zeros((500,2500,3),np.uint8)
	I = Graph_Module.Image2(xmin,0, xmax,300, ymin,-1, ymax,100, xsize,1800,ysize,200)
	while I[xmax] < xv.max():
		I[xmin]+=170/1000.
		I[xmax]+=170/1000.
		I[img] *= 0
		indiciesv = np.where(np.logical_and(xv>=I[xmin], xv<I[xmax]))
		xsv = xv[indiciesv]
		ysv = yv[indiciesv]
		baselinev = ysv*0.0+49
		I[ptsplot](x,xsv,y,baselinev,color,(0,0,255))
		I[ptsplot](x,xsv,y,baselinev,color,(0,0,255))
		I[ptsplot](x,xsv,y,ysv,color,(0,255,0))
		imgv[:200,:1800,:] = I[img]
		imgv[300:500,700:2500,:] = I[img]
		mci(imgv,color_mode=cv2.COLOR_RGB2BGR,delay=17)
		#mci(I[img],color_mode=cv2.COLOR_RGB2BGR,delay=17)


#EOF