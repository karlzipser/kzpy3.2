###############################
#  for interactive terminal
import __main__ as main
if not hasattr(main,'__file__'):
	from kzpy3.utils2 import *
	pythonpaths(['kzpy3','kzpy3/Car_Data_app'])
#
###############################
from Parameters_Module import *
import Data_Module
exec(identify_file_str)

_ = dictionary_access

for a in Args.keys():
	_(P,a,equals,_(Args,a))

bag_folders_src = P[SRC]
bag_folders_dst = P[DST]
True

runsv = sgg(opj(bag_folders_src,'*'))
print(bag_folders_src)
assert(len(runsv) > 0)


cprint('Preliminary check of '+bag_folders_src)
cprint("	checking bag file sizes and run durations")

##############
# Old code below, not always using dic naming conventions
for rv in runsv:
	bags = sgg(opj(rv,'*.bag'))
	cprint(d2s(tb,fname(rv),len(bags)))
	mtimes = []
	for b in bags:
		bag_size = os.path.getsize(b)
		mtimes.append(os.path.getmtime(b))
		if bag_size < 0.99 * 1074813904:
			cprint(d2s('Bagfile',b,'has size',bag_size,'which is below full size.'),'red')
			unix('mv '+b+' '+b+'.too_small')
	mtimes = sorted(mtimes)
	run_duration = mtimes[-1]-mtimes[0]
	print run_duration
	assert(run_duration/60./60. < 3.) # If clock set incorrectly, this can change during run leading to year-long intervals
	cprint(d2s(rv,'is okay'))
#
##############

for rv in runsv:
	D = Data_Module.Original_Timestamp_Data(bag_folder_path,rv, h5py_path,bag_folders_dst)
if fname(bag_folders_src) == 'new':
	os.rename(bag_folders_src,opj(pname(bag_folders_src),'processed2'))





def Timeseries_Data(*args):
	Args = args_to_dictionary(args)
	D = {}
	D[ts],D[vals] = get_key_sorted_elements_of_dic(Args[tdic])
	D[vals] = np.array(D[vals])
	True
	return D




# def Left_Timestamp_Data
if da(P,EXAMPLE2):
	dataset_pathv = 'ExtraDrive2/bdd_car_data_July2017_LCR'
	run_namev = 'direct_home_LCR_25Jul17_19h37m22s_Mr_Yellow'

	pathv = opjm(dataset_pathv,'meta',run_namev,'preprocessed_data.pkl')

	assert_disk_locations(pathv)

	Preprocessed_data = lo(opjm(dataset_pathv,'meta',run_namev,'preprocessed_data.pkl'))

	Original_timestamp_data = {}

	for kv in Preprocessed_data.keys():
		Original_timestamp_data[kv] = Timeseries_Data(topic,kv, tdic,Preprocessed_data[kv])
		print kv,len(Preprocessed_data[kv])

	for kv in Original_timestamp_data.keys():
		if len(shape(Original_timestamp_data[kv][vals])) == 2:
			if shape(Original_timestamp_data[kv][vals])[1] == 3:
				ctrv = 0
				for qv in [x]:#,y,z]:
					new_keyv = kv+'_'+qv
					Original_timestamp_data[new_keyv] = {}
					Original_timestamp_data[new_keyv][ts] = Original_timestamp_data[kv][ts]
					Original_timestamp_data[new_keyv][vals] = Original_timestamp_data[kv][vals][:,ctrv]
					ctrv += 1
				del Original_timestamp_data[kv]

	Left_timestamp_data = {}
	Left_timestamp_data[ts] = np.array(Original_timestamp_data[left_image][ts])

	Left_timestamp_data[right_ts] = []
	for iv in range(len(Original_timestamp_data[left_image][vals])):
		Left_timestamp_data[right_ts].append(Original_timestamp_data[right_image][ts][iv])
	Left_timestamp_data[right_ts] = np.array(Left_timestamp_data[right_ts])
	assert( np.abs( 0.03 - np.median(Left_timestamp_data[ts] - Left_timestamp_data[right_ts]) ) < 0.01 )

	for kv in sorted(Original_timestamp_data.keys()):
		if kv != left_image and kv != right_image:
			if len(Original_timestamp_data[kv][ts]) > 0:
				print('processing '+kv)
				Left_timestamp_data[kv] = np.interp(Left_timestamp_data[ts],
					Original_timestamp_data[kv][ts],Original_timestamp_data[kv][vals])
				if kv in P[MEO_PARAMS]:
					Left_timestamp_data[kv+'_meo'] = np.interp(Left_timestamp_data[ts],
						Original_timestamp_data[kv][ts],meo(Original_timestamp_data[kv][vals],P[MEO_PARAMS][kv]))

	Left_timestamp_data[state] = Left_timestamp_data[state].astype(int)

	Left_timestamp_data[left_ts_deltas] = 0.0 * Left_timestamp_data[ts]
	for iv in range(1,len(Left_timestamp_data[ts])):
		Left_timestamp_data[left_ts_deltas][iv] = Left_timestamp_data[ts][iv] - Left_timestamp_data[ts][iv-1]

"""
"""
#get imu std

if False:
	vv = []
	for iv in range(100,81000):
		vv.append(np.std(yv[iv-50:iv+50]))
	plot(vv)
"""


if False:
	D = h5py.File('/media/karlzipser/ExtraDrive2/bdd_car_data_July2017_LCR/h5py/direct_local_LCR_28Jul17_10h22m41s_Mr_Yellow/original_timestamp_data.h5py','r')
	L = D['left_image']
	imgsv = L['vals']
	for iv in range(1000,35216,):
		mci(imgsv[iv:94+iv,:,84,:],delay=1,scale=4)


#EOF


