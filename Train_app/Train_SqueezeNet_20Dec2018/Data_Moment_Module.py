from kzpy3.utils3 import *
from default_values import *
exec(identify_file_str)


F = h5r('/home/karlzipser/Desktop/Data/shuffled_h5py_data/tegra-ubuntu_30Oct18_15h58m09s.h5py')
index = 0
Data_moment = {}
once = False
def get_Data_moment():

	#if once:
	#	return Data_moment

	global index,Data_moment,once



	labels = {
		'direct': 0,
		'follow': 0,
		'furtive': 0,
		'heading_pause': 0,
		'left': 0,
		'play': 0,
		'right': 0,
	 }
	behavioral_mode = Behavioral_code_to_mode[F['behavioral_mode_code'][index]]
	labels[behavioral_mode] = 1

	Data_moment = {}

	Data_moment['name'] = 			'tegra-ubuntu_30Oct18_15h58m09s'
	Data_moment['labels'] = 		labels
	Data_moment['encoder_meo'] = 	F['encoder_meo'][index][:]
	Data_moment['gyro_heading_x'] = F['gyro_heading_x'][index][:]
	Data_moment['FLIP'] = 			F['flip'][index]
	Data_moment['encoder_past'] = 	F['encoder_past'][index][:]
	Data_moment['motor'] = 			F['motor'][index][:]
	Data_moment['steer'] = 			F['steer'][index][:]
	Data_moment['encoder_meo'] = 	F['encoder_meo'][index]
	Data_moment['left'] = 			F['left'][index]
	Data_moment['right'] = 			F['right'][index]
	Data_moment['left_small'] = 	F['left_small'][index]
	Data_moment['right_small'] = 	F['right_small'][index]
	index += 1
	if index >= len(F['flip']):
		index = 0

	once = True

	return Data_moment




def show_Data_moment(d):
	pass



#EOF