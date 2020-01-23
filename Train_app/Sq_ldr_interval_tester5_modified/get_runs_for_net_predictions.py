from kzpy3.utils3 import *

exec(identify_file_str)

P = {}

P['experiments_folders'] = []
P['run_folders'] = []
verbose = False



##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##								Don't change this so that it can be copied from Parameter_Module.py
if True:
	import kzpy3.Data_app.classify_data as classify_data
	
	
	if True:
		locations_to_classify = [opjm("1_TB_Samsung_n1"),opjm('2_TB_Samsung_n3/rosbags__preprocessed_data')]
	else:
		locations_to_classify = [opjm('2_TB_Samsung_n3/rosbags__preprocessed_data')]
	
	for l in locations_to_classify:
		cb("classify_data.find_locations('",l,"'),P['experiments_folders'])...")
		classify_data.find_locations(l,P['experiments_folders'],False)
		cb("...done.")
	if verbose: print len(P['experiments_folders'])
	if verbose: print P['experiments_folders']
	#raw_enter()
################################################################
if True:
################################################################
	older = [
		#opjm('2_TB_Samsung_n3/bdd_car_data_July2017_LCR/locations'),
		opjm('2_TB_Samsung_n3/preprocessed_5Oct2018_500GB/bdd_model_car_data_early_8Oct2018_lrc_LIDAR/locations'),
		opjm('2_TB_Samsung_n3/preprocessed_5Oct2018_500GB/bdd_model_car_data_late_Sept_early_Oct2018_lrc/locations'),
		opjm('2_TB_Samsung_n3/preprocessed_5Oct2018_500GB/bdd_car_data_late_Sept2018_lrc/locations'),
		opjm('2_TB_Samsung_n3/preprocessed_5Oct2018_500GB/bdd_car_data_18July_to_18Sept2018_lrc/locations'),
		opjm('2_TB_Samsung_n3/preprocessed_5Oct2018_500GB/model_car_data_July2018_lrc/locations'),
		#opjm('2_TB_Samsung_n3/preprocessed_5Oct2018_500GB/model_car_data_June2018_LCR/locations'),
	]

	P['experiments_folders'] += older

if False:
	P['experiments_folders'] = [
		'/media/karlzipser/1_TB_Samsung_n1/left_direct_stop__29to30Oct2018/locations',
		'/media/karlzipser/1_TB_Samsung_n1/left_direct_stop__31Oct_to_1Nov2018/locations',
	] # around 4:45pm

P['experiments_folders'] = list(set(P['experiments_folders']))
##
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################




for experiments_folder in P['experiments_folders']:
	if fname(experiments_folder)[0] == '_':
		continue
	cg("experiments_folder =",experiments_folder)
	locations = sggo(experiments_folder,'*')
	for location in locations:
		if fname(location)[0] == '_':
			spd2s('ignoring',location,"because of '_'" )
			continue
		if verbose: cg("\t",location)
		b_modes = sggo(location,'*')
		if verbose: cg("\t\tbehavioral modes at this location:", b_modes)
		for e in b_modes:
			if fname(e)[0] == '_':
				continue
			if fname(e) == 'racing':
				continue
			"""
			if fname(e) == 'play':
				continue
			if fname(e) == 'follow':
				continue
			if fname(e) == 'furtive':
				continue
			"""
			cb("\t",fname(e))
			P['run_folders'] += sggo(e,'h5py/*')

so(P['run_folders'],opjD('Data/Network_Predictions/runs.pkl'))


#EOF



