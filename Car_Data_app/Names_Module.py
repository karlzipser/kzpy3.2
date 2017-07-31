from Paths_Module import *
exec(identify_file_str)

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
	gyro_heading_x gyro_heading_y gyro_heading_z gyro_heading
	gyro_heading_x_meo gyro_heading_y_meo gyro_heading_z_meo
	gps
	ts
	right_ts
	
	SRC
	DST

	vals
	tdic
	bag_folder_path
	h5py_path
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