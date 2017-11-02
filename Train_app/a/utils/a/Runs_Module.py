from Parameters_Module import *

"""
P = {}
P[N_STEPS] = 10
P[N_FRAMES] = 2
P[DATA_PATH] = opjD('bdd_car_data_Sept2017_aruco_demo')
P[BATCH_SIZE] = 10
"""
def hdf5_file_is_open(F):
	try:
		l = len(F.keys())
		return True
	except:
		return False




def Run(**Args):
	_ = {}
	_[PATH] = Args[PATH]
	_[L_PATH] = opj(_[PATH],'left_timestamp_metadata_right_ts.h5py')
	_[O_PATH] = opj(_[PATH],'original_timestamp_data.h5py')
	_[RIGHT_TIMESTAMP_INDEX_DIC] = lo(opj(_[PATH],'right_timestamp_index_dic.pkl'),noisy=False)
	_[INDX] = -1
	_[OUTPUT] = {}
	def _usable_length():
		return len(_[L]['ts'])-P[N_STEPS]
	def _open(**Args):
		assert(not hdf5_file_is_open(_[L_PATH]))
		assert(not hdf5_file_is_open(_[O_PATH]))
		_[L] = h5r(_[L_PATH])
		_[O] = h5r(_[O_PATH])
		_[INDX] = max(0,int(np.random.randint(_[USABLE_LENGTH]()-30*P[SEGMENT_SECONDS]-P[N_FRAMES])))
		_[STOP] = _[INDX]+30*P[SEGMENT_SECONDS]
		spd2s('opening',_[PATH])
		print _[INDX]
	def _close():
		assert(hdf5_file_is_open(_[L]))
		assert(hdf5_file_is_open(_[O]))
		_[L].close()
		_[O].close()
		_[INDX] = -1
		spd2s('closing',_[PATH])
	def _read(**Args):
		if INDX in Args:
			_[INDX] = Args[INDX]
		if _[INDX] >= _[USABLE_LENGTH]() or _[INDX] >= _[STOP]:  #len(_[L]['ts'])-P[N_STEPS]:
			_[INDX] = -1
			_close()
			spd2s('read 1: _close()')
			return None
		Data = {}
		for t in Args[TOPICS]:
			if t not in ['left_image','right_image']:
				Data[t] = _[L][t][_[INDX]:_[INDX]+P[N_STEPS]]
			elif t == 'left_image':
				Data[t] = _[O][t]['vals'][_[INDX]:_[INDX]+P[N_FRAMES]]
			elif t == 'right_image':
				right_ts = _[L]['right_ts'][_[INDX]]
				right_index = _[RIGHT_TIMESTAMP_INDEX_DIC][right_ts]
				Data[t] = _[O][t]['vals'][right_index:right_index+P[N_FRAMES]]
			else:
				assert(False)
		_[INDX] += 1 #!!!!!!!!!!!!!!
		if _[INDX] >= _[USABLE_LENGTH]() or _[INDX] >= _[STOP]:  #len(_[L]['ts'])-P[N_STEPS]:
			_[INDX] = -1
			_close()
			spd2s('read 2: _close()')
		return Data
	_[USABLE_LENGTH] = _usable_length
	_[OPEN] = _open
	_[CLOSE] = _close
	_[READ] = _read
	return _








def Runs():
	_ = {}
	_[ALL] = {}	
	_[OPEN_RUN_PATHS] = None
	_[OPEN_RUN_PATHS_INDEX] = -1
	all_run_paths = sggo(P[DATA_PATH],'h5py','*')
	for r in all_run_paths:
		if len(sggo(r,'left_timestamp_metadata_right_ts.h5py')) == 1:
			_[ALL][r] = Run(PATH=r)
			pd2s('use',r)
		else:
			pd2s('not',r)

	def _get_list_of_open_and_closed_run_paths():
		o,c = [],[]
		for k in _[ALL].keys():
			if _[ALL][k][INDX] < 0:
				c.append(k)
			else:
				o.append(k)
		return o,c

	def _insure_correct_number_of_runs_are_open():
		o,c = _get_list_of_open_and_closed_run_paths()
		if len(o) < P[BATCH_SIZE]:
			np.random.shuffle(c)
			for i in range(P[BATCH_SIZE]-len(o)):
				A_run = _[ALL][c[i]]
				A_run[OPEN]()
				o.append(c[i])
		np.random.shuffle(o)
		_[OPEN_RUN_PATHS] = o
		_[OPEN_RUN_PATHS_INDEX] = 0

	def _get_run():
		r = _[OPEN_RUN_PATHS][_[OPEN_RUN_PATHS_INDEX]]
		_[OPEN_RUN_PATHS_INDEX] += 1
		return _[ALL][r]

	_[INSURE_CORRECT_NUMBER_OF_RUNS_ARE_OPEN] = _insure_correct_number_of_runs_are_open
	_[GET_RUN] = _get_run

	return _





