from Names_Module import *
from kzpy3.utils2 import *
exec(identify_file_str)



import resource

# the soft limit imposed by the current configuration
# the hard limit imposed by the operating system.
soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
print 'Soft limit is ', soft 

# For the following line to run, you need to execute the Python script as root.
resource.setrlimit(resource.RLIMIT_NOFILE, (60000, soft))

soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
print 'Soft limit is ', soft 


P = {}

P['experiments_folder'] = '/home/karlzipser/Desktop/all_aruco_reprocessed'


P[GPU] = 1
P[BATCH_SIZE] = 64
P[DISPLAY] = True
P[VERBOSE] = True
P[LOAD_ARUCO] = False
P[BAIR_CAR_DATA_PATH] = opjD('bdd_car_data_Sept2017_aruco_demo')
P[CODE_PATH] = CODE_PATH__
P[IGNORE] = [reject_run,left,out1_in2]#,'Smyth','racing','local','Tilden','campus']
P[REQUIRE_ONE] = []
P[USE_STATES] = [1,3,5,6,7]
P[N_FRAMES] = 2
P[N_STEPS] = 10
P[STRIDE] = 9#3 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
P[NETWORK_OUTPUT_FOLDER] = opjD('net_indoors')
P[SAVE_FILE_NAME] = 'net'
P[save_net_timer] = Timer(60*5)
P[print_timer] = Timer(4)
P[TRAIN_TIME] = 60*10.0
P[VAL_TIME] = 60*1.0
P[RESUME] = True
if RESUME:
    P[INITIAL_WEIGHTS_FOLDER] = opj(P[NETWORK_OUTPUT_FOLDER],'weights')
    P[WEIGHTS_FILE_PATH] = most_recent_file_in_folder(P[INITIAL_WEIGHTS_FOLDER],['net'],[])	


P['run_name_to_run_path'] = {}
P['data_moments_indexed'] = []
P['All_image_files'] = None

for e in sggo(P['experiments_folder'],'*'):
	print e
	if fname(e)[0] == '_':
		spd2s('Ignoring',e)
		continue
	d = lo(opj(e,'data_moments_indexed.pkl'))
	P['data_moments_indexed'] += d
	for r in sggo(e,'h5py','*'):
		assert(fname(r) not in P['run_name_to_run_path'])
		P['run_name_to_run_path'][fname(r)] = r


spd2s("len(P['data_moments_indexed']) =",len(P['data_moments_indexed']))

All_image_files = {}

folders5 = sgg('/home/karlzipser/Desktop/all_aruco_reprocessed/bdd_car_data_Sept2017_aruco_demo/h5py/*')

for f in P['run_name_to_run_path'].keys():
	print f
	All_image_files[f] = {}
	if True:
		try:
			O = h5r(opj(P['run_name_to_run_path'][f],'original_timestamp_data.h5py'))
			F = h5r(opj(P['run_name_to_run_path'][f],'flip_images.h5py'))
			All_image_files[f]['normal'] = O
			All_image_files[f]['flip'] = F
		except Exception as e:
			print("********** Exception ***********************")
			print(e.message, e.args)

P['All_image_files'] = All_image_files



"""
Increase the Limit

To increase the limit to 1080 use the following command:

ulimit -Sn 1080

You can change the hard limit too, ulimit -Hn 2040. ulimit -n 2040 changes 
both the soft and hard limits to the same value. Once you change the hard limit, 
you cannot increase it above the value you just set without rebooting.



lsof -Fn -u karlzipser| sort  | uniq | grep /home | wc -l



import resource

# the soft limit imposed by the current configuration
# the hard limit imposed by the operating system.
soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
print 'Soft limit is ', soft 

# For the following line to run, you need to execute the Python script as root.
resource.setrlimit(resource.RLIMIT_NOFILE, (3000, hard))


"""













#EOF