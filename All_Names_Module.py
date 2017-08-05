use_wordsv = """
	h5py_folder
	EXAMPLE1
	EXAMPLE2
	EXAMPLE3
	EXAMPLE4
	EXAMPLE5
	EXAMPLE6
	EXAMPLE7
	EXAMPLE8
	VERBOSE
	
	MEO_PARAMS
	DATASET_PATH RUN_NAME
	topic
	run_name
	h5py_path
	x y z

	dic_type
	acc_x
	acc_y
	acc_z
	acc_x_meo
	acc_y_meo
	acc_z_meo

	acc
	right_image
	gyro_x
	gyro_y
	gyro_z
	gyro_x_meo
	gyro_y_meo
	gyro_z_meo
	gyro
	encoder
	encoder_meo

	left_ts_deltas

	state
	steer
	motor
	left_image
	gyro_heading_x
	gyro_heading_y
	gyro_heading_z
	gyro_heading
	gyro_heading_x_meo
	gyro_heading_y_meo
	gyro_heading_z_meo
	gps
	ts
	right_ts
	
	SRC
	DST
	DATA_SRC 
	vals
	tdic
	bag_folder_path
	h5py_path
	meta_run_path
	preprocessed_datafile_path
	rgb_1to4_path

	EXAMPLE1
	EXAMPLE2
	EXAMPLE3
	EXAMPLE4
	EXAMPLE5
	EXAMPLE6
	EXAMPLE7
	EXAMPLE8
	VERBOSE
	cameras
	color
	color_mode
	coordinates
	data_type
	dic_type
	floats_to_pixels
	image
	img
	left_image
	lines_plot
	pixels_to_floats
	ptsplot
	purpose
	steer
	x xint
	xmax
	xmin
	xscale
	xsize
	y yint
	ymax
	ymin
	yscale
	ysize

	acc
	right_image
	gyro
	encoder
	state
	steer
	motor
	left_image
	gyro_heading
	gps
	TOPICS
	name
	maxval
	minval
	START_TIME
	END_TIME
	CV2_KEY_COMMANDS
	pixel_to_float
	VERTICAL_LINE_PROPORTION START_TIME END_TIME X_PIXEL_SIZE Y_PIXEL_SIZE SCREEN_X SCREEN_Y
	MOUSE_X MOUSE_Y
	START_TIME_INIT END_TIME_INIT
	MOUSE_X MOUSE_Y MOUSE_MOVE_TIME
	center_time
	L_FILE O_FILE
	Image_source
	REAL_TIME_DTV MOUSE_IN_RED_ZONE
	IMAGE2 IMAGE3
	TEMP_RUN_NUMBER
	check show ICONS
	width height name number x y img click_time clicked
	Img
	START_TIME_INIT END_TIME_INIT Y_PIXEL_SIZE_INIT X_PIXEL_SIZE_INIT
	path
	CURRENT_ICON_NUM CAMERA_SCALE CURRENT_ICON
	baseline
	H5PY_RUNS CURRENT_ICON_NAME DATASET_PATHS MAX_ICONS_PER_ROW Y_MOUSE_RANGE_PROPORTION

	reject_run 
	left 
	out1_in2 
	dic 
	name 
	test 
	dic_type 
	purpose 
	batch_size 
	net 
	camera_data 
	metadata 
	target_data 
	names 
	states 
	loss_dic 
	train 
	val 
	ctr 
	all_steer 
	epoch_counter 
	get_data 
	next 
	run_code 
	seg_num 
	offset 
	all_data_moment_id_codes 
	left 
	right 
	fill 
	clear 
	forward 
	backward 
	display 
	GPU 
	BATCH_SIZE 
	DISPLAY 
	VERBOSE 
	LOAD_ARUCO 
	BAIR_CAR_DATA_PATH 
	RESUME 
	IGNORE 
	REQUIRE_ONE 
	USE_STATES 
	N_FRAMES 
	N_STEPS 
	STRIDE 
	save_net_timer 
	print_timer 
	epoch_timer 
	WEIGHTS_FILE_PATH 
	SAVE_FILE_NAME 
	mode 
	criterion 
	optimizer 
	data_ids 
	data_moment 
	racing 
	caffe 
	follow 
	direct 
	play 
	furtive 
	labels 
	LCR 
	data_moment_loss_record 
	loss 
	outputs 
	print_now 
	network 
	metadata 
	steer 
	motor 
	data 
	NETWORK_OUTPUT_FOLDER 
	code data_moment_loss_records loss_history weights   
	save_net 
	CODE_PATH 
	rate_ctr 
	rate_timer 
	step 
	rate_counter 
	loss_record 
	add loss 
	TRAIN_TIME 
	VAL_TIME INITIAL_WEIGHTS_FOLDER 
	activiations 
	moment_index  imgs  view camera_input final_output 
	pre_metadata_features pre_metadata_features_metadata post_metadata_features scales delay


"""












from kzpy3.utils import *
import re
#import keyword

"""
def represents_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
"""

def getWords(text):
    return re.compile('\w+').findall(text)

_ignore_words_strv_ = """
	args
	astype
	float
	implemented
	int64
	stack
	translates
	uint8
	vis2
	which
	EOF
	COLOR_RGB2BGR
	a
	bair_car_data_Main_Dataset
	bdd_car_data_July2017_LCR
	copy
	delay
	direct_local_LCR_10Jul17_09h36m15s_Mr_Yellow
	furtive_24Aug2016_Tilden
	hasattr
	home
	i
	interactive
	interp
	karlzipser
	keys
	kzpy3
	logical_and
	main
	max
	meta
	o
	pkl
	png
	preprocessed_data
	sin
	teg9
	terminal
	utils2
	where
"""

"""
_ignore_words_ = getWords(_ignore_words_strv_)
"""

"""
code_filesv = gg(opj(CODE_PATH__,'*.py'))
code_files2v = []
for cv in code_filesv:
	if 'Paths_Module' not in cv:
		if 'Names_Module' not in cv:
			code_files2v.append(cv)

print(code_files2v)
codev = []
for cv in code_files2v:
	codev += txt_file_to_list_of_strings(cv)

cv='\n'.join(codev)
wordsv = getWords(cv)
Words = {}
for wv in wordsv:
	if wv in _ignore_words_:
		#print wv
		continue
	if wv in globals():
		#print wv
		continue
	if keyword.iskeyword(wv):
		continue
	if wv[-1] == 'v':
		continue
	if str.isupper(wv[0]):
		if len(wv) == 1:
			continue
		if not str.isupper(wv[1]):
			continue
	if represents_int(wv[0]):
		continue
	if wv[0] == '_':
		continue
	if wv in locals():
		#print wv
		continue
	Words[wv] = True

print('---')
swordsv = sorted(Words.keys())
for wv in swordsv:
	print(wv)
"""


use_words_listv = getWords(use_wordsv)
for _name in use_words_listv:
	exec(d2n(_name,'=',"'",_name,"'"))


#EOF

















#EOF

