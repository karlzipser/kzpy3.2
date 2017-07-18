from kzpy3.vis import *
import kzpy3.teg9.data.utils.preprocess_bag_data as preprocess_bag_data
import kzpy3.teg9.data.utils.preprocess_Bag_Folders as preprocess_Bag_Folders
import kzpy3.teg9.data.utils.Bag_File as Bag_File
#import shutil

"""
e.g.,
python ~/kzpy3/teg9/data/preprocess.py /media/karlzipser/ExtraDrive2/Mr_Purple_7July2017 /media/karlzipser/ExtraDrive2/bdd_car_data_July2017_path_dataset 30
python ~/kzpy3/teg9/data/preprocess.py /media/karlzipser/ExtraDrive2/Mr_Orange_6July2017 /media/karlzipser/ExtraDrive2/bdd_car_data_July2017_path_dataset 30
python ~/kzpy3/teg9/data/preprocess.py /media/karlzipser/ExtraDrive2/Mr_Orange_8July2017 /media/karlzipser/ExtraDrive2/bdd_car_data_July2017_path_dataset 30
python ~/kzpy3/teg9/data/preprocess.py /media/karlzipser/ExtraDrive2/Mr_Purple_8July2017 /media/karlzipser/ExtraDrive2/bdd_car_data_July2017_path_dataset 30
python ~/kzpy3/teg9/data/preprocess.py /media/karlzipser/ExtraDrive2/Mr_Purple_6July2017 /media/karlzipser/ExtraDrive2/bdd_car_data_July2017_path_dataset 30

"""

bag_folders_src_location = sys.argv[1]
bag_folders_dst = sys.argv[2]
NUM_STATE_ONE_STEPS = int(sys.argv[3])
MIN_VALID_SPEED = int(sys.argv[3])
assert(is_number(NUM_STATE_ONE_STEPS))
assert(NUM_STATE_ONE_STEPS>0 and NUM_STATE_ONE_STEPS<1000)
assert(is_number(MIN_VALID_SPEED))
assert(MIN_VALID_SPEED>49 and MIN_VALID_SPEED<100)

bag_folders_src = opj(bag_folders_src_location,'new' )
bag_folders_dst_rgb1to4_path = opj(bag_folders_dst,'rgb_1to4')
bag_folders_dst_meta_path = opj(bag_folders_dst,'meta')

runs = sgg(opj(bag_folders_src,'*'))
assert(len(runs) > 0)

tb = '\t'

cprint('Preliminary check of '+bag_folders_src)
cprint("	checking bag file sizes and run durations")

for r in runs:
	bags = sgg(opj(r,'*.bag'))
	cprint(d2s(tb,fname(r),len(bags)))
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
	cprint(d2s(r,'is okay'))

for r in runs:
	preprocess_bag_data.preprocess_bag_data(r)

Bag_File.bag_folders_transfer_meta(bag_folders_src,bag_folders_dst_meta_path)
Bag_File.bag_folders_save_images(bag_folders_src,bag_folders_dst_rgb1to4_path)

graphics=False
#accepted_states=[1,3,5,6,7]
accepted_states=[1,2,3]

#pkl_name='Bag_Folder.redo.pkl' # if different from 'Bag_Folder.pkl', (e.g., 'Bag_Folder_90_state_one_steps.pkl') files will be reprocessed.
pkl_name='Bag_Folder.redo_for_min_speed.pkl' # if different from 'Bag_Folder.pkl', (e.g., 'Bag_Folder_90_state_one_steps.pkl') files will be reprocessed.

preprocess_Bag_Folders.preprocess_Bag_Folders(bag_folders_dst_meta_path,
	bag_folders_dst_rgb1to4_path
	,NUM_STATE_ONE_STEPS=NUM_STATE_ONE_STEPS,
	graphics=graphics,accepted_states=accepted_states,
	pkl_name=pkl_name,MIN_VALID_SPEED=MIN_VALID_SPEED)

os.rename(bag_folders_src,opj(bag_folders_src_location,'processed'))

