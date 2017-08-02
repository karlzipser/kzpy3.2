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



P[ICONS] = [Graph_Module.Icon(x,0, y,0, width,100, height,100, name,'Icon1', img,None, number,1)]
P[X_PIXEL_SIZE_INIT],P[Y_PIXEL_SIZE_INIT] = P[X_PIXEL_SIZE],P[Y_PIXEL_SIZE]

while True:

	
	lv,ov = temp_get_files(P[TEMP_RUN_NUMBER])
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
		#cv2.destroyAllWindows()
		#mci(P[IMAGE2][img],title=steer)
		#cv2.moveWindow(steer,P[SCREEN_X],P[SCREEN_Y])







		#P[IMAGE2][img] *= 0
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
#			screen_xv_init,screen_yv_init = P[SCREEN_X],P[SCREEN_Y]
#			yminv_init,ymaxv_init,P[X_PIXEL_SIZE_INIT],P[Y_PIXEL_SIZE_INIT] = yminv,ymaxv,P[X_PIXEL_SIZE],P[Y_PIXEL_SIZE]
#			screen_xv_init,screen_yv_init = P[SCREEN_X],P[SCREEN_Y]

			I[kv] = Graph_Module.Image2(
				xsize,P[X_PIXEL_SIZE],
				ysize,P[Y_PIXEL_SIZE],
				xmin,P[START_TIME],
				xmax,P[END_TIME],
				ymin,yminv,
				ymax,ymaxv,
				Img,P[IMAGE2])
			P[IMAGE3] = I[kv]
			I[kv][ptsplot](x,tsv, y,valsv, color,P[TOPICS][kv][color])
		if np.abs(P[MOUSE_Y]-P[Y_PIXEL_SIZE]/2) > 100:
			ref_xv = int(P[VERTICAL_LINE_PROPORTION]*P[X_PIXEL_SIZE])
			P[MOUSE_IN_RED_ZONE] = False
		else:
			ref_xv = P[MOUSE_X]
			P[MOUSE_IN_RED_ZONE] = True
			cv2.line(
				I[kv][img],
				(P[MOUSE_X],0),
				(P[MOUSE_X],P[Y_PIXEL_SIZE]),
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
			(P[SCREEN_X]-200,30),
			cv2.FONT_HERSHEY_SIMPLEX,
			0.75,(255,0,0),1)
		cv2.line(
			I[kv][img],
			(int(P[VERTICAL_LINE_PROPORTION]*P[X_PIXEL_SIZE]),0),
			(int(P[VERTICAL_LINE_PROPORTION]*P[X_PIXEL_SIZE]),P[Y_PIXEL_SIZE]),
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
		I[kv][img][(P[X_PIXEL_SIZE]-4*shape(camera_imgv)[0]):,(P[Y_PIXEL_SIZE]-4*shape(camera_imgv)[1]):,:] = cv2.resize(camera_imgv, (0,0), fx=4, fy=4)
		keyv = mci(P[IMAGE2][img],color_mode=cv2.COLOR_RGB2BGR,delay=33,title=kv)

		if img_index_timerv.check():
			display_ratev = max(img_index_listv)-min(img_index_listv)
			img_index_listv = []
			img_index_timerv.reset()

		#mci(O[left_image][vals][img_indexv][:],
		#	title=left_image,scale=4)
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

		if keyv == ord('0'):
			P[TEMP_RUN_NUMBER]=0;print 0;break
		elif keyv == ord('1'):
			P[TEMP_RUN_NUMBER]=1;print 1;break
		elif keyv == ord('2'):
			P[TEMP_RUN_NUMBER]=2;print 2;break

		for mv in P[CV2_KEY_COMMANDS]:
			if len(mv) > 0:
				if keyv == ord(mv):
					if P[MOUSE_IN_RED_ZONE]:
						mouse_red_zone_warning_timerv = Timer(1)
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
		
		if P[ICONS][0][clicked]:
			P[ICONS][0][clicked] = False
			P[TEMP_RUN_NUMBER] += 1
			if P[TEMP_RUN_NUMBER] > 2:
				P[TEMP_RUN_NUMBER] = 0
			break
		






#EOF