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



if da(P,EXAMPLE1):
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
		Data_Module.Original_Timestamp_Data(bag_folder_path,rv, h5py_path,bag_folders_dst)
		Data_Module.Left_Timestamp_Metadata()
	if fname(bag_folders_src) == 'new':
		os.rename(bag_folders_src,opj(pname(bag_folders_src),'processed2'))





































if False:
	vv = []
	for iv in range(100,81000):
		vv.append(np.std(yv[iv-50:iv+50]))
	plot(vv)



if False:
	D = h5py.File('/media/karlzipser/ExtraDrive2/bdd_car_data_July2017_LCR/h5py/direct_local_LCR_28Jul17_10h22m41s_Mr_Yellow/original_timestamp_data.h5py','r')
	L = D['left_image']
	imgsv = L['vals']
	for iv in range(1000,35216,):
		mci(imgsv[iv:94+iv,:,84,:],delay=1,scale=4)


if False:#da(P,EXAMPLE2):
	dataset_pathv = P[DATASET_PATH]
	run_namev = P[RUN_NAME]

	pathv = opj(dataset_pathv,'h5py',run_namev,'original_timestamp_data.h5py')

	assert_disk_locations(pathv)

	F = h5py.File(pathv,'r')
	L = h5py.File(opj(pname(pathv),'left_timestamp_data.h5py'),'w')

	L.create_dataset(ts,data=np.array(F[left_image][ts]))
	"""

	#Left_timestamp_data = {}
	#Left_timestamp_data[ts] = np.array(F[left_image][ts])

	Left_timestamp_data[right_tsv] = []
	for iv in range(len(F[left_image][vals])):
		Left_timestamp_data[right_tsv].append(F[right_image][ts][iv])

	Left_timestamp_data[right_tsv] = np.array(Left_timestamp_data[right_tsv])
	assert( np.abs( 0.03 - np.median(Left_timestamp_data[ts] - Left_timestamp_data[right_tsv]) ) < 0.01 )

	for kv in sorted(F.keys()):
		if kv != left_image and kv != right_image:
			if len(F[kv][ts]) > 0:
				print('\tprocessing '+kv)
				Left_timestamp_data[kv] = np.interp(Left_timestamp_data[ts],
					F[kv][ts],F[kv][vals])
				if kv in P[MEO_PARAMS]:
					Left_timestamp_data[kv+'_meo'] = np.interp(Left_timestamp_data[ts],
						F[kv][ts],meo(F[kv][vals],P[MEO_PARAMS][kv]))

	Left_timestamp_data[state] = Left_timestamp_data[state].astype(int)

	Left_timestamp_data[left_ts_deltas] = 0.0 * Left_timestamp_data[ts]
	for iv in range(1,len(Left_timestamp_data[ts])):
		Left_timestamp_data[left_ts_deltas][iv] = Left_timestamp_data[ts][iv] - Left_timestamp_data[ts][iv-1]
	"""


#EOF


