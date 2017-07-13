from kzpy3.utils2 import *
pythonpaths(['kzpy3','kzpy3/teg10'])
from vis2 import *
import data.utils.preprocess_bag_data as preprocess_bag_data
import data.utils.preprocess_Bag_Folders as preprocess_Bag_Folders
import data.utils.Bag_File as Bag_File

doc_string="""
e.g.,
python kzpy3/teg10/data/preprocess.py -src /media/karlzipser/ExtraDrive2/Mr_Purple_7July2017 -dst /media/karlzipser/ExtraDrive2/bdd_car_data_July2017_path_dataset -n 30
"""


"""
local_variable_names = ['argument_dictionary']
for l in local_variable_names:
	exec(d2n(l,'=',"'",l,"'"))
local_variable_values = {}
lv = local_variable_values
"""


translation_dic = {'src':'bag_folders_src_location','dst':'bag_folders_dst','n':'NUM_STATE_ONE_STEPS','bd':'DO_PREPROCESS_BAG_DATA','bf':'DO_PREPROCESS_BAG_FOLDERS'}
if __name__ == "__main__" and '__file__' in vars():
    argument_dictionary = args_to_dic({  'pargs':sys.argv[1:]  })
else:
    print('Running this within interactive python.')
    argument_dictionary = args_to_dic({
    	'pargs':"-src /media/karlzipser/ExtraDrive2/Mr_Purple_7July2017 -dst /media/karlzipser/ExtraDrive2/bdd_car_data_TEMP -n 30 -bd True -bf False"  })
argument_dictionary = translate_args(
    {'argument_dictionary':argument_dictionary,
    'translation_dic':translation_dic})
if len(argument_dictionary) == 0:
	pd2s(doc_string)
	nice_print_dic({'dic':translation_dic,'name':'arguments'})
	exit()
nice_print_dic({'dic':argument_dictionary,'name':'argument_dictionary'})


#nice_print_dic({dic:v[argument_dictionary],name:argument_dictionary})





def preprocess(d):
	bag_folders_src_location = d['bag_folders_src_location']
	bag_folders_dst = d['bag_folders_dst']
	NUM_STATE_ONE_STEPS = int(d['NUM_STATE_ONE_STEPS'])
	assert(is_number(NUM_STATE_ONE_STEPS))
	for k in ['DO_PREPROCESS_BAG_DATA','DO_PREPROCESS_BAG_FOLDERS']:
		if k not in d:
			exec(d2s(k,"= 'Yes'"))
		else:
			exec(d2n(k,'=',"'",d[k],"'"))
	True

	bag_folders_src = opj(bag_folders_src_location,'new')
	bag_folders_dst_rgb1to4_path = opj(bag_folders_dst,'rgb_1to4')
	bag_folders_dst_meta_path = opj(bag_folders_dst,'meta')

	runs = sgg(opj(bag_folders_src,'*'))
	assert(len(runs) > 0)




	if DO_PREPROCESS_BAG_DATA == 'Yes':
		pd2s('DO_PREPROCESS_BAG_DATA')
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



	if DO_PREPROCESS_BAG_FOLDERS == 'Yes':
		pd2s('DO_PREPROCESS_BAG_FOLDERS')
		graphics=False
		accepted_states=[1,3,5,6,7]
		pkl_name='Bag_Folder.pkl' # if different from 'Bag_Folder.pkl', (e.g., 'Bag_Folder_90_state_one_steps.pkl') files will be reprocessed.

		preprocess_Bag_Folders.preprocess_Bag_Folders(bag_folders_dst_meta_path,
			bag_folders_dst_rgb1to4_path
			,NUM_STATE_ONE_STEPS=NUM_STATE_ONE_STEPS,
			graphics=graphics,accepted_states=accepted_states,
			pkl_name=pkl_name)

	os.rename(bag_folders_src,opj(bag_folders_src_location,'processed'))
	






if __name__ == '__main__':
	preprocess(argument_dictionary)


# EOF
