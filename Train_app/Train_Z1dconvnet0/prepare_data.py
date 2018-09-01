
from kzpy3.vis3 import *
exec(identify_file_str)

clear_screen()
#python kzpy3/Train_app/Train_Z1dconvnet0/prepare_data.py
P = {}
P['num_input_timesteps'] = 60
P['plot individual run data'] = False
P['plot concatenated run data'] = False
P['input_indicies'] = na(range(-P['num_input_timesteps'],0))
P['target_index_range'] = na(range(0,30,3))
P['timeindex_offset'] = 0
if using_linux():
	P['dataset path'] = '/media/karlzipser/rosbags/flex_sensors_Aug2018'
else:
	P['dataset path'] = '/Volumes/transfer/flex_sensors_Aug2018/'
P['good_timestep_proportion'] = 0.8
P['processed data location'] = 'Train_app/Train_Z1dconvnet0/__local__/'

list_of_h5py_folders = sggo(P['dataset path'],'*')

P['topics'] = [
	 'acc_x',
	 'acc_y',
	 'acc_z',
	 'encoder',
	 'gyro_x',
	 'gyro_y',
	 'gyro_z',
	 'cmd_steer',
	 'cmd_motor',
	 'gyro_heading_x',
	 'gyro_heading_y',
	 'gyro_heading_z',
	 'drive_mode',
	 'human_agent',
	 'motor',
	 'steer',
	 'xfc0',
	 'xfl0',
	 'xfl1',
	 'xfr0',
	 'xfr1',
	]

def get_raw_run_data(P):
	M = {}
	M_temp = {}
	for t in P['topics']:
		M[t] = na([])

	for f in list_of_h5py_folders:
		print f
		pd2s('h5py folder',f)
		runs = sggo(f,'*')
		for r in runs:
			pd2s('\t',r)
			try:
				L = h5r(opj(r,'left_timestamp_metadata_right_ts.h5py'))
				for t in P['topics']:
					M_temp[t] = L[t][:] #if topic not in file, this will raise exception, avoiding adding partial data to M.
				for t in P['topics']:
					print('adding '+t)
					M[t] = np.concatenate((M[t],M_temp[t]),axis=None)
					if P['plot individual run data']:
						figure(d2s(t,':',fname(r)));clf();plot(M[t])
				if P['plot individual run data']:
					raw_enter()
					CA()
			except:
				exec(EXCEPT_STR)
			try:
				L.close()
			except:
				exec(EXCEPT_STR)
		if P['plot individual run data']:
			for t in P['topics']:
				figure(d2s(t,': all runs'));clf();plot(M[t])
			raw_enter()
			CA()
	L={}
	
	for t in P['topics']:
		if t in ['drive_mode','human_agent','cmd_steer','cmd_motor','steer','motor']:
			L[t] = M[t][:]
		else:
			L[t] = zscore(M[t][:])
	L['IMU_mag'] = 0*L['acc_x']
	for t in ['acc_x','acc_y','acc_z','gyro_x','gyro_y','gyro_z',]:
		L['IMU_mag'] += np.abs(L[t])
	L['IMU_mag'] /= 6.0
	a_topic = a_key(L)
	for t in P['topics']:
		pd2s('len(L[t] =',len(L[t]))
		assert len(L[t]) == len(L[a_topic])

	if P['plot concatenated run data']:
		for t in P['topics']:
			figure(d2s(t,': all runs'));clf();plot(L[t])
		raw_enter()
		CA()
	return L,M

from kzpy3.misc.progress import ProgressBar

def Progress_animator(total_count,update_Hz=1.0):
	D = {}
	#print 'AAA'
	D['progress'] = ProgressBar(total_count) 
	D['progress timer'] = Timer(1.0/(1.0*update_Hz))
	def _update_function(current_count):
		#print 'BBB'
		if True:
			if D['progress timer'].check():
				#print 'CCC'
				assert current_count < total_count+1
				D['progress'].animate(current_count)
				D['progress timer'].reset()
			else:
				pass#time.sleep(0.1)
		else:#except Exception as e:
			pass
	D['update'] = _update_function
	return D


#def max_steer_or_motor_value(target_array):
#	return np.max(np.abs(target_array-49))
def max_felx_signal(index_range,L):
	max_sig = -5
	for t in [
		'xfc0',
		'xfl0',
		'xfl1',
		'xfr0',
		'xfr1',]:
		msig = np.max(L[t][index_range])
		if msig > max_sig:
			max_sig = msig
	return max_sig


def get_good_input_time_indicies(L):
	Pb = Progress_animator(total_count=len(L[P['topics'][0]]),update_Hz=10)
	good_input_time_indicies = []
	max_sig_values = []
	i = 0
	for i in range(len(L[P['topics'][0]])):
		try:
			good_count = 0
			for j in range(i-P['num_input_timesteps'],i):
				if L['drive_mode'][j] > 0:
					if L['human_agent'][j] < 1:
						if (L['motor'][j]-49) < 5:
							#print 'no motor'
							#if np.abs(L['steer'][j]-49) < 5:
								#pd2s(j,int(L['steer'][j]),int(L['motor'][j]),good_count)
							good_count += 1
							Pb['update'](i)
				#print i,j,good_count
			#print good_count/(1.0*P['num_input_timesteps'])
			if good_count/(1.0*P['num_input_timesteps']) > P['good_timestep_proportion']:
				max_sig_values.append([i,max_felx_signal(i+P['target_index_range'],L)])
				#good_input_time_indicies.append(i)

				#max_motor_values.append(max_steer_or_motor_value(L['motor'][i+P['target_index_range']]))
				#pd2s(i,'succeeded')
			#pd2s(i,'failed')
		except:
			exec(EXCEPT_STR)
	Pb['update'](i);print('\n')
	#assert len(good_input_time_indicies) == len(max_sig_values)
	return max_sig_values

"""
def display_data(L,i,P):
	figure(d2s('data'))
	title(i)
	clf()
	xylim(0,90,-50,100)
	for t in [
		'motor',
		'steer',
		'IMU_mag',
		'xfc0',
		'xfl0',
		'xfl1',
		'xfr0',
		'xfr1',
	]:
	 	if t[0] == 'x':
	 		color = 'k'
	 	elif t == 'motor':
	 		color = 'b'
	 	elif t == 'steer':
	 		color = 'r'
	 	elif t == 'IMU_mag':
	 		color = 'g'
	 	vals = L[t][i-P['num_input_timesteps']/2:i+P['num_input_timesteps']/2+30]
	 	if t == 'IMU_mag':
	 		vals = 3*vals-20
	 	plot(vals,color)
	spause()

def display_data2(L,i,P):
	figure(d2s('data2'))
	clf()
	title(i)
	xylim(np.min(P['input_indicies'])-3,np.max(P['target_index_range'])+3,-50,100)

	for input_target in [0,1]:
		if input_target == 0:
			
			indicies = P['input_indicies']
		else:
			lst = 
			indicies = P['target_index_range']			
		for t in lst:
		 	if t[0] == 'x':
		 		color = 'k'
		 	elif t == 'motor':
		 		color = 'b'
		 	elif t == 'steer':
		 		color = 'r'
		 	elif t == 'IMU_mag':
		 		color = 'g'
		 	else:
		 		color = 'c'
		 	vals = L[t][i+indicies]
		 	if t == 'IMU_mag':
		 		vals = 3*vals-20
		 	plot(indicies,vals,color+'.-')
	spause()

"""

P['input_lst'] = [
	'IMU_mag',
	'encoder',
	'cmd_steer',
	'cmd_motor',
	'motor',
	'steer',
	'xfc0',
	'xfl0',
	'xfl1',
	'xfr0',
	'xfr1',
]
P['target_lst'] = [
	'motor',
	'steer',
]
def display_data3(D,P):
	figure(d2s('data3'))
	clf()
	title(i)
	xylim(np.min(P['input_indicies'])-3,np.max(P['target_index_range'])+3,-50,100)

	for input_target in [0,1]:
		for input_target in ['input','target']:	
			if input_target == 'input':
				indicies = P['input_indicies']
			else:
				indicies = P['target_index_range']
			for t in D[input_target].keys():
			 	if t[0] == 'x':
			 		color = 'k'
			 	elif t == 'motor':
			 		color = 'b'
			 	elif t == 'steer':
			 		color = 'r'
			 	elif t == 'IMU_mag':
			 		color = 'g'
			 	else:
			 		color = 'c'
			 	vals = D[input_target][t]

			 	plot(indicies,vals,color+'.-')
	spause()


def get_input_output_data(L,i,P):
	D = {}

	for input_target in ['input','target']:
		D[input_target] = {}
		if input_target == 'input':
			lst = P['input_lst']
			indicies = P['input_indicies']
		else:
			lst = P['target_lst']
			indicies = P['target_index_range']		
		for t in lst:
			D[input_target][t] = L[t][i+indicies]
	return D

def display_data_animate(L,i,n,P):
	CA()
	for i in range(i-n,i+n,1):
		D = get_input_output_data(L,i,P)
		display_data3(D,P)
		#time.sleep(1)

try:
	L = lo(opjk(P['processed data location'],'L.pkl'))
	M = lo(opjk(P['processed data location'],'M.pkl'))
	pd2s('loaded L and M')
except:
	#exec(EXCEPT_STR)
	pd2s('making and saving L and M')
	L,M=get_raw_run_data(P)
	so(L,opjk(P['processed data location'],'L.pkl'))
	so(M,opjk(P['processed data location'],'M.pkl'))	
try:
	I = lo(opjk(P['processed data location'],'I.pkl'))
	pd2s('loaded I')
except:
	#exec(EXCEPT_STR)
	pd2s('making and saving I')
	max_sig_values = get_good_input_time_indicies(L)
	I = {}
	max_sig_values = na(max_sig_values)
	sig_sorted = max_sig_values[max_sig_values[:,1].argsort()]
	I['max_sig_values'] = max_sig_values
	I['sig_sorted'] = sig_sorted
	so(I,opjk(P['processed data location'],'I.pkl'))

if False:
	for i in range(100): display_data_animate(L,int(sig_sorted[-np.random.randint(30000),0]),10,P)


"""
find_timer = Timer(1/10000.0)
epoch_num = 0
while True:
	try:
		epoch_num += 1
		CS_(d2s('starting epoch',epoch_num))
		Time_indicies = range(P['timeindex_offset']+num_input_timesteps,len(L['encoder'][:])-num_input_timesteps)
		while len(Time_indicies) > 280000:#batch_size:
			batch = 0
			while batch < batch_size:
				i = np.random.randint(len(Time_indicies))
				time_index = Time_indicies[i]

				target_motor = list(L['motor'][time_index+P['target_index_range']])
				target_steer = list(L['steer'][time_index+P['target_index_range']])
				if (( max(abs(target_steer)) > 0.75) or (max(abs(target_motor)) > 0.75)) or (np.random.randint(10)<1):
					assert(len(target_motor)==10)
					assert(len(target_steer)==10)
					the_target[batch,0:20,0]=torch.from_numpy(na(target_steer+target_motor))
					_topic_ctr = 0
					for t in P['topics']:
						the_input[batch,_topic_ctr,:] = torch.from_numpy(L[t][(-num_input_timesteps+time_index):time_index])
						_topic_ctr += 1
					del Time_indicies[i]
					batch += 1
				find_timer.reset()
			freq = rate_counter.freq(do_print=False)
			if freq != False:
				pd2s(batch_size*freq,'Hz')
			#print type(the_input),type(the_target),type(Network['forward'])

			Network['forward'](the_input,the_target)

			Network['backward']()

			Network['save net']()

			if display_timer.check():
				print len(Time_indicies)
				figure(1);clf();ylim(-6,6);plot(target_steer,'r:');plot(target_motor,'b:');
				the_output = Network['net'].C['output'][0].data.cpu().numpy()
				output_steer = the_output[0:10]
				output_motor = the_output[10:20]
				plot(output_steer,'r.-')
				plot(output_motor,'b.-')
				spause()
				display_timer.reset()
				#if display_timer3.check():
				for l in ['input','conv1/relu','conv2/relu','conv3']:#,'ip1']:
					n = Network['net'].C[l][0].data.cpu().numpy()
					mi(z2o(n),l)
				plt.pause(0.1)
				spause()
				display_timer3.reset()

	except KeyboardInterrupt:
		#P['ABORT'] = True
		exec(EXCEPT_STR)
		break
	except Exception as e:
		pd2s("Main.py Exception",e)
		exec(EXCEPT_STR)

CS_('done.')
"""
def get_print_exec_str(List_of_names):
	s = """ \b"pd2s("""
	for l in List_of_names:
		s += d2n("'",l," = ',",l,',')
	s += """ )" """
	return s




#EOF

