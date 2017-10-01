from Parameters_Module import *


P = {}
P[N_STEPS] = 10
P[N_FRAMES] = 2


def hdf5_file_is_open(F):
	try:
		l = len(F.keys())
		return True
	except:
		return False


def Run(**Args):
	_ = {}
	_[L_PATH] = opj(Args[PATH],'left_timestamp_metadata_right_ts.h5py')
	_[O_PATH] = opj(Args[PATH],'original_timestamp_data.h5py')
	def _open():
		assert(not hdf5_file_is_open(_[L_PATH]))
		assert(not hdf5_file_is_open(_[O_PATH]))
		_[L] = h5r(_[L_PATH])
		_[O] = h5r(_[O_PATH])
		_[INDX] = 0
	def _close():
		assert(hdf5_file_is_open(_[L_PATH]))
		assert(hdf5_file_is_open(_[O_PATH]))
		_[L].close()
		_[O].close()
		_[INDX] = 0
	def _read(**Args):
		if _[INDX] >= len(_[L]['ts'])-P[N_STEPS]: 
			_close()
			return None
		Data = {}
		for t in Args[TOPICS]:
			if t not in [LEFT,RIGHT]:
				Data[t] = _[L][t][_[INDX]:_[INDX]+P[N_STEPS]]
			else:
				Data[t] = _[O][t]['vals'][_[INDX]:_[INDX]+P[N_FRAMES]]
		_[INDX] += 1
		return Data
	_[OPEN] = _open
	_[CLOSE] = _close
	_[READ] = _read
	return _


r = Run(PATH=opjD('bdd_car_data_Sept2017_aruco_demo/h5py/Mr_Yellow_2017-09-15-21-10-14'))
r[OPEN]()
r[READ](TOPICS=['steer','motor'])


def Data_Packer(**Args):

	for we_are in ['the setup section']:

		_ = {}
		_[BATCH_NUM] = 0
		_[L_H5PY] = None
		_[O_H5PY] = None
		_[RUN_PATHS] = sgg(Args[H5PY_PATH])
		random.shuffle(_[RUN_PATHS])
		_[BATCH_FILES] = {}
		for i in range(P[BATCH_SIZE]):
			_[BATCH_FILES][i] = {}
			_[BATCH_FILES][i][PATH] = _[RUN_PATHS][i]
			_[BATCH_FILES][i][L_H5PY] = h5r(opj(_[BATCH_FILES][i][PATH],'left_timestamp_metadata.h5py'))
			_[BATCH_FILES][i][O_H5PY] = h5r(opj(_[BATCH_FILES][i][PATH],'original_timestamp_data.h5py'))
			_[BATCH_FILES][i][CTR] = 0

	for we_are in ['function definitions']:


		def _next_files():
			if not hdf5_file_is_open(_[L_H5PY]):
				assert(not hdf5_file_is_open(_[O_H5PY]))
				spd2s('not hdf5_file_is_open(_[O_H5PY])')
				_[L_H5PY] = h5r(opjD('bdd_car_data_Sept2017_aruco_demo/h5py/Mr_Black_2017-09-02-13-42-50/left_timestamp_metadata.h5py'))
				_[O_H5PY] = h5r(opjD('bdd_car_data_Sept2017_aruco_demo/h5py/Mr_Black_2017-09-02-13-42-50/original_timestamp_data.h5py'))
			return _[L_H5PY], _[O_H5PY]


		def _next():

			L,O = _next_files()

			name='name'

			if _[CTR] >= len(L['ts'])-7*P[N_FRAMES]: # note constant, 7
				L.close()
				O.close()
				_[CTR] = 0
				return _next()
			else:
				list_of_images = []

				for i in range(6*P[N_FRAMES]):  # note constant, 6
					ctr = _[BATCH_FILES][_[BATCH_NUM][CTR]
					img = O['left_image']['vals'][ctr][:,:,1]	# i.e., (94, 168)
					img = np.expand_dims(img,axis=2)				# i.e., (94, 168, 1)
					list_of_images.append( img )
					_[BATCH_FILES][_[BATCH_NUM]][CTR] += 1

				list_of_meta_data_floats_or_arrays=[0.0]
				steer = L['steer'][_[BATCH_NUM]][CTR]]:_[BATCH_NUM]][CTR]+P[N_STEPS]]/99.
				motor = L['motor'][_[BATCH_NUM]][CTR]]:_[BATCH_NUM]][CTR]+P[N_STEPS]]/99.
				list_of_target_floats_or_lists = list(steer) + list(motor)
				_[BATCH_NUM] += 1
				if _[BATCH_NUM] >= P[BATCH_SIZE]:
					_[BATCH_NUM] = 0
				return name,list_of_images,list_of_meta_data_floats_or_arrays,list_of_target_floats_or_lists




	for we_are in ['the place where we name the functions']:

		_[NEXT] = _next



	for we_are in ['the return section.']:
	
		return _


