from kzpy3.utils2 import *
pythonpaths(['kzpy3','kzpy3/teg10'])
from vis2 import *
import data.utils.preprocess_bag_data as preprocess_bag_data
import data.utils.preprocess_Bag_Folders as preprocess_Bag_Folders
import data.utils.Bag_File as Bag_File


"""
e.g.,
python kzpy3/teg10/preprocess.py --src /media/karlzipser/rosbags/temp --dst /media/karlzipser/ExtraDrive2/bdd_car_data_July2017_path_dataset/ --num 30 --accepted_states [1,2,3] --bd yes --bf yes

python kzpy3/teg10/data/preprocess.py --src /media/karlzipser/rosbags/temp --dst /media/karlzipser/ExtraDrive2/bdd_car_data_July2017_LCR --num 30 --accepted_states [1,2,3] --bd no --bf yes --redo_bag_folders yes
"""
cmd_line_args = "--src /media/karlzipser/rosbags/temp --dst /media/karlzipser/ExtraDrive2/bdd_car_data_July2017_LCR --num 30 --accepted_states [1,2,3] --bd no --bf yes --redo_bag_folders yes"
Command_line_arguments = args_to_dictionary(cmd_line_args.split(' '))

for _name in ['dic','REDO_BAG_FOLDERS','DO_PREPROCESS_BAG_DATA','DO_PREPROCESS_BAG_FOLDERS','accepted_states','bag_folders_src_location',
	'bag_folders_dst','NUM_STATE_ONE_STEPS']:
    exec(d2n(_name,'=',"'",_name,"'"))
G = {}

G[DO_PREPROCESS_BAG_DATA],G[DO_PREPROCESS_BAG_FOLDERS] = True,True
G[REDO_BAG_FOLDERS] = False
G[accepted_states] = [1,3,5,6,7]
G[bag_folders_src_location] = Command_line_arguments['--src']
G[bag_folders_dst] = Command_line_arguments['--dst']
G[NUM_STATE_ONE_STEPS] = int(Command_line_arguments['--num'])
if '--redo_bag_folders' in Command_line_arguments:
	if Command_line_arguments['--redo_bag_folders'] == 'yes':
		G[REDO_BAG_FOLDERS] = True
if '--bd' in Command_line_arguments:
	if Command_line_arguments['--bd'] != 'yes':
		G[DO_PREPROCESS_BAG_DATA] = False
if '--bf' in Command_line_arguments:
	if Command_line_arguments['--bf'] != 'yes':
		G[DO_PREPROCESS_BAG_FOLDERS] = False
if '--accepted_states' in Command_line_arguments:
	exec("G[accepted_states] = "+Command_line_arguments['--accepted_states'])
	assert(type(G[accepted_states]) == list)

zdprint(dic,G)


bag_folders_src = opj(G[bag_folders_src_location],'new' )
bag_folders_dst_rgb1to4_path = opj(G[bag_folders_dst],'rgb_1to4')
bag_folders_dst_meta_path = opj(G[bag_folders_dst],'meta')
#print bag_folders_dst_rgb1to4_path
#print bag_folders_dst_meta_path


if G[DO_PREPROCESS_BAG_DATA]:

	runs = sgg(opj(bag_folders_src,'*'))
	assert(len(runs) > 0)

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


if G[DO_PREPROCESS_BAG_FOLDERS]:

	graphics=False
	"""
	if G[REDO_BAG_FOLDERS]:
		pd2s('Redoing bag folders . . .')
		pkl_name = 'Bag_Folder_REDO.pkl' # if different from 'Bag_Folder.pkl', (e.g., 'Bag_Folder_90_state_one_steps.pkl') files will be reprocessed.
	else:
		pkl_name = 'Bag_Folder.pkl'

	preprocess_Bag_Folders.preprocess_Bag_Folders(bag_folders_dst_meta_path,
		bag_folders_dst_rgb1to4_path
		,NUM_STATE_ONE_STEPS=NUM_STATE_ONE_STEPS,
		graphics=graphics,accepted_states=G[accepted_states],
		pkl_name=pkl_name)
	"""
	accepted_states=[1,3,5,6,7]
	pkl_name='Bag_Folder.pkl' # if different from 'Bag_Folder.pkl', (e.g., 'Bag_Folder_90_state_one_steps.pkl') files will be reprocessed.

	preprocess_Bag_Folders.preprocess_Bag_Folders(bag_folders_dst_meta_path,
		bag_folders_dst_rgb1to4_path
		,NUM_STATE_ONE_STEPS=NUM_STATE_ONE_STEPS,
		graphics=graphics,accepted_states=accepted_states,
		pkl_name=pkl_name)

if G[DO_PREPROCESS_BAG_DATA]:
	os.rename(bag_folders_src,opj(G[bag_folders_src_location],'processed'))


