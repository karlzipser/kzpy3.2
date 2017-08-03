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
"""

	Put in baseline
	Put in second markers, both absolute and relative to verticle line
	Put in multiple runs
		-- write name on Graph_Module
		-- allow selection with mouse

"""
_ = dictionary_access

for a in Args.keys():
	_(P,a,equals,_(Args,a))

#cv2.destroyAllWindows()
#mci(P[IMAGE2][img],title=steer)
#cv2.moveWindow(steer,P[SCREEN_X],P[SCREEN_Y])
P[X_PIXEL_SIZE_INIT],P[Y_PIXEL_SIZE_INIT] = P[X_PIXEL_SIZE],P[Y_PIXEL_SIZE]
##################3
P[ICONS] = {}

P[DATASET_PATH] = opjD('bdd_car_data_July2017_LCR')
P[H5PY_RUNS] = sggo(P[DATASET_PATH],'h5py','*')

for iv in rlen(P[H5PY_RUNS]):
	O = h5r(opj(P[H5PY_RUNS][iv],'original_timestamp_data.h5py'))
	icon_imgv = O[left_image][vals][int(len(O[left_image][vals])/2)][:]
	icon_imgv = cv2.resize(icon_imgv, (0,0), fx=0.5, fy=0.5)
	namev = fname(P[H5PY_RUNS][iv])
	P[ICONS][namev] = Graph_Module.Icon(
						y,int(10+1.1*iv*shape(icon_imgv)[1]),
						x,0.52*P[Y_PIXEL_SIZE],
						img,icon_imgv,
						Img,None,
						path,P[H5PY_RUNS][iv],
						name,namev)
P[CURRENT_ICON_NAME] = namev



while True:

	run_namev = P[ICONS][P[CURRENT_ICON_NAME]][name]
	lv = opj(P[ICONS][P[CURRENT_ICON_NAME]][path],'left_timestamp_metadata.h5py')
	ov = opj(P[ICONS][P[CURRENT_ICON_NAME]][path],'original_timestamp_data.h5py')
	L = h5r(lv)
	O = h5r(ov)
	tsv = L[ts][:]
	tsv = tsv.copy()
	tsv -= tsv[0]
	Timestamp_to_left_image = {}
	for iv in rlen(tsv):
		Timestamp_to_left_image[tsv[iv]] = iv
	P[END_TIME] =  max(tsv)
	P[START_TIME] = 0
	P[START_TIME_INIT],P[END_TIME_INIT] = P[START_TIME],P[END_TIME]

	I = {}

	zero_baselinev = 0*tsv
	baseline_with_ticsv = zero_baselinev.copy()
	for i in rlen(baseline_with_ticsv):
		if np.mod(int(tsv[i]),10.0) == 0:
			baseline_with_ticsv[i] = 1.0

	mouse_red_zone_warning_timerv = Timer(0)
	show_menuv = True
	first_timev = True
	img_index_timerv = Timer(1)
	img_index_listv = []
	display_ratev = 0

	while True:

		P[IMAGE2] = Graph_Module.Image2(
			xmin,P[START_TIME],
			xmax,P[END_TIME],
			ymin,-1,
			ymax,100,
			xsize,P[X_PIXEL_SIZE],
			ysize,P[Y_PIXEL_SIZE])
		for nv in P[ICONS]:
			P[ICONS][nv][Img] = P[IMAGE2]
			P[ICONS][nv][show]()
		ctrv = 0
		for kv in sorted(P[TOPICS].keys()):
			valsv = L[kv][:]
			if P[TOPICS][kv][minval] == minval:
				yminv = min(valsv)
			else:
				yminv = P[TOPICS][kv][minval]
			if P[TOPICS][kv][maxval] == maxval:
				ymaxv = max(valsv)
			else:
				ymaxv = P[TOPICS][kv][maxval]
			dyv = (ymaxv - yminv)
			yminv = ymaxv - dyv*(len(P[TOPICS].keys())+1)
			ymaxv += dyv*ctrv
			ctrv += 1
			yminv_init,ymaxv_init, = yminv,ymaxv

			I[kv] = Graph_Module.Image2(
				xsize,P[X_PIXEL_SIZE],
				ysize,P[Y_PIXEL_SIZE],
				xmin,P[START_TIME],
				xmax,P[END_TIME],
				ymin,yminv,
				ymax,ymaxv,
				Img,P[IMAGE2])
			P[IMAGE3] = I[kv]
			if kv == 'acc_y':
				baseline_valsv = baseline_with_ticsv + P[TOPICS][kv][baseline]
				baseline_colorv = (255,255,255)
			else:
				baseline_valsv = zero_baselinev + P[TOPICS][kv][baseline]
				baseline_colorv = (64,64,64)
			#for i in rlen(baseline_valsv):
			#	if np.mod(tsv[i],10) == 0:
			#		baseline_valsv[i] = 1
			I[kv][ptsplot](x,tsv, y,baseline_valsv, color,baseline_colorv)
			I[kv][ptsplot](x,tsv, y,valsv, color,P[TOPICS][kv][color])
		if np.abs(P[MOUSE_Y]-P[Y_PIXEL_SIZE]*0.4) > 100:
			ref_xv = int(P[VERTICAL_LINE_PROPORTION]*P[X_PIXEL_SIZE])
			P[MOUSE_IN_RED_ZONE] = False
		else:
			ref_xv = P[MOUSE_X]
			P[MOUSE_IN_RED_ZONE] = True
			cv2.line(
				I[kv][img],
				(P[MOUSE_X],0),
				(P[MOUSE_X],int(P[Y_PIXEL_SIZE]/2)),
				(255,0,0))
		time_from_pixelv = I[kv][pixel_to_float](xint,ref_xv, yint,0)[0]
		ts_from_pixelv = find_nearest(tsv,time_from_pixelv)
		cv2.putText(
			I[kv][img],
			d2n(dp(ts_from_pixelv,3),'s'),
			(10,30),
			cv2.FONT_HERSHEY_SIMPLEX,
			0.75,(255,0,0),1)
		cv2.putText(
			I[kv][img],
			d2n(dp(display_ratev/30.0,1),'X'),
			(10,90),
			cv2.FONT_HERSHEY_SIMPLEX,
			0.75,(255,0,0),1)
		cv2.line(
			I[kv][img],
			(int(P[VERTICAL_LINE_PROPORTION]*P[X_PIXEL_SIZE]),0),
			(int(P[VERTICAL_LINE_PROPORTION]*P[X_PIXEL_SIZE]),int(P[Y_PIXEL_SIZE]/2)),
			(0,0,255))
		if not mouse_red_zone_warning_timerv.check():
			cv2.putText(
				I[kv][img],
				"Mouse in red zone, cannot use key commands",
				(200,200),
				cv2.FONT_HERSHEY_SIMPLEX,
				2.0,(255,255,255),4)
		img_indexv = Timestamp_to_left_image[ts_from_pixelv]
		img_index_listv.append(img_indexv)
		camera_imgv = O[left_image][vals][img_indexv][:]
		cxv = (P[Y_PIXEL_SIZE]-P[CAMERA_SCALE]*shape(camera_imgv)[0])
		cyv = (P[X_PIXEL_SIZE]-P[CAMERA_SCALE]*shape(camera_imgv)[1])
		I[kv][img][cxv:,cyv:,:] = cv2.resize(camera_imgv, (0,0), fx=4, fy=4)
		cv2.putText(
			I[kv][img],
			run_namev,
			(cyv+10,cxv-10),
			cv2.FONT_HERSHEY_SIMPLEX,
			0.75,(255,255,255),1)
		for nv in P[ICONS]:
			if nv == P[CURRENT_ICON_NAME]:
				iconv = P[ICONS][nv]
				cv2.rectangle(I[kv][img],(iconv[y],iconv[x]),(iconv[y]+iconv[height],iconv[x]+iconv[width]), (200,200,200), 3)
				break
		#####################################################################
		#
		keyv = mci(P[IMAGE2][img],color_mode=cv2.COLOR_RGB2BGR,delay=33,title=kv)
		#
		#####################################################################

		if img_index_timerv.check():
			display_ratev = max(img_index_listv)-min(img_index_listv)
			img_index_listv = []
			img_index_timerv.reset()

		if first_timev:
			first_timev = False
			cv2.setMouseCallback(kv,Graph_Module.mouse_event)

		dtv = (P[START_TIME]-P[END_TIME])*0.001

		dvalv = (ymaxv-yminv)*0.001
		dxpixelsv = max(1,P[X_PIXEL_SIZE]*0.1)
		dypixelsv = max(1,P[Y_PIXEL_SIZE]*0.1)

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
					if P[MOUSE_IN_RED_ZONE]:
						mouse_red_zone_warning_timerv = Timer(2)
					else:
						cmd_tuplev = P[CV2_KEY_COMMANDS][mv]
						exec(cmd_tuplev[0])
					key_decodedv = True
		if not key_decodedv:
			if keyv != -1:
				try:
					print(d2s('keyv =',keyv))
					print(d2s(str(unichr(keyv)), '=',keyv))
				except Exception as e:
					print("********** Exception ***********************")
					print(e.message, e.args)
		
		#################################

		clickedv = False
		for nv in P[ICONS]:
			iconv = P[ICONS][nv]
			if iconv[clicked]:
				P[CURRENT_ICON_NAME] = iconv[name]
				iconv[clicked] = False
				clickedv = True
				P[VERTICAL_LINE_PROPORTION]=0.5
				P[START_TIME],P[END_TIME] = P[START_TIME_INIT],P[END_TIME_INIT]
				yminv,ymaxv = yminv_init,ymaxv_init
				show_menuv = True
		if clickedv:
			clickedv = False
			break



#EOF