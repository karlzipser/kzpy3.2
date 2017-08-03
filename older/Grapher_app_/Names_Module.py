from Paths_Module import *
exec(identify_file_str)
from Car_Data_app.Names_Module import *
print('---')
use_wordsv = """

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

"""

import re
import keyword
def represents_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

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
_ignore_words_ = getWords(_ignore_words_strv_)

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



use_words_listv = getWords(use_wordsv)
for _name in use_words_listv:
	exec(d2n(_name,'=',"'",_name,"'"))
#EOF