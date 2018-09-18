
from kzpy3.vis3 import *
from default_values import *
#from kzpy3.Train_app.OneD.Flex_fnn3.default_values import *
exec(identify_file_str)

#clear_screen()


def get_raw_run_data(P):

	S = {}

	for smooth_type in P['dat/smoothing values']:

		S[smooth_type] = {}
		s = P['dat/smoothing values'][smooth_type]

		for f in sggo(P['path/dataset path.'],'*'):

			pd2s('h5py folder',f)

			runs = sggo(f,'*')

			M = {}

			for t in P['dat/topics.']:
				M[t] = na([])

			for r in runs:
				pd2s('\t',r)
				try:
					L = h5r(opj(r,'left_timestamp_metadata_right_ts.h5py'))
					
					M_temp = {}
					
					for t in P['dat/topics.']:
						M_temp[t] = L[t][:] #if topic not in file, this will raise exception, avoiding adding partial data to M.
						previous_value = M_temp[t][0]
						for i in range(1,len(M_temp[t])):
							if np.abs(M_temp[t][i]) > 1000:
								M_temp[t][i] = previous_value
							else:
								M_temp[t][i] = (1.0-s)*M_temp[t][i]+s*M_temp[t][i-1]
							previous_value = M_temp[t][i]
					for t in P['dat/topics.']:
						print('adding '+t)
						M[t] = np.concatenate((M[t],M_temp[t]),axis=None)
						if P['plt/plot individual run data,']:
							figure(d2s(t,smooth_type,':',fname(r)));clf();plot(M[t])
					if P['plt/plot individual run data,']:
						raw_enter()
						CA()
					S[smooth_type] = M
				except:
					exec(EXCEPT_STR)
				try:
					L.close()
				except:
					exec(EXCEPT_STR)
	
	"""	
	S['raw']['IMU_mag'] = 0*M['acc_x']
	for t in ['acc_x','acc_y','acc_z','gyro_x','gyro_y','gyro_z',]:
		S['raw']['IMU_mag'] += np.abs(L[t])
	S['raw']['IMU_mag'] /= 6.0
	"""
	

	S['baseline_corrected'] = {}
	S['thresholds'] = {}
	for t in P['dat/topics.']:
		S['baseline_corrected'][t] = S['raw'][t]-S['baseline'][t]
		if t[0] != 'x':
			print t
		else:
			S['thresholds'][t] = {}
			Pb = Progress_animator(total_count=500,update_Hz=10,message=t)
			for thresh in range(10,500,10):
				Pb['update'](thresh)
				S['thresholds'][t][thresh] = [i for i,v in enumerate(S['baseline_corrected'][t]) if v > thresh]
	S['thresholds']['x_all'] = {}
	for thresh in range(10,500,10):
		S['thresholds']['x_all'][thresh] = []
		for t in P['dat/topics.']:
			if t[0] == 'x':
				S['thresholds']['x_all'][thresh] += S['thresholds'][t][thresh]
		S['thresholds']['x_all'][thresh] = list(set(S['thresholds']['x_all'][thresh]))
	return S



def get_good_input_time_indicies(L):
	Pb = Progress_animator(total_count=len(L[P['dat/topics.'][0]]),update_Hz=10,message='good_input_time_indicies')
	good_input_time_indicies = []
	i = 0
	for i in range(len(L[P['dat/topics.'][0]])):
		try:
			good_count = 0
			for j in range(i-P['net/num input timesteps.'],i):
				if L['drive_mode'][j] > 0:
					if L['human_agent'][j] < 1:
						if (L['motor'][j]-49) < 5:
							good_count += 1
							#print good_count
							Pb['update'](i)
			if good_count/(1.0*P['net/num input timesteps.']) > P['dat/good timestep proportion.']:
				good_input_time_indicies.append(i)
			else:
				pass#print 'bad'
		except:
			exec(EXCEPT_STR)
	Pb['update'](i);print('\n')
	return good_input_time_indicies


def assemble_training_data(S):
	L = {}
	for t in [ 
		'xfc0',
		'xfl0',
		'xfl1',
		'xfr0',
		'xfr1',
		]:
		L[t] = S['baseline_corrected'][t]# + 10.0 * np.random.randn(1)
		L[t+'_flip'] = S['baseline_corrected'][P['dat/flip_topics.'][t]]# + 10.0 * np.random.randn(1)
	L['steer'] = S['raw']['steer'].copy()
	L['steer_flip'] = 99-S['raw']['steer']
	L['motor'] = S['raw']['motor'].copy()
	L['motor_flip'] = L['motor']
	#L['IMU_mag'] = S['raw']['IMU_mag'].copy()
	#L['IMU_mag_flip'] = L['IMU_mag']

	return L



def display_data3(D,P,title='data3'):
	figure(title)
	clf()
	xylim(np.min(P['net/input indicies.'])-3,np.max(P['net/target index range.'])+3,-50,100)

	#for input_target in [0,1]:
	for input_target in ['input','target']:	
		if input_target == 'input':
			indicies = P['net/input indicies.']
		else:
			indicies = P['net/target index range.']

		for t in D[input_target].keys():
			vals = D[input_target][t]
		 	if t[0] == 'x':
		 		color = 'k'
		 		vals = D[input_target][t]/10.0
		 	elif t == 'motor':
		 		color = 'b'
		 	elif t == 'steer':
		 		color = 'r'
		 	elif t == 'IMU_mag':
		 		color = 'g'
		 	else:
		 		color = 'c'
		 	#vals = D[input_target][t]

		 	plot(indicies,vals,color+'.-')
	spause()


def get_input_output_data_(L,i,P):
	D = {}
	FLIP = random.choice([0,1])
	for input_target in ['input','target']:
		D[input_target] = {}
		if input_target == 'input':
			lst = P['net/input lst.']
			indicies = P['net/input indicies.']
		else:
			lst = P['net/target lst.']
			indicies = P['net/target index range.']
		if FLIP == False:
			flip_str = ''
		else:
			flip_str = '_flip'
		for t in lst:

			rand_offset = 0
			if t[0] == 'x':

				rand_offset = np.random.randint(-200,200)# 30*np.random.rand(1)
				#print rand_offset
				#print L[t+flip_str][i+indicies][:5]
				#print (L[t+flip_str][i+indicies]+rand_offset)[:5]
				D[input_target][t] = na(L[t+flip_str][i+indicies])+rand_offset	
				#print D[input_target][t][:5]
			else:
				D[input_target][t] = L[t+flip_str][i+indicies]
	return D


def display_data_animate(L,i,n,P):
	CA()
	for i in range(i-n,i+n,10):
		D = get_input_output_data(L,i,P)
		display_data3(D,P)
		#time.sleep(1)



processed_data_location = P['path/processed data location.']

try:
	S = lo(opj(processed_data_location,'S.pkl'))
	pd2s('loaded S')
except:
	#exec(EXCEPT_STR)
	pd2s('making and saving S')
	S = get_raw_run_data(P)
	so(S,opj(processed_data_location,'S.pkl'))
try:
	I = lo(opj(processed_data_location,'I.pkl'))
	pd2s('loaded I')
except:
	#exec(EXCEPT_STR)
	pd2s('making and saving I')
	I = get_good_input_time_indicies(S['baseline_corrected'])
	so(I,opj(processed_data_location,'I.pkl'))

usable_indicies = I #list(set(I) and set(S['thresholds']['x_all'][10]))
L = assemble_training_data(S)
print len(usable_indicies),len(I),len(L['steer'])


if False:
	for i in range(100): display_data_animate(L,np.random.choice(usable_indicies),100,P)


def get_print_exec_str(List_of_names,_locals_):
	s = """pd2s("""
	for l in List_of_names:
		s += d2n("'",l," = ',",globals()[l],',')
	s += """ )"""
	return s


CS_(np.random.choice(['ready','done','finished','complete']),say_comment=False)

#EOF

