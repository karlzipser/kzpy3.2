use_wordsv = """
aruco_data markers nearest_marker
alpha beta gamma dist a h a_rotated marker marker_point marker_face GRAPHICS
pts pts_center_nearest theta pts_centered center_marker rotate_around
deg
visualize dic plot_start_configuration
	marker_data_path pts_rotated pts_translated
MARKER_SETUP
BAIR_CAR_DATA_PATH TOPIC_STEPS_LIMIT actual_pts
BATCH_SIZE
CAMERA_SCALE
CODE_PATH
CURRENT_ICON
CURRENT_ICON_NAME
CURRENT_ICON_NUM
CV2_KEY_COMMANDS
DATASET_PATH
DATASET_PATHS
DATA_SRC
DISPLAY
DST
END_TIME
END_TIME_INIT
EXAMPLE1
EXAMPLE2
EXAMPLE3
EXAMPLE4
EXAMPLE5
EXAMPLE6
EXAMPLE7
EXAMPLE8
GPU
H5PY_RUNS
ICONS
IGNORE
IMAGE2
IMAGE3
INITIAL_WEIGHTS_FOLDER vertical_line insert_camera_image cv2_key_commands
process_key_commands vertical_line_proportion camera timestamp_to_left_image
Image_source  ref_time dt ref_time img_index key
Img graph_topics
LCR
LOAD_ARUCO
L_FILE
MAX_ICONS_PER_ROW
MEO_PARAMS
MOUSE_IN_RED_ZONE
MOUSE_MOVE_TIME
MOUSE_X
MOUSE_Y
NETWORK_OUTPUT_FOLDER
N_FRAMES
N_STEPS
O_FILE
REAL_TIME_DTV
REQUIRE_ONE
RESUME
RUN_NAME
SAVE_FILE_NAME
SCREEN_X
SCREEN_Y
SRC
START_TIME
START_TIME_INIT
STRIDE
Smyth
TEMP_RUN_NUMBER
TOPICS topics
TRAIN_TIME
Tilden
USE_STATES
VAL_TIME
VERBOSE
VERTICAL_LINE_PROPORTION
WEIGHTS_FILE_PATH
X_PIXEL_SIZE
X_PIXEL_SIZE_INIT
Y_MOUSE_RANGE_PROPORTION
Y_PIXEL_SIZE
Y_PIXEL_SIZE_INIT
acc
acc_x
acc_x_meo
acc_y
acc_y_meo
acc_z
acc_z_meo
activiations
add
all_data_moment_id_codes
all_steer
aruco_ring
backward
bag_folder_path
base_graph
baseline
baseline_with_tics
batch_size
caffe
camera_data
camera_input
cameras
campus
center_time
check
clear
click_time
clicked
code
color
color_mode
coordinates
criterion
ctr
data
data_ids
data_moment
data_moment_loss_record
data_moment_loss_records
data_type
delay
dic
dic_type
direct
display
encoder
encoder_meo
end_time
end_time_init
epoch_counter
epoch_timer
fill
final_output
floats_to_pixels
follow
forward
furtive
get_data
gps
gyro
gyro_heading
gyro_heading_x
gyro_heading_x_meo
gyro_heading_y
gyro_heading_y_meo
gyro_heading_z
gyro_heading_z_meo
gyro_x
gyro_x_meo
gyro_y
gyro_y_meo
gyro_z
gyro_z_meo
h5py_folder
h5py_path
height
home
image
img
imgs
labels
left
left_image
left_image_flip
left_ts_deltas
lines_plot
local
loss
loss_dic
loss_history
loss_record
maxval
meta_path
meta_run_path
metadata
minval
mode
moment_index
mostly_caffe
mostly_human
motor
multicar
name
names
net
network
next
night
notes
number
offset
only_states_1_and_6_good
optimizer
out1_in2
outputs
path
pixel_to_float
pixels_to_floats
play
post_metadata_features
pre_metadata_features
pre_metadata_features_metadata
preprocessed_datafile_path
print_now
print_timer
ptsplot
purpose
racing
rate_counter
rate_ctr
rate_timer
reference_time
reject_intervals
reject_run
rgb_1to4_path
right
right_image
right_ts
run_code
run_labels
run_name
runs
save_net
save_net_timer
scales
seg_num
show
snow
start_time
start_time_init
state
states
steer
step
target_data
tdic
test
timestamps
topic
train
ts
txt
val
vals
values
view
weights
width
x
xint
xmax
xmin
xscale
xsize
y
yint
ymax
ymin
yscale
ysize
z
zero_baseline


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
Use_words_dic = {}
for _name in use_words_listv:
	Use_words_dic[_name] = True
use_words_listv = []
for _name in sorted(Use_words_dic.keys()):
	exec(d2n(_name,'=',"'",_name,"'"))
	use_words_listv.append(_name)
	#print(_name)


#EOF

















#EOF

