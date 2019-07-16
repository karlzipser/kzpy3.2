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

python kzpy3/Data_app/Main.py SRC '/media/karlzipser/rosbags/Mr_Yellow_29July2017/new' DST '/media/karlzipser/ExtraDrive2/bdd_car_data_July2017_LCR/h5py'

				To convert from pkl representation of data, e.g.:

				python kzpy3/Data_app/Main.py 'DATA_SRC' '/media/karlzipser/ExtraDrive2/bdd_car_data_July2017_regular'  DST '/media/karlzipser/ExtraDrive2/bdd_car_data_July2017_regular/h5py'

To change rosbags disk permissions: sudo chmod -R 777 /media/karlzipser/rosbags/

* Put flip into processing pipeline
"""

from Parameters_Module import *
import Data_Module
exec(identify_file_str)

for a in Args.keys():
	P[a] = Args[a]

print(Args)

print("""
To process data, e.g.:

	Data src /media/karlzipser/rosbags/new dst /media/karlzipser/rosbags/

or:
	Data


To view, e.g.:

	pGraph runs /media/karlzipser/rosbags/h5py/

or:

	pGraph

""")
time.sleep(2)

bag_folders_src_ = opjm('rosbags/new')
h5py_dst = opjm('rosbags/h5py')


if 'src' in Args and 'dst' in Args:
	bag_folders_src_ = Args['src']
	h5py_dst = Args['dst']

os.system('mkdir -p '+h5py_dst)

assert_disk_locations(bag_folders_src_)
runs = sgg(opj(bag_folders_src_,'*'))
#print(bag_folders_src_)
assert(len(runs) > 0)


cprint('Preliminary check of '+bag_folders_src_)
cprint("	checking bag file sizes and run durations")


preexisting_processed_runs = []

for p in sggo(h5py_dst,'*'):
	preexisting_processed_runs.append(fname(p))

if P['Allow below-size bag files?']:
	raw_enter("\n\n>>>>> Are you sure you want to 'Allow below-size bag files?'?\n")

for r in runs:
	if fname(r) in preexisting_processed_runs:
		pd2s(fname(r),'already processed.')
		continue
	bags = sgg(opj(r,'*.bag')) #+sgg(opj(r,'*.bag.too_small'))
	cprint(d2s("\t",fname(r),len(bags)))
	mtimes = []
	for b in bags:
		#print b
		bag_size = os.path.getsize(b)
		#print bag_size
		mtimes.append(os.path.getmtime(b))
		#print mtimes
		if not P['Allow below-size bag files?']:
			if bag_size < P['min bagfile size']:
				cprint(d2s('Bagfile',b,'has size',bag_size,'which is below min size,',P['min bagfile size']),'red')
				unix('mv '+b+' '+b+'.too_small')
	mtimes = sorted(mtimes)
	#pd2s('mtimes:',mtimes)
	run_duration = mtimes[-1]-mtimes[0]
	pd2s('run_duration:',run_duration)
	assert(run_duration/60./60. < 3.) # If clock set incorrectly, this can change during run leading to year-long intervals
	cprint(d2s(r,'is okay'))


success = True
for r in runs:
	if fname(r) in preexisting_processed_runs:
		pd2s(fname(r),'already processed, skipping this run.')
		continue
	if True:#try:
		Data_Module.Original_Timestamp_Data(bag_folder_path=r, h5py_path=h5py_dst)
		Data_Module.make_flip_images(h5py_folder=opj(h5py_dst,fname(r)))
		if P['use_LIDAR']:
			Data_Module.make_flip_lidar_images(h5py_folder=opj(h5py_dst,fname(r)))
		Data_Module.Left_Timestamp_Metadata(run_name=fname(r), h5py_path=h5py_dst)
	else:#except Exception as e:
		print("**********for r in runs: Exception ***********************")
		print(e.message, e.args)
		success = False
if success:
	if fname(bag_folders_src_) == 'new':
		os.rename(bag_folders_src_,opj(pname(bag_folders_src_),'processed_'+time_str()))




#EOF


