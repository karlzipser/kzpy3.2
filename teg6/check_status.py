from kzpy3.utils import *
from kzpy3.teg4.data.preprocess.preprocess_bag_data import *

data_locations = ['/home/karlzipser/Desktop/bair_car_data_rgb_1to4',
'/home/karlzipser/Desktop/bair_car_data_meta']#,
#'/media/karlzipser/bair_car_data_4/bair_car_data',
#'/media/karlzipser/bair_car_data_6/bair_car_data']
data_dic = {}
run_location_dic = {}
run_name_subsets = {}

def get_run_name_subset(data_dic,runs_path):
	rs = data_dic[runs_path].keys()
	run_name_subset = []
	for r in rs:
		run_name_subset.append(fname(r))
	return run_name_subset

		
def print_data_status(data_dic,runs_path,run_name_subset=[]):
	cprint(runs_path)
	for run in sorted(data_dic[runs_path]):
		if (fname(run) in run_name_subset) or len(run_name_subset) == 0:
			bags = data_dic[runs_path][run]['bags']
			bags_pkl = data_dic[runs_path][run]['bags.pkl']
			cprint(d2n('\t',fname(run)))
			if len(bags) > 0:
				c = 'white'
			else:
				c = 'red'
			cprint(d2n('\t\t',len(bags),' .bag files'),c)
			if len(bags_pkl) > 0:
				c = 'white'
			else:
				c = 'red'
			cprint(d2n('\t\t',len(bags_pkl),' .bag.pkl files'),c)
			left = False
			Bag_Folder = False
			if data_dic[runs_path][run]['preprocess']:
				left = data_dic[runs_path][run]['preprocess']['left_image_bound_to_data']
				Bag_Folder = data_dic[runs_path][run]['preprocess']['Bag_Folder']
			if left:
				cprint(d2n('\t\t\t',fname(left)))
			else:
				cprint(d2n('\t\t\t','left_image_bound_to_data.pkl missing'),'red')
			if Bag_Folder:
				cprint(d2n('\t\t\t',fname(Bag_Folder)))
			else:
				cprint(d2n('\t\t\t','Bag_Folder.pkl missing'),'red')
			cprint('')


def check_data_status(data_dic,runs_path):
	if 'bair_car_data_meta' in runs_path:
		no_separate_preprocess_dir = True
	else:
		no_separate_preprocess_dir = False
	data_dic[runs_path] = {}
	runs = sgg(opj(runs_path,'*'))
	for r in range(len(runs)):
		run = runs[r]
		run_name = fname(run)
		if run_name not in run_location_dic:
			run_location_dic[run_name] = []
		run_location_dic[run_name].append(pname(run))
		data_dic[runs_path][run_name] = {}
		bags = sgg(opj(run,'*.bag'))
		data_dic[runs_path][run_name]['bags'] = bags
		bags_pkl = sgg(opj(run,'*.bag.pkl'))
		data_dic[runs_path][run_name]['bags.pkl'] = bags_pkl		
		preprocess_path = False
		if no_separate_preprocess_dir:
			preprocess_path = run
		else:
			preprocess_path_list = sgg(opj(run,'.pre*'))
			if len(preprocess_path_list) > 0:
				preprocess_path = fname(preprocess_path_list[-1])
		if preprocess_path:
			data_dic[runs_path][run_name]['preprocess'] = {}
			left_list = sgg(opj(run,preprocess_path,'left*'))
			if len(left_list) > 0:
				left = left_list[-1]
				data_dic[runs_path][run_name]['preprocess']['left_image_bound_to_data'] = left
			else:
				data_dic[runs_path][run_name]['preprocess']['left_image_bound_to_data'] = False

			Bag_list = sgg(opj(run,preprocess_path,'Bag_Folder*'))
			if len(Bag_list) > 0:
				Bag_Folder = Bag_list[-1]
				data_dic[runs_path][run_name]['preprocess']['Bag_Folder'] = Bag_Folder
			else:
				data_dic[runs_path][run_name]['preprocess']['Bag_Folder'] = False
		else:
			data_dic[runs_path][run_name]['preprocess'] = False


		
if False:
	for dl in data_locations:
		check_data_status(data_dic,dl)
		run_name_subsets[dl] = get_run_name_subset(data_dic,dl)

	for dl in data_locations:	
		print_data_status(data_dic,dl,run_name_subsets['/media/karlzipser/bair_car_data_6/bair_car_data'])

	for run_name in run_name_subsets['/media/karlzipser/bair_car_data_6/bair_car_data']:
		#run_name = 'play_Nino_to_campus_08Oct16_09h00m00s_Mr_Blue_1b'
		run_locs = run_location_dic[run_name]
		left = []
		for rl in run_locs:
			if data_dic[rl][run_name]['preprocess']:
				if data_dic[rl][run_name]['preprocess']['left_image_bound_to_data']:
					left.append(data_dic[rl][run_name]['preprocess']['left_image_bound_to_data'])
		print left
		

	for run in sorted(run_location_dic.keys()):
		#cprint(d2n(r))
		run_locs = ['/home/karlzipser/Desktop/bair_car_data_meta'] #sorted(run_location_dic[run])
		#cprint(d2n('\t',len(run_locs)))
		BAG_FOLDER_DONE = False
		for rl in run_locs:
			if run in data_dic[rl].keys():
				if data_dic[rl][run]['preprocess']:
					if 'Bag_Folder' in data_dic[rl][run]['preprocess']:
						if data_dic[rl][run]['preprocess']['Bag_Folder']:
							BAG_FOLDER_DONE = True
							break
		if BAG_FOLDER_DONE == False:
			cprint(opj(rl,run) + ' has preprocess but lacks Bag_Folder.pkl','red')
		else:
			cprint(opj(rl,run) + ' has Bag_Folder.pkl')



	no_preprocess = []
	dl = '/media/karlzipser/bair_car_data_6/bair_car_data'#'/home/karlzipser/Desktop/bair_car_data_meta' # 
	for run in data_dic[dl]:
		if data_dic[dl][run]['preprocess']:
			cprint(d2s(run,'preprocess'))
		else:
			cprint(d2s(run,'no preprocess'),'red')
			no_preprocess.append(run)
			preprocess_bag_data(opj(dl,run))


