###############################
#  for interactive terminal
# import __main__ as main
# if not hasattr(main,'__file__'):
#	from kzpy3.utils2 import *
#	pythonpaths(['kzpy3','kzpy3/Data_app'])
#
###############################
"""
To preprocess rosbags, e.g.:
python kzpy3/Car_Data_app/Main.py SRC '/media/karlzipser/rosbags/Mr_Yellow_29July2017/new' DST '/media/karlzipser/ExtraDrive2/bdd_car_data_July2017_LCR/h5py'

To convert from pkl representation of data, e.g.:

python kzpy3/Car_Data_app/Main.py DATA_SRC '/media/karlzipser/ExtraDrive2/bdd_car_data_July2017_regular'  DST '/media/karlzipser/ExtraDrive2/bdd_car_data_July2017_regular/h5py'

To change rosbags disk permissions: sudo chmod -R 777 /media/karlzipser/rosbags/

* Put flip into processing pipeline
"""

from Parameters_Module import *
import Data_Module
exec(identify_file_str)

for a in Args.keys():
	P[a] = Args[a]

print(Args)

if SRC in Args and DST in Args:
	bag_folders_src_ = Args[SRC]
	h5py_dst = Args[DST]
	assert_disk_locations(bag_folders_src_)
	runs = sgg(opj(bag_folders_src_,'*'))
	#print(bag_folders_src_)
	assert(len(runs) > 0)


	cprint('Preliminary check of '+bag_folders_src_)
	cprint("	checking bag file sizes and run durations")

	for r in runs:
		bags = sgg(opj(r,'*.bag'))
		cprint(d2s(tb,fname(r),len(bags)))
		mtimes = []
		for b in bags:
			#print b
			bag_size = os.path.getsize(b)
			#print bag_size
			mtimes.append(os.path.getmtime(b))
			#print mtimes
			if bag_size < 0.99 * 1074813904:
				cprint(d2s('Bagfile',b,'has size',bag_size,'which is below full size.'),'red')
				unix('mv '+b+' '+b+'.too_small')
		mtimes = sorted(mtimes)
		#pd2s('mtimes:',mtimes)
		run_duration = mtimes[-1]-mtimes[0]
		pd2s('run_duration:',run_duration)
		assert(run_duration/60./60. < 3.) # If clock set incorrectly, this can change during run leading to year-long intervals
		cprint(d2s(r,'is okay'))


	success = True
	for r in runs:
		try:
			Data_Module.Original_Timestamp_Data(bag_folder_path=r, h5py_path=h5py_dst)
			#if P['ARUCO'] == 'True':
			#	spd2s('aruco!')
			Data_Module.make_flip_images(h5py_folder=opj(h5py_dst,fname(r)))
			Data_Module.Left_Timestamp_Metadata(run_name=fname(r), h5py_path=h5py_dst)
		except Exception as e:
			print("**********for r in runs: Exception ***********************")
			print(e.message, e.args)
			success = False
	if success:
		if fname(bag_folders_src_) == 'new':
			os.rename(bag_folders_src_,opj(pname(bag_folders_src_),'processed_'+time_str()))


elif DATA_SRC in Args and DST in Args:
	data_src_ = Args[DATA_SRC]
	h5py_dst_ = Args[DST]
	True

	runs = sggo(data_src_,'meta','*')
	print(data_src_)
	assert(len(runs) > 0)
	for r in runs:
		try:
			Data_Module.Original_Timestamp_Data_from_preprocessed_data_pkl(
				preprocessed_datafile_path,opj(r,'preprocessed_data.pkl'),
				h5py_path,h5py_dst_,
				rgb_1to4_path,opj(data_src_,'rgb_1to4',fname(r)))
			Data_Module.Left_Timestamp_Metadata(run_name,fname(r), h5py_path,h5py_dst_)
		except Exception as e:
			print("********** elif DATA_SRC in Args and DST in Args: Exception ***********************")
			print(e.message, e.args)	




#EOF


