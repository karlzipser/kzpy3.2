###############################
#  for interactive terminal
import __main__ as main
if not hasattr(main,'__file__'):
	from kzpy3.utils2 import *
	pythonpaths(['kzpy3','kzpy3/Grapher_app'])
#
###############################
from Parameters_Module import *
from kzpy3.vis2 import *
import Graph_Module
from Car_Data_app.Names_Module import *
exec(identify_file_str)
"""
	* Have playback at fix rate, not machine capacity
	* Parameterize all those little display constants
	* Write out total time
	* Print out all topic values at current time
	* Show left and right images
	* Allow programatic display, exactly corresponding to network training needs
	* Need to display data from hdf5 files or from data extracted from neural network inputs/outputs
	* Need to display from ros
"""
_ = dictionary_access

for a in Args.keys():
	_(P,a,equals,_(Args,a))


P[X_PIXEL_SIZE_INIT],P[Y_PIXEL_SIZE_INIT] = P[X_PIXEL_SIZE],P[Y_PIXEL_SIZE]



h5py_run_path = '/home/karlzipser/Desktop/bdd_car_data_July2017_LCR/h5py/direct_Tilden_LCR_23Jul17_10h27m34s_Mr_Yellow'
l_ = opj(h5py_run_path,'left_timestamp_metadata.h5py')
o_  = opj(h5py_run_path,'original_timestamp_data.h5py')

O = h5r(o_ )
#ts_ = L[ts][:]
#ts_ = ts_.copy()
#ts_ -= ts_[0]


L = h5r(l_)
OO = {}
for topic_ in P[TOPICS].keys():
	if topic_ in L.keys():
		OO[topic_] = {}
		OO[topic_][ts] = L[ts][:]
		OO[topic_][vals] = L[topic_][:]
OO[left_image] = {}
OO[left_image][ts] = L[ts][:]
OO[left_image][vals] = O[left_image][vals]



def Display_Graph(*args):
	Args = args_to_dictionary(args)
	D = {}
	D[topics] = Args[topics]
	print D[topics].keys()
	True
	D[timestamp_to_left_image] = {}
	ts_ = D[topics][left_image][ts][:]
	for i_ in rlen(ts_):
		D[timestamp_to_left_image][ts_[i_]] = i_
	D[end_time] = max(ts_)
	D[start_time] = min(ts_)
	D[reference_time] = (D[start_time]+D[end_time])/2.0
	D[start_time_init],D[end_time_init] = D[start_time],D[end_time]
	D[base_graph] = Graph_Module.Graph_Image(
		xmin,D[start_time],
		xmax,D[end_time],
		ymin,-1,
		ymax,100,
		xsize,P[X_PIXEL_SIZE],
		ysize,P[Y_PIXEL_SIZE])
	D[zero_baseline] = 0*ts_
	D[baseline_with_tics] = D[zero_baseline].copy()
	for i in rlen(D[baseline_with_tics]):
		if np.mod(int(ts_[i]),10.0) == 0:
			D[baseline_with_tics][i] = 1.0

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
		camera_img_ = camera_[img_index_][:]
		cx_ = (P[Y_PIXEL_SIZE]-P[CAMERA_SCALE]*shape(camera_img_)[0])
		cy_ = (P[X_PIXEL_SIZE]-P[CAMERA_SCALE]*shape(camera_img_)[1])
		D[base_graph][img][cx_-10:-10,cy_-10:-10,:] = cv2.resize(camera_img_, (0,0), fx=4, fy=4)
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
		elif key_ == ord('k'): D[start_time] += 100
		elif key_ == ord('k'): D[start_time] += 100
		elif key_ == ord('k'): D[start_time] += 100
		elif key_ == ord('k'): D[start_time] += 100
		elif key_ == ord('k'): D[start_time] += 100
		elif key_ == ord('k'): D[start_time] += 100
		elif key_ == ord('k'): D[start_time] += 100
		elif key_ == ord('k'): D[start_time] += 100

		if not key_decoded_:
			if key_ != -1:
				try:
					print(d2s('key_ =',key_))
					print(d2s(str(unichr(key_)), '=',key_))
				except Exception as e:
					print("********** Exception ***********************")
					print(e.message, e.args)
	D[process_key_commands] = _function_process_key_commands
	

	def _function_graph_topics(*args):
		Args = args_to_dictionary(args)
		True
		ctr_ = 0
		for topic_ in sorted(D[topics].keys()):

			if topic_ in P[TOPICS]:

				vals_ = D[topics][topic_][vals][:]
				ts_ = D[topics][topic_][ts][:]

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
				I[topic_] = Graph_Module.Graph_Image(
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
				#I[topic_][ptsplot](x,ts_, y,baseline_vals_, color,baseline_color_)
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
		D[reference_time] = find_nearest(D[topics][left_image][ts][:],ref_time_+D[start_time])   #D[topics][left_image][ts][0])
		img_index_ = D[timestamp_to_left_image][D[reference_time]]
		D[base_graph][img] *= 0
		D[graph_topics]()
		vertical_line_proportion_ = (D[reference_time]-D[start_time])/(D[end_time]-D[start_time])
		D[vertical_line](vertical_line_proportion,vertical_line_proportion_, color,(0,0,255))
		D[dt] = (D[start_time]-D[end_time])*0.001
		 
		D[insert_camera_image](camera,O[left_image][vals], img_index, img_index_)#D[timestamp_to_left_image][ts_from_pixel_])

		key_ = mci(D[base_graph][img],color_mode=cv2.COLOR_RGB2BGR,delay=1,title='topics')

		D[process_key_commands](key,key_)
	D[show] = _function_show



	return D

			



if __name__ == '__main__':
	D = Display_Graph(topics,OO)
	timer=Timer(0)
	while True:
		timer.reset()
		D[show]()
		print timer.time()


#EOF0.348613977432
0.365895986557
