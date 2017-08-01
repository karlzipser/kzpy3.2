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
from Car_Data_app.Names_Module import *
exec(identify_file_str)

_ = dictionary_access

for a in Args.keys():
    _(P,a,equals,_(Args,a)) #P[a] = Args[a]


cv2.destroyAllWindows()
P[VERTICAL_LINE_PROPORTION]
dproportv = 1/1000.0
P[START_TIME] = P[START_TIME]

xpixelsv = P[X_PIXEL_SIZE]
ypixelsv = P[Y_PIXEL_SIZE]
screen_xv = P[SCREEN_X]
screen_yv = P[SCREEN_Y]

def mouse_event(event, x, y, buttons, user_param):
	if event == cv2.EVENT_LBUTTONDOWN:
		P[MOUSE_X] = x
		P[MOUSE_Y] = y
		do_center_time('center_time',I[pixel_to_float](xint,x, yint,0)[0])


def do_center_time(*args):
	Args = args_to_dictionary(args)
	center_timev = Args['center_time']
	time_widthv = P[END_TIME] - P[START_TIME]
	P[START_TIME] = center_timev - time_widthv/2
	P[END_TIME] = center_timev + time_widthv/2


if da(P,EXAMPLE5):
	L = h5r(opjD('bdd_car_data_July2017_LCR/h5py/direct_local_LCR_29Jul17_18h09m32s_Mr_Yellow/left_timestamp_metadata.h5py'))
	O = h5r(opjD('bdd_car_data_July2017_LCR/h5py/direct_local_LCR_29Jul17_18h09m32s_Mr_Yellow/original_timestamp_data.h5py'))
	

	t0v = L[ts][0]
	tsv = L[ts]
	tsv -= tsv[0]
	Timestamp_to_left_image = {}
	for iv in rlen(tsv):
		Timestamp_to_left_image[tsv[iv]] = iv
	
	P[END_TIME] =  max(tsv)


	for kv in P[TOPICS].keys():
		print(kv)
		valsv = L[kv][:]
		if P[TOPICS][kv][minval] == minval:
			yminv = min(valsv)
		else:
			yminv = P[TOPICS][kv][minval]
		if P[TOPICS][kv][maxval] == maxval:
			ymaxv = max(valsv)
		else:
			ymaxv = P[TOPICS][kv][maxval]


		P[START_TIME_INIT],P[END_TIME_INIT],yminv_init,ymaxv_init,xpixelsv_init,ypixelsv_init = P[START_TIME],P[END_TIME],yminv,ymaxv,xpixelsv,ypixelsv
		screen_xv_init,screen_yv_init = screen_xv,screen_yv
		show_menuv = True
		first_timev = True
		while True:
			I = Graph_Module.Image2(xmin,P[START_TIME], xmax,P[END_TIME], ymin,yminv, ymax,ymaxv, xsize,xpixelsv,ysize,ypixelsv)
			I[ptsplot](x,tsv,y,valsv,color,(0,255,0))
			time_from_pixelv = I[pixel_to_float](xint,int(P[VERTICAL_LINE_PROPORTION]*xpixelsv), yint,0)[0]
			ts_from_pixelv = find_nearest(tsv,time_from_pixelv)
			assert(ts_from_pixelv in tsv) #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			cv2.putText(I[img],d2s(dp(ts_from_pixelv,3)),(10,30),cv2.FONT_HERSHEY_SIMPLEX,1.0,(255,0,0),4)
			cv2.line(I[img],(int(P[VERTICAL_LINE_PROPORTION]*xpixelsv),0),(int(P[VERTICAL_LINE_PROPORTION]*xpixelsv),ypixelsv),(0,0,255))
			keyv = mci(I[img],color_mode=cv2.COLOR_RGB2BGR,delay=33,title=kv)
			mci(O[left_image][vals][Timestamp_to_left_image[ts_from_pixelv]][:],title=left_image,scale=4)
			if first_timev:
				first_timev = False
				cv2.moveWindow(kv,screen_xv,screen_yv)
				cv2.setMouseCallback(kv,mouse_event)
			dtv = (P[START_TIME]-P[END_TIME])*0.001
			dvalv = (ymaxv-yminv)*0.001
			dxpixelsv = max(1,xpixelsv*0.1)
			dypixelsv = max(1,ypixelsv*0.1)

			if show_menuv:
				show_menuv = False
				print('Key command menu')
				for lv in P[CV2_KEY_COMMANDS]:
					print_lv = lv
					if len(lv) == 0 or lv == ' ':
						print_lv = "\'"+lv+"\'"
					print(d2s('\t',print_lv,'-',P[CV2_KEY_COMMANDS][lv][1]))
					
			key_decodedv = False

			for mv in P[CV2_KEY_COMMANDS]:
				if len(mv) > 0:
					if keyv == ord(mv):
						cmd_tuplev = P[CV2_KEY_COMMANDS][mv]
						exec(cmd_tuplev[0])
						#print(cmd_tuplev[1])
						key_decodedv = True

			if not key_decodedv:
				if keyv != -1:
					print(d2s(str(unichr(keyv)), '=',keyv))






























if da(P,EXAMPLE1):
	limgv=imread('/home/karlzipser/Desktop/cameras.png' )
	#o=lo('/home/karlzipser/Desktop/bair_car_data_Main_Dataset/meta/furtive_24Aug2016_Tilden/preprocessed_data.pkl' )
	ov=lo('/home/karlzipser/Desktop/bdd_car_data_July2017_LCR/meta/direct_local_LCR_10Jul17_09h36m15s_Mr_Yellow/preprocessed_data.pkl')
	xv,yv = get_key_sorted_elements_of_dic(ov['steer'])
	xv = np.array(xv)
	yv = np.array(yv)
	xv -= xv[0]

	xLv,yLv = get_key_sorted_elements_of_dic(ov['left_image'])
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
		I[img][:200,:200,:] = limgv[:200,:200,:3].copy()
		indiciesv = np.where(np.logical_and(xv>=I[xmin], xv<I[xmax]))
		xsv = xv[indiciesv]
		ysv = yv[indiciesv]
		baselinev = ysv*0.0+49
		I[ptsplot](x,xsv,y,baselinev,color,(0,0,255))
		#I[ptsplot](x,xsv,y,baselinev,color,(0,0,255))
		I[ptsplot](x,xsv,y,ysv,color,(0,255,0))
		imgv[:200,:1800,:] = I[img]
		imgv[300:500,700:2500,:] = I[img]
		mci(imgv,color_mode=cv2.COLOR_RGB2BGR,delay=17)
		#mci(I[img],color_mode=cv2.COLOR_RGB2BGR,delay=17)



if da(P,EXAMPLE2):
	ov=lo('/home/karlzipser/Desktop/bdd_car_data_July2017_LCR/meta/direct_local_LCR_10Jul17_09h36m15s_Mr_Yellow/preprocessed_data.pkl')
	xv,yv = get_key_sorted_elements_of_dic(ov['encoder'])
	xv = np.array(xv)
	yv = np.array(yv)
	ymv = np.array(meo(yv,200))
	xv -= xv[0]
	I = Graph_Module.Image2(xmin,xv.min()-100, xmax,xv.max()+100, ymin,-1, ymax,10, xsize,6000,ysize,800)
	baselinev = yv*0.0
	for iv in rlen(xv):
		if np.mod(int(xv[iv]),10) == 0:
			baselinev[iv] = 1
	I[ptsplot](x,xv,y,baselinev,color,(0,0,255))
	I[ptsplot](x,xv, y,ymv, color,(255,0,0))
	I[ptsplot](x,xv, y,yv, color,(0,255,0))
	mci(I[img],color_mode=cv2.COLOR_RGB2BGR,delay=1)
	wk(1000000)




if da(P,EXAMPLE3):
	#ov=lo('/media/karlzipser/ExtraDrive2/bdd_car_data_July2017_LCR/meta/direct_Tilden_LCR_12Jul17_09h41m48s_Mr_Yellow/preprocessed_data.pkl')
	#ov=lo('/media/karlzipser/ExtraDrive2/bdd_car_data_July2017_LCR/meta/direct_local_LCR_12Jul17_20h20m26s_Mr_Yellow/preprocessed_data.pkl')
	#ov=lo('/media/karlzipser/ExtraDrive2/bdd_car_data_July2017_LCR/meta/direct_home_LCR_25Jul17_20h04m40s_Mr_Yellow/preprocessed_data.pkl')
	ov=lo('/media/karlzipser/ExtraDrive2/bdd_car_data_July2017_LCR/meta/direct_home_LCR_25Jul17_19h37m22s_Mr_Yellow/preprocessed_data.pkl')
	xv,yv = get_key_sorted_elements_of_dic(ov['gyro'])
	xv = np.array(xv)
	yv = np.array(yv)
	yv=yv[:,1]
	
	ymv = np.array(meo(yv,200))
	xv -= xv[0]
	I = Graph_Module.Image2(xmin,xv.min()-100, xmax,xv.max()+100, ymin,-500, ymax,500, xsize,3000,ysize,2000)
	baselinev = yv*0.0
	for iv in rlen(xv):
		if np.mod(int(xv[iv]),10) == 0:
			baselinev[iv] = 1
	I[ptsplot](x,xv,y,baselinev,color,(0,0,255))
	I[ptsplot](x,xv, y,yv, color,(0,255,0))
	I[ptsplot](x,xv, y,ymv, color,(255,0,0))
	mci(I[img],color_mode=cv2.COLOR_RGB2BGR,delay=1)
	wk(1000000)

	if False:
		vv = []
		for iv in range(100,81000):
			vv.append(np.std(yv[iv-50:iv+50]))
		plot(vv)


if da(P,EXAMPLE4):

	ov=lo('/media/karlzipser/ExtraDrive2/bdd_car_data_July2017_LCR/meta/direct_home_LCR_25Jul17_19h37m22s_Mr_Yellow/preprocessed_data.pkl')
	xv,yv = get_key_sorted_elements_of_dic(ov['gyro'])
	xv = np.array(xv)
	yv = np.array(yv)
	yv=yv[:,1]
	
	ymv = np.array(meo(yv,200))
	xv -= xv[0]
	I = Graph_Module.Image2(xmin,xv.min()-100, xmax,xv.max()+100, ymin,-500, ymax,500, xsize,3000,ysize,2000)
	baselinev = yv*0.0
	for iv in rlen(xv):
		if np.mod(int(xv[iv]),10) == 0:
			baselinev[iv] = 1
	I[ptsplot](x,xv,y,baselinev,color,(0,0,255))
	I[ptsplot](x,xv, y,yv, color,(0,255,0))
	I[ptsplot](x,xv, y,ymv, color,(255,0,0))
	mci(I[img],color_mode=cv2.COLOR_RGB2BGR,delay=1)
	wk(1000000)

	if False:
		vv = []
		for iv in range(100,81000):
			vv.append(np.std(yv[iv-50:iv+50]))
		plot(vv)

#EOF