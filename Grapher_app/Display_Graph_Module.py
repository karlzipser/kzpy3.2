from Parameters_Module import *
from vis2 import *
import Graph_Image_Module
import kzpy3.data_analysis.Angle_Dict_Creator as Angle_Dict_Creator
exec(identify_file_str)

_ = dictionary_access



def Display_Graph(*args):
	Args = args_to_dictionary(args)
	D = {}
	D[topics] = Args[topics]
	True
	#print D[topics].keys()
	
	D[timestamp_to_left_image] = {}
	if left_image in D[topics]:
		ts_ = D[topics][left_image][ts][:]
	else:
		ts_ = D[topics][acc_x][ts][:]
	for i_ in rlen(ts_):
		D[timestamp_to_left_image][ts_[i_]] = i_
	D[end_time] = max(ts_)
	D[start_time] = D[end_time]-60#min(ts_)
	D[reference_time] = (D[start_time]+D[end_time])/2.0
	D[start_time_init],D[end_time_init] = D[start_time],D[end_time]
	D[base_graph] = Graph_Image_Module.Graph_Image(
		xmin,D[start_time],
		xmax,D[end_time],
		ymin,-1,
		ymax,100,
		xsize,P[X_PIXEL_SIZE],
		ysize,P[Y_PIXEL_SIZE])
	#D[zero_baseline] = 0*ts_
	#D[baseline_with_tics] = D[zero_baseline].copy()
	#for i in rlen(D[baseline_with_tics]):
	#	if np.mod(int(ts_[i]),10.0) == 0:
	#		D[baseline_with_tics][i] = 1.0

	def _function_vertical_line(*args):
		Args = args_to_dictionary(args)
		vertical_line_proportion_ = Args[vertical_line_proportion]
		color_ = Args[color]
		True
		cv2.line(
			D[base_graph][img],
			(int(vertical_line_proportion_*P[X_PIXEL_SIZE]),0),
			(int(vertical_line_proportion_*P[X_PIXEL_SIZE]),int(P[Y_PIXEL_SIZE]/2)),
			color_)
	D[vertical_line] = _function_vertical_line

	def _function_insert_camera_image(*args):
		Args = args_to_dictionary(args)
		camera_ = Args[camera]
		img_index_ = Args[img_index]
		True
		if False:
			camera_img_ = camera_[img_index_][:]
			cx_ = (P[Y_PIXEL_SIZE]-P[CAMERA_SCALE]*shape(camera_img_)[0])
			cy_ = (P[X_PIXEL_SIZE]-P[CAMERA_SCALE]*shape(camera_img_)[1])
			D[base_graph][img][cx_-10:-10,cy_-10:-10,:] = cv2.resize(camera_img_, (0,0), fx=1, fy=1)
		camera_img_ = camera_[img_index_][:]
		D[base_graph][img][-shape(camera_img_)[0]:,-shape(camera_img_)[1]:,:] = camera_img_
	D[insert_camera_image] = _function_insert_camera_image	

	D[cv2_key_commands] = {
		'p':("P[START_TIME] -= P[REAL_TIME_DTV]; P[END_TIME] -= P[REAL_TIME_DTV]",
			"Time step forward,real time"),
		'm':("P[START_TIME] -= P[REAL_TIME_DTV]/2.0; P[END_TIME] -= P[REAL_TIME_DTV]/2.0",
			"Time step forward,real time"),
		'l':("P[START_TIME] -= dt_; P[END_TIME] -= dt_",
			"Time step forward"),
		'h':("P[START_TIME] += dt_; P[END_TIME] += dt_",
			"Time step back"),
		'u':("P[START_TIME] += P[REAL_TIME_DTV]; P[END_TIME] += P[REAL_TIME_DTV]",
			"Time step back, real time"),
		'v':("P[START_TIME] += P[REAL_TIME_DTV]/2.0; P[END_TIME] += P[REAL_TIME_DTV]/2.0",
			"Time step back, real time"),
		'j':("P[START_TIME] += 100.0*dt_; P[END_TIME] -= 100.0*dt_",
			"Time scale out"),
		'k':("P[START_TIME] -= 100.0*dt_; P[END_TIME] += 100.0*dt_",
			"Time scale in"),
		' ':("P[VERTICAL_LINE_PROPORTION]=0.5;" +
			"P[START_TIME],P[END_TIME] = P[START_TIME_INIT],P[END_TIME_INIT];" +
			"ymin_,ymax_ = ymin_init_,ymax_init_;"+
			"show_menuv = True","Reset"),
		'a':("show_menuv = True","Menu"),
		'q':("sys.exit()","Quit"),
	}

	def _function_process_key_commands(*args):
		Args = args_to_dictionary(args)
		key_ = Args[key]
		True
		key_decoded_ = False
		dt_ = D[dt]
		if key_ == ord('q'): sys.exit()
		elif key_ == ord('j'): D[start_time] += 100.0*dt_; D[end_time] -= 100.0*dt_
		elif key_ == ord('k'): D[start_time] -= 100.0*dt_; D[end_time] += 100.0*dt_
		elif key_ == ord('l'): D[start_time] -= dt_; D[end_time] -= dt_
		elif key_ == ord('h'): D[start_time] += dt_; D[end_time] += dt_
		elif key_ == ord(' '): D[start_time],D[end_time] = D[start_time_init],D[end_time_init];


		if False: #not key_decoded_:
			if key_ != -1:
				try:
					print(d2s('key_ =',key_))
					print(d2s(str(unichr(key_)), '=',key_))
				except Exception as e:
					pass
					#print("********** Exception ***********************")
					#print(e.message, e.args)
	D[process_key_commands] = _function_process_key_commands
	

	def _function_graph_topics(*args):
		Args = args_to_dictionary(args)
		True
		ctr_ = 0
		for topic_ in sorted(D[topics].keys()):

			if topic_ in P[TOPICS]:

				vals_ = np.array(D[topics][topic_][vals][:])
				ts_ = np.array(D[topics][topic_][ts][:])

				if P[TOPICS][topic_][minval] == minval:
					ymin_ = min(vals_)
				else:
					ymin_ = P[TOPICS][topic_][minval]
				if P[TOPICS][topic_][maxval] == maxval:
					ymax_ = max(vals_)
				else:
					ymax_ = P[TOPICS][topic_][maxval]

				dyv = (ymax_ - ymin_)
				ymin_ = ymax_ - dyv*(len(D[topics].keys())+1)
				ymax_ += dyv*ctr_
				ctr_ += 1
				ymin_init_,ymax_init_, = ymin_,ymax_
				I = {}
				I[topic_] = Graph_Image_Module.Graph_Image(
					xsize,P[X_PIXEL_SIZE],
					ysize,P[Y_PIXEL_SIZE],
					xmin,D[start_time],
					xmax,D[end_time],
					ymin,ymin_,
					ymax,ymax_,
					Img,D[base_graph])
				baseline_vals_ = 0*ts_ + P[TOPICS][topic_][baseline]
				baseline_color_ = (64,64,64)

				I[topic_][ptsplot](x,ts_, y,vals_, color,P[TOPICS][topic_][color])
				I[topic_][ptsplot](x,ts_, y,baseline_vals_, color,baseline_color_)
	D[graph_topics] = _function_graph_topics


	def _function_show(*args):
		"""
		Note, the input is in terms of t0 = 0, but the data is time since The Epoch.
		"""

		Args = args_to_dictionary(args)

		if start_time in Args:
			D[start_time] = D[start_time_init]+Args[start_time]
		if end_time in Args:
			D[end_time] = D[start_time] + Args[end_time]

		if ref_time in Args:
			ref_time_ = Args[ref_time]
		else:
			ref_time_ = (D[start_time]+D[end_time])/2.0 - D[start_time]
		True
		D[reference_time] = D[end_time]#find_nearest(np.array(D[topics][left_image][ts][:]),ref_time_+D[start_time])   #D[topics][left_image][ts][0])
		img_index_ = D[timestamp_to_left_image][D[reference_time]]
		D[base_graph][img] *= 0
		D[graph_topics]()
		vertical_line_proportion_ = (D[reference_time]-D[start_time])/(D[end_time]-D[start_time])
		D[vertical_line](vertical_line_proportion,vertical_line_proportion_, color,(0,0,255))
		D[dt] = (D[start_time]-D[end_time])*0.001
		 
		#D[insert_camera_image](camera,D[topics][left_image][vals], img_index, img_index_)#D[timestamp_to_left_image][ts_from_pixel_])
		if left_image in D[topics]:
			camera_img_ =  D[topics][left_image][vals][-1].copy()
			cx_ = (P[Y_PIXEL_SIZE]-P[CAMERA_SCALE]*shape(camera_img_)[0])
			cy_ = (P[X_PIXEL_SIZE]-P[CAMERA_SCALE]*shape(camera_img_)[1])
			angles_to_center, angles_surfaces, distances_marker, markers = Angle_Dict_Creator.get_angles_and_distance(camera_img_)
			for i_ in rlen(markers):
				
				xy_ = markers[i_].corners_xy[0].mean(axis=0)
				#xy_ += np.array([cy_-10,cx_-10])
				
				xy_=tuple(xy_.astype(np.int))
				
				if P[SHOW_MARKER_ID]:
					num_ = markers[i_].marker_id
				else:
					num_ = int(np.degrees(angles_to_center[markers[i_].marker_id])/2)
				cv2.putText(
					camera_img_,
					d2n(num_),
					xy_,
					cv2.FONT_HERSHEY_SIMPLEX,
					1.0,(0,255,0),2) 
			#print(dp(np.array(angles_to_center),1))
			#D[insert_camera_image](camera,D[topics][left_image][vals], img_index,-1)#D[timestamp_to_left_image][ts_from_pixel_])
			D[base_graph][img][cx_-10:-10,cy_-10:-10,:] = camera_img_
		key_ = mci(D[base_graph][img],color_mode=cv2.COLOR_RGB2BGR,delay=1,title='topics')

		D[process_key_commands](key,key_)
	D[show] = _function_show



	return D

			




























#EOF
