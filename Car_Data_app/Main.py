###############################
#  for interactive terminal
import __main__ as main
if not hasattr(main,'__file__'):
	from kzpy3.utils2 import *
	pythonpaths(['kzpy3','kzpy3/Car_Data_app'])
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

_ = dictionary_access

for a in Args.keys():
	_(P,a,equals,_(Args,a))

print(Args)




if SRC in Args and DST in Args:
	bag_folders_src_ = Args[SRC]
	h5py_dst = Args[DST]
	True

	runs_ = sgg(opj(bag_folders_src_,'*'))
	print(bag_folders_src_)
	assert(len(runs_) > 0)


	cprint('Preliminary check of '+bag_folders_src_)
	cprint("	checking bag file sizes and run durations")

	##############
	# Old code below, not always using dic naming conventions
	for r_ in runs_:
		bags = sgg(opj(r_,'*.bag'))
		cprint(d2s(tb,fname(r_),len(bags)))
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
		print mtimes
		run_duration = mtimes[-1]-mtimes[0]
		print run_duration
		assert(run_duration/60./60. < 3.) # If clock set incorrectly, this can change during run leading to year-long intervals
		cprint(d2s(r_,'is okay'))
	#
	##############

	for r_ in runs_:
		Data_Module.Original_Timestamp_Data(bag_folder_path,r_, h5py_path,h5py_dst)
		Data_Module.Left_Timestamp_Metadata(run_name,fname(r_), h5py_path,h5py_dst)
		Data_Module.make_flip_images(h5py_folder,opj(h5py_dst,fname(r_)))
	if fname(bag_folders_src_) == 'new':
		os.rename(bag_folders_src_,opj(pname(bag_folders_src_),'processed_'+time_str()))


elif DATA_SRC in Args and DST in Args:
	data_src_ = Args[DATA_SRC]
	h5py_dst_ = Args[DST]
	True

	runs_ = sggo(data_src_,'meta','*')
	print(data_src_)
	assert(len(runs_) > 0)
	for r_ in runs_:
		try:
			Data_Module.Original_Timestamp_Data_from_preprocessed_data_pkl(
				preprocessed_datafile_path,opj(r_,'preprocessed_data.pkl'),
				h5py_path,h5py_dst_,
				rgb_1to4_path,opj(data_src_,'rgb_1to4',fname(r_)))
			Data_Module.Left_Timestamp_Metadata(run_name,fname(r_), h5py_path,h5py_dst_)
		except Exception as e:
			print("********** Exception ***********************")
			print(e.message, e.args)	




#EOF


