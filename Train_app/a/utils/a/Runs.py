#from Parameters_Module import *


P = {}
P[N_STEPS] = 10
P[N_FRAMES] = 2
P[DATA_PATH] = opjD('bdd_car_data_Sept2017_aruco_demo')
P[BATCH_SIZE] = 10

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
	def _open():
		assert(not hdf5_file_is_open(_[L_PATH]))
		assert(not hdf5_file_is_open(_[O_PATH]))
		_[L] = h5r(_[L_PATH])
		_[O] = h5r(_[O_PATH])
		_[INDX] = 0
	def _close():
		assert(hdf5_file_is_open(_[L]))
		assert(hdf5_file_is_open(_[O]))
		_[L].close()
		_[O].close()
		_[INDX] = 0
	def _read(**Args):
		if _[INDX] >= len(_[L]['ts'])-P[N_STEPS]: 
			_close()
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
		_[INDX] += 1
		return Data
	_[OPEN] = _open
	_[CLOSE] = _close
	_[READ] = _read
	return _





def Runs():
	_ = {}
	_[ALL] = {}
	_[PATHS_OF_BATCHED] = {}	

	def _free_run_to_batch():
		free_runs = list(set(_[ALL].keys()) - set(_[PATHS_OF_BATCHED].keys()))
		r = np.random.choice(free_runs)
		_[PATHS_OF_BATCHED][r] = True
		_[SORTED_PATHS_OF_BATCHED] = sorted(_[PATHS_OF_BATCHED])
		_[ALL][r][OPEN]()

	all_run_paths = sggo(P[DATA_PATH],'h5py','*')
	for r in all_run_paths:
		if len(sggo(r,'left_timestamp_metadata_right_ts.h5py'))==1:
			_[ALL][r] = Run(PATH=r)
			pd2s('use',r)
		else:
			pd2s('not',r)

	for i in range(P[BATCH_SIZE]):
		_free_run_to_batch()

	return _


runs = {}
runs[RUNS] = Runs()

