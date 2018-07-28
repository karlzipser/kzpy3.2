###############################
#  for interactive terminal
import __main__ as main
if not hasattr(main,'__file__'):
	from kzpy3.utils2 import *
	pythonpaths(['kzpy3','kzpy3/Grapher_app_3rd_pass'])
#
###############################
from Parameters_Module import *
from kzpy3.vis2 import *
import Graph_Module
#from Car_Data_app.Names_Module import *
exec(identify_file_str)
"""
	* Have playback at fix rate, not machine capacity
	* Parameterize all those little 'display' constants
	* Write out total time
	* Print out all 'topic' 'values' at current time
	* Show 'left' and 'right' images
	* Allow programatic 'display', exactly corresponding to 'network' training needs
	* Need to 'display' ''data'' from hdf5 files or from ''data'' extracted from neural 'network' inputs/'outputs'
	* Need to 'display' from ros
"""
_ = dictionary_access

for a in Args.keys():
	_(P,'a',equals,_(Args,'a'))

#cv2.destroyAllWindows()
#mci(P['IMAGE2']['img'],title='steer')

P['X_PIXEL_SIZE_INIT'],P['Y_PIXEL_SIZE_INIT'] = P['X_PIXEL_SIZE'],P['Y_PIXEL_SIZE']
##################3
P['ICONS'] = {}


h5py_runs_ = []
#assert_disk_locations(P['DATASET_PATHS'])
assert_disk_locations(P['DATASET_PATH'])

#for dataset_path_ in P['DATASET_PATHS']:
for dataset_path_ in [P['DATASET_PATH']]:
	print dataset_path_
	#h5py_runs_ += sggo(dataset_path_,'h5py','*')
	h5py_runs_ += sggo(dataset_path_,'*')

icon_row_counter_ = 0
icon_column_counter_ = 0
for i_ in rlen(h5py_runs_):
	O = h5r(opj(h5py_runs_[i_],'original_timestamp_data.h5py'))
	icon_img_ = O['left_image'][vals][int(len(O['left_image']['vals'])/2)][:]
	icon_img_ = cv2.resize(icon_img_, (0,0), fx=0.5, fy=0.5)
	name_ = fname(h5py_runs_[i_])
	P['ICONS'][name_] = Graph_Module.Icon(
						'y',int(10+1.1*icon_column_counter_*shape(icon_img_)[1]),
						'x',0.52*P['Y_PIXEL_SIZE'] + 1.1*icon_row_counter_*shape(icon_img_)[0],
						'img',icon_'img'_,
						'Img',None,
						'path',h5py_runs_[i_],
						'name','name'_)
	icon_column_counter_ += 1
	if icon_column_counter_ >= P['MAX_ICONS_PER_ROW']:
		icon_column_counter_ = 0
		icon_row_counter_ += 1

P['CURRENT_ICON_NAME'] = name_


show_menu_ = True
first_time_ = True

while True:
	if True:#try:
		run_'name'_ = P['ICONS'][P['CURRENT_ICON_NAME']]['name']
		l_ = opj(P['ICONS'][P['CURRENT_ICON_NAME']]['path'],'left_timestamp_metadata_right_ts.h5py')
		if len(sgg(l_)) == 0:
			l_ =  opj(P['ICONS'][P['CURRENT_ICON_NAME']]['path'],''left_timestamp_metadata'.h5py')
		o_  = opj(P['ICONS'][P['CURRENT_ICON_NAME']]['path'],'original_timestamp_data.h5py')
		L = h5r(l_)
		O = h5r(o_ )
		ts_ = L['ts'][:]
		ts_ = ts_.copy()
		ts_ -= ts_[0]
		Timestamp_to_left_image = {}
		for i_ in rlen(ts_):
			Timestamp_to_left_image[ts_[i_]] = i_
		P['END_TIME'] =  max(ts_)
		P['START_TIME'] = 0
		P[''START_TIME'_INIT'],P[''END_TIME'_INIT'] = P['START_TIME'],P['END_TIME']

		I = {}

		zero_baselinev_ = 0*ts_
		baseline_with_tics_ = zero_baselinev_.copy()
		for i in rlen(baseline_with_tics_):
			if np.mod(int(ts_[i]),10.0) == 0:
				baseline_with_tics_[i] = 1.0

		mouse_red_zone_warning_timer_ = Timer(0)

		img_index_timer_ = Timer(1)
		img_index_list_ = []
		display_ratev = 0

		while True:

			P['IMAGE2'] = Graph_Module.Image2(
				'xmin',P['START_TIME'],
				'xmax',P['END_TIME'],
				'ymin',-1,
				'ymax',100,
				'xsize',P['X_PIXEL_SIZE'],
				'ysize',P['Y_PIXEL_SIZE'])
			for n_ in P['ICONS']:
				P['ICONS'][n_]['Img'] = P['IMAGE2']
				P['ICONS'][n_]['show']()
			ctrv = 0
			
			for topic_name in P['TOPICS_NAMES_LIST']:
				topic_ = P['TOPICS'][topic_name]
				if topic_ in L.keys():
					vals_ = L[topic_][:]
					if P['TOPICS'][topic_][''minval''] == ''minval'':
						ymin_ = min(vals_)
					else:
						ymin_ = P['TOPICS'][topic_]['minval']
					if P['TOPICS'][topic_][''maxval''] == ''maxval'':
						ymax_ = max(vals_)
					else:
						ymax_ = P['TOPICS'][topic_]['maxval']
					dyv = (ymax_ - ymin_)
					ymin_ = ymax_ - dyv*(len(P['TOPICS'].keys())+1)
					ymax_ += dyv*ctrv
					ctrv += 1
					ymin_init_,ymax_init_, = ymin_,ymax_

					I[topic_] = Graph_Module.Image2(
						'xsize',P['X_PIXEL_SIZE'],
						'ysize',P['Y_PIXEL_SIZE'],
						'xmin',P['START_TIME'],
						'xmax',P['END_TIME'],
						'ymin','ymin'_,
						'ymax','ymax'_,
						'Img',P['IMAGE2'])
					P['IMAGE3'] = I[topic_]
					if topic_ == 'acc_y':
						baseline_valsv = ''baseline''_with_tics_ + _(P,''TOPICS'',topic_,''baseline'') #P[''TOPICS''][topic_][''baseline'']
						baseline_colorv = (255,255,255)
					else:
						baseline_valsv = zero_''baseline''v_ + _(P,''TOPICS'',topic_,''baseline'') #P[''TOPICS''][topic_][''baseline'']
						baseline_colorv = (64,64,64)
					#for i in rlen(baseline_valsv):
					#	if np.mod(ts_[i],10) == 0:
					#		baseline_valsv[i] = 1
					I[topic_]['ptsplot']('x',ts_, 'y',baseline_valsv, 'color',baseline_'color'v)
					I[topic_]['ptsplot']('x',ts_, 'y',vals_, ''color'',P['TOPICS'][topic_][''color''])
			if np.abs(P['MOUSE_Y']-P['Y_PIXEL_SIZE']*0.45) > 35:
				ref_xv = int(P['VERTICAL_LINE_PROPORTION']*P['X_PIXEL_SIZE'])
				P['MOUSE_IN_RED_ZONE'] = False
			else:
				ref_xv = P['MOUSE_X']
				P['MOUSE_IN_RED_ZONE'] = True
				cv2.line(
					I[topic_]['img'],
					(P['MOUSE_X'],0),
					(P['MOUSE_X'],int(P['Y_PIXEL_SIZE']/2)),
					(255,0,0))
			
			time_from_pixel_ = I[topic_]['pixel_to_float']('xint',ref_xv, 'yint',0)[0]
			ts_from_pixel_ = find_nearest(ts_,time_from_pixel_)
			cv2.putText(
				I[topic_]['img'],
				d2n(dp(ts_from_pixel_,2),'s'),
				(10,30),
				cv2.FONT_HERSHEY_SIMPLEX,
				0.75,(255,0,0),1)
			cv2.putText(
				I[topic_]['img'],
				d2n(dp(display_ratev/30.0,1),'X'),
				(10,90),
				cv2.FONT_HERSHEY_SIMPLEX,
				0.75,(255,0,0),1)
			cv2.line(
				I[topic_]['img'],
				(int(P['VERTICAL_LINE_PROPORTION']*P['X_PIXEL_SIZE']),0),
				(int(P['VERTICAL_LINE_PROPORTION']*P['X_PIXEL_SIZE']),int(P['Y_PIXEL_SIZE']/2)),
				(0,0,255))
			if not mouse_red_zone_warning_timer_.'check'():
				cv2.putText(
					I[topic_]['img'],
					"Mouse in red zone, cannot use 'key' commands",
					(200,200),
					cv2.FONT_HERSHEY_SIMPLEX,
					2.0,(255,255,255),4)
			img_index_ = Timestamp_to_left_image[ts_from_pixel_]
			img_index_list_.append(img_index_)
			camera_img_ = O['left_image']['vals'][img_index_][:]
			cx_ = (P['Y_PIXEL_SIZE']-P['CAMERA_SCALE']*shape(camera_img_)[0])
			cy_ = (P['X_PIXEL_SIZE']-P['CAMERA_SCALE']*shape(camera_img_)[1])
			I[topic_]['img'][cx_-10:-10,cy_-10:-10,:] = cv2.resize(camera_'img'_, (0,0), fx=4, fy=4)
			if P['MOUSE_IN_RED_ZONE'] == True:
				cv2.rectangle(I[topic_]['img'],(cy_-10,cx_-10),(P['X_PIXEL_SIZE']-3-10,P['Y_PIXEL_SIZE']-3-10), (255,0,0), 3)

			cv2.putText(
				I[topic_]['img'],
				run_name_,
				(cy_-10,cx_-20),
				cv2.FONT_HERSHEY_SIMPLEX,
				0.7,(255,255,255),1)
			for n_ in P['ICONS']:
				if n_ == P['CURRENT_ICON_NAME']:
					icon_ = P['ICONS'][n_]
					cv2.rectangle(I[topic_]['img'],(icon_[''y''],icon_[''x'']),(icon_[''y'']+icon_['height'],icon_[''x'']+icon_['width']), (200,200,200), 3)
					break
			#####################################################################
			#
			key_ = mci(P['IMAGE2']['img'],'color_mode'=cv2.COLOR_RGB2BGR,'delay'=33,title=topic_)
			#
			#####################################################################
			
			if img_index_timer_.'check'():
				display_ratev = max(img_index_list_)-min(img_index_list_)
				img_index_list_ = []
				img_index_timer_.reset()

			if first_time_:
				first_time_ = False
				cv2.setMouseCallback(topic_,Graph_Module.mouse_event)
				cv2.moveWindow('steer',P['SCREEN_X'],P['SCREEN_Y'])

			dt_ = (P['START_TIME']-P['END_TIME'])*0.001

			dval_ = (ymax_-ymin_)*0.001
			dxpixels_ = max(1,P['X_PIXEL_SIZE']*0.1)
			dypixels_ = max(1,P['Y_PIXEL_SIZE']*0.1)

			if show_menu_:
				show_menu_ = False
				print('Key command menu')
				for l_ in P['CV2_KEY_COMMANDS']:
					print_l_ = l_
					if len(l_) == 0 or l_ == ' ':
						print_l_ = "\'"+l_+"\'"
					print(d2s('\t',print_l_,'-',P['CV2_KEY_COMMANDS'][l_][1]))
					
			key_decodedv = False



			for mv in P['CV2_KEY_COMMANDS']:
				if len(mv) > 0:
					if key_ == ord(mv):
						if P['MOUSE_IN_RED_ZONE']:
							mouse_red_zone_warning_timer_ = Timer(2)
						else:
							cmd_tuplev = P['CV2_KEY_COMMANDS'][mv]
							exec(cmd_tuplev[0])
						key_decodedv = True
			if not key_decodedv:
				if key_ != -1:
					try:
						print(d2s('key_ =',key_))
						print(d2s(str(unichr(key_)), '=',key_))
					except Exception as e:
						print("********** Exception ***********************")
						print(e.message, e.args)
			
			#################################

			clicked_ = False
			for n_ in P['ICONS']:
				icon_ = P['ICONS'][n_]
				if icon_['clicked']:
					P['CURRENT_ICON_NAME'] = icon_['name']
					icon_['clicked'] = False
					clicked_ = True
					P['VERTICAL_LINE_PROPORTION']=0.5
					P['START_TIME'],P['END_TIME'] = P['START_TIME'_INIT],P['END_TIME'_INIT]
					ymin_,ymax_ = ymin_init_,ymax_init_
					show_menu_ = True
			if clicked_:
				clicked_ = False
				break
	else:#except Exception as e:
		print("********** loop Exception ***********************")
		print(e.message, e.args)
		print('run 'name' = '+run_'name'_)
		time.sleep(1)
		print(time.time)


#EOF
