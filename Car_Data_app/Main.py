###############################
#  for interactive terminal
import __main__ as main
if not hasattr(main,'__file__'):
	from kzpy3.utils2 import *
	pythonpaths(['kzpy3','kzpy3/Car_Data_app'])
#
###############################
"""
e.g.,
python kzpy3/Car_Data_app/Main.py SRC '/media/karlzipser/rosbags/Mr_Yellow_29July2017/new' DST '/media/karlzipser/ExtraDrive2/bdd_car_data_July2017_LCR/h5py'
"""

from Parameters_Module import *
import Data_Module
exec(identify_file_str)

_ = dictionary_access

for a in Args.keys():
	_(P,a,equals,_(Args,a))

print(Args)




if SRC in Args and DST in Args:
	bag_folders_srcv = Args[SRC]
	h5py_dst = Args[DST]
	True

	runsv = sgg(opj(bag_folders_srcv,'*'))
	print(bag_folders_srcv)
	assert(len(runsv) > 0)


	cprint('Preliminary check of '+bag_folders_srcv)
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
		Data_Module.Original_Timestamp_Data(bag_folder_path,rv, h5py_path,h5py_dst)
		Data_Module.Left_Timestamp_Metadata(run_name,fname(rv), h5py_path,h5py_dst)
	if fname(bag_folders_srcv) == 'new':
		os.rename(bag_folders_srcv,opj(pname(bag_folders_srcv),'processed2'))





if P[ EXAMPLE2 ]:
	L = h5r('/media/karlzipser/ExtraDrive2/bdd_car_data_July2017_LCR/h5py/direct_local_LCR_29Jul17_18h09m32s_Mr_Yellow/left_timestamp_metadata.h5py')
	for kv in L.keys():
		figure(kv)
		plot(L[ts][:],L[kv][:])








#EOF


