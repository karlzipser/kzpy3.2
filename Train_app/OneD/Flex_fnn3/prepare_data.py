
from kzpy3.vis3 import *
#from default_values import *
from kzpy3.Train_app.OneD.Flex_fnn3.default_values import *
exec(identify_file_str)

clear_screen()

list_of_h5py_folders = sggo(P['path/dataset path.'],'*')

def get_raw_run_data(P):
	M = {}
	M_temp = {}
	for t in P['dat/topics.']:
		M[t] = na([])
	Smoothing_values = {'data':0.9999,'baseline':0.9999}
	print Smoothing_values
	for f in list_of_h5py_folders:
		print f
		pd2s('h5py folder',f)
		runs = sggo(f,'*')
		for r in runs:
			pd2s('\t',r)
			try:
				L = h5r(opj(r,'left_timestamp_metadata_right_ts.h5py'))
				for t in P['dat/topics.']:
					if 'baseline' in t:
						s = Smoothing_values['baseline']
					else:
						s = Smoothing_values['data']
					M_temp[t] = L[t][:] #if topic not in file, this will raise exception, avoiding adding partial data to M.
					previous_value = M_temp[t][0]
					for i in range(1,len(M_temp[t])):
						if np.abs(M_temp[t][i]) > 500:
							M_temp[t][i] = previous_value
						else:
							M_temp[t][i] = (1.0-s)*M_temp[t][i]+s*M_temp[t][i-1]
						previous_value = M_temp[t][i]
				for t in P['dat/topics.']:
					print('adding '+t)
					M[t] = np.concatenate((M[t],M_temp[t]),axis=None)
					if P['plt/plot individual run data,']:
						figure(d2s(t,':',fname(r)));clf();plot(M[t])
				if P['plt/plot individual run data,']:
					raw_enter()
					CA()
			except:
				exec(EXCEPT_STR)
			try:
				L.close()
			except:
				exec(EXCEPT_STR)
		if P['plt/plot individual run data,']:
			for t in P['dat/topics.']:
				figure(d2s(t,': all runs'));clf();plot(M[t])
			raw_enter()
			CA()
	L={}
	
	for t in P['dat/topics.']:
		if t in ['drive_mode','human_agent','cmd_steer','cmd_motor','steer','motor']:
			L[t] = M[t][:]
		else:
			L[t] = M[t][:]#zscore(M[t][:])
	L['IMU_mag'] = 0*L['acc_x']
	for t in ['acc_x','acc_y','acc_z','gyro_x','gyro_y','gyro_z',]:
		L['IMU_mag'] += np.abs(L[t])
	L['IMU_mag'] /= 6.0
	a_topic = a_key(L)
	for t in P['dat/topics.']:
		pd2s('len(L[t] =',len(L[t]))
		assert len(L[t]) == len(L[a_topic])

	if P['plt/plot concatenated run data,']:
		for t in P['dat/topics.']:
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

###start
def get_good_input_time_indicies(L):
	Pb = Progress_animator(total_count=len(L[P['dat/topics.'][0]]),update_Hz=10)
	good_input_time_indicies = []
	max_sig_values = []
	i = 0
	for i in range(len(L[P['dat/topics.'][0]])):
		try:
			good_count = 0
			for j in range(i-P['net/num input timesteps.'],i):
				if L['drive_mode'][j] > 0:
					if L['human_agent'][j] < 1:
						if (L['motor'][j]-49) < 5:
							#print 'no motor'
							#if np.abs(L['steer'][j]-49) < 5:
								#pd2s(j,int(L['steer'][j]),int(L['motor'][j]),good_count)
							good_count += 1
							#print good_count
							Pb['update'](i)
				#print i,j,good_count
			#print good_count/(1.0*P['num_input_timesteps'])
			if good_count/(1.0*P['net/num input timesteps.']) > P['dat/good timestep proportion.']:
				max_sig_values.append([i,max_felx_signal(i+P['net/target index range.'],L)])
				#print 'good'
			else:
				pass#print 'bad'
				#good_input_time_indicies.append(i)

				#max_motor_values.append(max_steer_or_motor_value(L['motor'][i+P['net/target index range.']]))
				#pd2s(i,'succeeded')
			#pd2s(i,'failed')
		except:
			exec(EXCEPT_STR)
	Pb['update'](i);print('\n')
	#assert len(good_input_time_indicies) == len(max_sig_values)
	return max_sig_values
###stop
def display_data3(D,P):
	figure(d2s('data3'))
	clf()
	title(i)
	xylim(np.min(P['net/input indicies.'])-3,np.max(P['net/target index range.'])+3,-50,100)

	for input_target in [0,1]:
		for input_target in ['input','target']:	
			if input_target == 'input':
				indicies = P['net/input indicies.']
			else:
				indicies = P['net/target index range.']
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
			lst = P['net/input lst.']
			indicies = P['net/input indicies.']
		else:
			lst = P['net/target lst.']
			indicies = P['net/target index range.']		
		for t in lst:
			D[input_target][t] = L[t][i+indicies]
	return D

def display_data_animate(L,i,n,P):
	CA()
	for i in range(i-n,i+n,1):
		D = get_input_output_data(L,i,P)
		display_data3(D,P)
		#time.sleep(1)

processed_data_location = P['path/processed data location.']


try:
	L = lo(opj(processed_data_location,'L.pkl'))
	M = lo(opj(processed_data_location,'M.pkl'))
	pd2s('loaded L and M')
except:
	#exec(EXCEPT_STR)
	pd2s('making and saving L and M')
	L,M = get_raw_run_data(P)
	so(L,opj(processed_data_location,'L.pkl'))
	so(M,opj(processed_data_location,'M.pkl'))

"""
try:
	I = lo(opj(processed_data_location,'I.pkl'))
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
	so(I,opj(processed_data_location,'I.pkl'))
"""
if False:
	for i in range(100): display_data_animate(L,int(sig_sorted[-np.random.randint(30000),0]),10,P)


def get_print_exec_str(List_of_names,_locals_):
	s = """ \b"pd2s("""
	for l in List_of_names:
		s += d2n("'",l," = ',",globals()[l],',')
	s += """ )" """
	return s




#EOF

