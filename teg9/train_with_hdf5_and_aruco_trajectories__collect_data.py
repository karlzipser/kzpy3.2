from kzpy3.vis2 import *
from kzpy3.vis import mi_or_cv2_animate
import kzpy3.teg9.data.utils.get_data_with_hdf5 as get_data_with_hdf5
import caffe

translation_dic = {'p':'PROCESS_NUM'}

if __name__ == "__main__" and '__file__' in vars():
	argument_dictionary = args_to_dic({'pargs':sys.argv[1:]})
else:
	print('Running this within interactive python.')
	argument_dictionary = args_to_dic({'pargs':"-p 0"})

argument_dictionary = translate_args({ 'argument_dictionary':argument_dictionary,'translation_dic':translation_dic })
print(argument_dictionary)

PROCESS_NUM = int(argument_dictionary['PROCESS_NUM'])


REPO = 'kzpy3'
TEG = 'teg9'
CAF = 'caf8'
DISPLAY = True

ignore = ['reject_run','left','out1_in2','Smyth','racing','local','Tilden','campus'] # runs with these labels are ignored
require_one = ['aruco_ring'] # at least one of this type of run lable is required


if False:
	MODEL = 'z2_color'
	print(MODEL)
	bair_car_data_path = opjD('bair_car_data_new_28April2017') #opjD('bair_car_data_Main_Dataset') # opjD('bair_car_data_new')
	weights_file_path =  most_recent_file_in_folder(opjD(MODEL),['caffemodel'])
	#weights_file_path = opjh('caffe_models/z2_color.caffemodel')
	N_FRAMES = 2 # how many timesteps with images.
	N_STEPS = 10 # how many timestamps with non-image data
	gpu = 1

if True:
	MODEL = 'z2_color_aruco'
	print(MODEL)
	bair_car_data_path = opjD('bair_car_data_new_28April2017') #opjD('bair_car_data_Main_Dataset') # opjD('bair_car_data_new')
	weights_file_path =  most_recent_file_in_folder(opjD(MODEL),['caffemodel'])
	#weights_file_path = opjh('caffe_models/z2_color/z2_color.caffemodel')
	N_FRAMES = 2 # how many timesteps with images.
	N_STEPS = 10 # how many timestamps with non-image data
	gpu = 1


if False:
	MODEL = 'z2_color_small_ip1'
	print(MODEL)
	bair_car_data_path = opjD('bair_car_data_Main_Dataset') # '/media/karlzipser/ExtraDrive4/bair_car_data_new_28April2017'#opjD('bair_car_data_new')
	weights_file_path =  most_recent_file_in_folder(opjD(fname(opjh(REPO,CAF,MODEL))),['caffemodel'])
	N_FRAMES = 2 # how many timesteps with images.
	N_STEPS = 10 # how many timestamps with non-image data
	gpu = 1


if False:
	MODEL = 'z3_color'
	print(MODEL)
	bair_car_data_path = opjD('bair_car_data_Main_Dataset') # '/media/karlzipser/ExtraDrive4/bair_car_data_new_28April2017'#opjD('bair_car_data_new')
	weights_file_path = most_recent_file_in_folder(opjD(fname(opjh(REPO,CAF,MODEL))),['caffemodel'])
	#weights_file_path = opj('caffe_models/z3_color_iter_14600000.caffemodel')
	N_FRAMES = 3 # how many timesteps with images.
	N_STEPS = 30 # how many timestamps with non-image data
	gpu = 1


if False:
	MODEL = 'z1_color'
	print(MODEL)
	bair_car_data_path = '/media/karlzipser/ExtraDrive4/bair_car_data_new_28April2017'
	weights_file_path = most_recent_file_in_folder(opjD(fname(opjh(REPO,CAF,MODEL))),['caffemodel'])
	N_FRAMES = 1 # how many timesteps with images.
	N_STEPS = 10 # how many timestamps with non-image data
	gpu = 1


if False:
	CS_('load aruco trajectory data')
	Aruco_Steering_Trajectories = {}
	aruco_data_location = opjD('output_data')
	paths = sggo(aruco_data_location,'*.pkl')
	for i in range(len(paths)):
		o = paths[i]
		ast = lo(o)
		for run_name in ast.keys():	
			print(d2n(run_name,' (',i+1,' of ',len(paths),')'))
			if run_name not in Aruco_Steering_Trajectories:
				Aruco_Steering_Trajectories[run_name] = {}
			if len(ast[run_name].keys()) > 4:
				print_stars()
				continue
			for mode in ast[run_name].keys():
				print('\t'+mode)
				if mode not in Aruco_Steering_Trajectories[run_name]:
					Aruco_Steering_Trajectories[run_name][mode] = {}
				timestamps = ast[run_name][mode]['near_t']
				dd = ast[run_name][mode]['desired_direction'][0]
				print('\t\t'+str(dd))
				Aruco_Steering_Trajectories[run_name][mode][dd] = {}
				for i in range(len(timestamps)):
					t = timestamps[i]
					Aruco_Steering_Trajectories[run_name][mode][dd][t] = {}
					for topic in ast[run_name][mode].keys():
						if topic not in ['near_t','desired_direction']:
							q = ast[run_name][mode][topic][i]
							if not(is_number(q)):
								q = array(q)
								q = q.astype(np.float16)
							else:
								q = np.float16(q)
							Aruco_Steering_Trajectories[run_name][mode][dd][t][topic] = q
	
	ctr = 0
	for run_name in Aruco_Steering_Trajectories.keys():
		if 'flip_' in run_name:
			del Aruco_Steering_Trajectories[run_name]
			continue
		flip = 'flip_'+run_name
		print(d2n(flip,' (',ctr+1,' of ',len(paths),')'))
		ctr += 1
		Aruco_Steering_Trajectories[flip]= {}
		for mode in Aruco_Steering_Trajectories[run_name]:
			Aruco_Steering_Trajectories[flip][mode] = {}
			for dd in [0,1]:
				Aruco_Steering_Trajectories[flip][mode][dd] = {}
				for t in Aruco_Steering_Trajectories[run_name][mode][dd].keys():
					Aruco_Steering_Trajectories[flip][mode][dd][t] = {}
					Aruco_Steering_Trajectories[flip][mode][dd][t]['steer'] = np.float16(99-Aruco_Steering_Trajectories[run_name][mode][dd][t]['steer'])
					Aruco_Steering_Trajectories[flip][mode][dd][t]['velocity'] = np.float16(Aruco_Steering_Trajectories[run_name][mode][dd][t]['velocity'])
					l = list(Aruco_Steering_Trajectories[run_name][mode][dd][t]['other_car_inverse_distances'])
					l.reverse(); l = array(l); l = l.astype(np.float16)
					Aruco_Steering_Trajectories[flip][mode][dd][t]['other_car_inverse_distances'] = l
					l = list(Aruco_Steering_Trajectories[run_name][mode][dd][t]['marker_inverse_distances'])
					l.reverse(); l = array(l); l = l.astype(np.float16)
					Aruco_Steering_Trajectories[flip][mode][dd][t]['marker_inverse_distances'] = l
					l = list(Aruco_Steering_Trajectories[run_name][mode][dd][t]['potential_values'])
					l.reverse(); l = array(l); l = l.astype(np.float16)
					Aruco_Steering_Trajectories[flip][mode][dd][t]['potential_values'] = l

					l = list(Aruco_Steering_Trajectories[run_name][mode][dd][t]['clock_potential_values'])
					l.reverse(); l = array(l); l = l.astype(np.float16)
					Aruco_Steering_Trajectories[flip][mode][dd][t]['clock_potential_values'] = l

					if dd == 0:
						Aruco_Steering_Trajectories[flip][mode][dd][t]['desired_direction'] = 1
					else:
						Aruco_Steering_Trajectories[flip][mode][dd][t]['desired_direction'] = 0
					Aruco_Steering_Trajectories[flip][mode][dd][t]['relative_heading'] =  np.float16(360 - Aruco_Steering_Trajectories[run_name][mode][dd][t]['relative_heading'])

	unix('mkdir -p '+opjD('Aruco_Steering_Trajectories'))
	ctr = 0
	for run_name in sorted(Aruco_Steering_Trajectories.keys()):
		print(d2n(run_name,' (',ctr+1,' of ',len(paths),')'))
		so(Aruco_Steering_Trajectories[run_name],opjD('Aruco_Steering_Trajectories',run_name))
		ctr += 1
	raw_input('enter')


if True:
	print("Loading Aruco_Steering_Trajectories . . .")
	paths = sggo(opjD('Aruco_Steering_Trajectories','*.pkl'))
	Aruco_Steering_Trajectories = {}
	ctr = 0
	for p in paths:
		o = lo(p)
		run_name = fname(p).replace('.pkl','')
		print(d2n(run_name,' (',ctr+1,' of ',len(paths),')'))
		Aruco_Steering_Trajectories[run_name] = o
		ctr += 1





hdf5_runs_path = opj(bair_car_data_path,'hdf5/runs')
hdf5_segment_metadata_path = opj(bair_car_data_path,'hdf5/segment_metadata')






get_data_with_hdf5.load_Segment_Data(hdf5_segment_metadata_path,hdf5_runs_path)



print('\nloading low_steer... (takes awhile)')
low_steer = load_obj(opj(hdf5_segment_metadata_path,'low_steer'))
print('\nloading high_steer... (takes awhile)')
high_steer = load_obj(opj(hdf5_segment_metadata_path,'high_steer'))
print('done')

all_steer = high_steer+low_steer

all_steer_len = len(all_steer)
all_steer_range =  range(int(PROCESS_NUM*all_steer_len/8),1+int((PROCESS_NUM+1)*all_steer_len/8))


#wait_for_enter()


def get_data_ids(d):
	all_index = d['all_index']

	choice = all_steer[all_index]
	run_code = choice[3]
	seg_num = choice[0]
	offset = choice[1]


	run_name = get_data_with_hdf5.Segment_Data['run_codes'][run_code]
	#print run_name
	"""
	if run_name not in Aruco_Steering_Trajectories.keys():
		#print('Run name '+run_name+' not in Aruco_Steering_Trajectories')
		return None
	if len(Aruco_Steering_Trajectories[run_name].keys()) < 2:
		#print('len(Aruco_Steering_Trajectories[run_name].keys()) <= 2')
		return None
	"""
	#print 'here!'
	seg_num_str = str(seg_num)
	#aruco_matches = []
	#print(run_code,seg_num,offset,N_STEPS,offset+0,N_FRAMES)
	for i in [0]:#range(N_FRAMES):
		timestamp = get_data_with_hdf5.Segment_Data['runs'][run_name]['segments'][seg_num_str]['left_timestamp'][offset+i]
		behavioral_mode = np.random.choice(
			['Direct_Arena_Potential_Field',
 			#'Furtive_Arena_Potential_Field',
 			'Follow_Arena_Potential_Field'])
 			#'Play_Arena_Potential_Field'])
		desired_direction = np.random.choice([0,1])
		"""
		if timestamp in Aruco_Steering_Trajectories[run_name][behavioral_mode][desired_direction].keys():
			aruco_matches.append(timestamp)
		if len(aruco_matches) < 1:
			print(d2s('no aruco match',time.time()))
			return None
		"""
	data = get_data_with_hdf5.get_data(run_code,seg_num,offset,N_STEPS,offset+0,N_FRAMES,ignore=ignore,require_one=require_one,no_images=True)
	if data != None:
		data['behavioral_mode'] = behavioral_mode
		data['desired_direction'] = desired_direction
 		#for topic in Aruco_Steering_Trajectories[run_name][behavioral_mode][desired_direction][timestamp]:
 		#	data[topic] = Aruco_Steering_Trajectories[run_name][behavioral_mode][desired_direction][timestamp][topic]
 		data['id'] = (run_name,behavioral_mode,desired_direction,timestamp,run_code,seg_num,offset)

	return data


def get_data_ids2(d):
	all_index = d['all_index']

	choice = all_steer[all_index]
	run_code = choice[3]
	seg_num = choice[0]
	offset = choice[1]


	run_name = get_data_with_hdf5.Segment_Data['run_codes'][run_code]
	#print run_name
	
	if run_name not in Aruco_Steering_Trajectories.keys():
		print('Run name '+run_name+' not in Aruco_Steering_Trajectories')
		return None
	if len(Aruco_Steering_Trajectories[run_name].keys()) < 2:
		print('len(Aruco_Steering_Trajectories[run_name].keys()) <= 2')
		return None
	
	#print 'here!'
	seg_num_str = str(seg_num)
	aruco_matches = []
	#print(run_code,seg_num,offset,N_STEPS,offset+0,N_FRAMES)
	for i in [0]:#range(N_FRAMES):
		timestamp = get_data_with_hdf5.Segment_Data['runs'][run_name]['segments'][seg_num_str]['left_timestamp'][offset+i]
		behavioral_mode = np.random.choice(
			['Direct_Arena_Potential_Field',
 			#'Furtive_Arena_Potential_Field',
 			'Follow_Arena_Potential_Field'])
 			#'Play_Arena_Potential_Field'])
		desired_direction = np.random.choice([0,1])
		
		if timestamp in Aruco_Steering_Trajectories[run_name][behavioral_mode][desired_direction].keys():
			aruco_matches.append(timestamp)
		if len(aruco_matches) < 1:
			
			return None
		
	return True





timer = Timer(10)

if False:
	data_id_dic = {}
	

	print((PROCESS_NUM,min(all_steer_range),max(all_steer_range)))

	for i in all_steer_range:
		if i >= all_steer_len:
			continue
		data = get_data_ids({ 'all_index':i })
		if data == None:
			data_id_dic[i] = None
		else:
			data_id_dic[i] = data['id']
		if timer.check():
			print(len(data_id_dic))
			timer.reset()

	unix('mkdir -p '+opjD('data_id_dics'))
	so(data_id_dic,opjD('data_id_dics',d2n(PROCESS_NUM,'.pkl')))

	finished()

ctr = 0
data_id_dic = {}
paths = sggo(opjD('data_id_dics','*.pkl'))
for p in paths:
	print p
	d = lo(p)
	for k in d.keys():
		data_id_dic[k] = d[k]
"""
for k in data_id_dic.keys():
	if timer.check():
		print(k,time.time())
		timer.reset()
	if data_id_dic[k] != None:
		q = get_data_ids2({ 'all_index':i })
		if q == None:
			data_id_dic[i] = None
			ctr += 1
			print(d2s('no aruco match',time.time(),i,ctr))
"""
data_id_dic2 = {}
for k in data_id_dic.keys():
	if data_id_dic[k] != None:
		data_id_dic2[k] = data_id_dic[k]

so(opjD('data_id_dic.pkl'),data_id_dic2)

