from kzpy3.vis2 import *
import get_data_moments__LCR.get_data_moments__LCR_dataset_version as get_data_moments

def make_data_moments_dics(locations_path=''):

	if True:
		#locations_path = '/home/karlzipser/Desktop/bdd_car_data_July2017_LCR/locations'
		locations = sggo(locations_path,'*')
		num_steps = 90
		for l in locations:
			location = fname(l)
			behavioral_modes = sggo(l,'*')
			for b in behavioral_modes:
				Data_Moments = []
				behavioral_mode = fname(b)
				print location,behavioral_mode
				runs = sggo(b,'h5py','*')
				for r in runs:
					run_name = fname(r)
					pd2s('\t',run_name)
					print 1,locations_path,location,behavioral_mode,run_name,num_steps
					data_moments = get_data_moments(locations_path,location,behavioral_mode,run_name,num_steps)
					Data_Moments += data_moments
					pd2s('len data_moments =',len(data_moments))
					pd2s('len Data_Moments =',len(Data_Moments))
					#raw_enter()
				so(Data_Moments,opj(b,'_data_moments_right_ts'))
				#raw_enter()		

	if False:
		steer_hist = {}
		steer_hist['center'] = []
		steer_hist['left'] = []
		steer_hist['right'] = []

		for d in Data_Moments:
			if d['behavioral_mode'] != 'center':
				print d
			steer_hist[d['behavioral_mode']].append(d['steer'])

		for b in ['center','left','right']:
			figure(b);clf();hist(steer_hist[b])

	#
	#############################################################################







	#############################################################################
	#
	#locations_path = '/media/karlzipser/2_TB_Samsung_n2_/bair_car_data_Main_Dataset_part1/locations'
	#locations_path = '/media/karlzipser/2_TB_Samsung_n2_/here/locations'
	#locations_path = '/home/karlzipser/Desktop/bdd_car_data_July2017_LCR/locations'

	locations = sggo(locations_path,'*')
	for l in locations:
		behavioral_modes = sggo(l,'*')
		for e in behavioral_modes:
			if fname(e)[0] == '_':
				spd2s('ignoring',e)
				continue
			spd2s(e)

			data_moments_folder = opj(e,'data_moments')
			
			data_moments_indexed_file = opj(e,'_data_moments_right_ts.pkl')

			data_moments = lo(data_moments_indexed_file)

			random.shuffle(data_moments)

			num_val = 0.1*len(data_moments)

			data_moments_dic = {}
			data_moments_dic['val'] = {}
			data_moments_dic['train'] = {}
			for a in ['val','train']:
				for b in ['high_steer','low_steer']:
					data_moments_dic[a][b] = []
					#unix('mkdir -p '+opj(data_moments_folder,a,b))

			ctr = 0

			for d in data_moments:

				if abs(d['steer']-49) < 5:
					steer_type = 'low_steer'
				else:
					steer_type = 'high_steer'

				if ctr < num_val:
					data_moments_dic['val'][steer_type].append(d)
				else:
					data_moments_dic['train'][steer_type].append(d)

				ctr += 1

			so(opj(e,'data_moments_dic'),data_moments_dic)
			os.remove('data_moments_indexed_file')















# EOF