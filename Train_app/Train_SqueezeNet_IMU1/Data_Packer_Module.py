from Parameters_Module import *

L = h5r(opjD('bdd_car_data_Sept2017_aruco_demo/h5py/Mr_Black_2017-09-02-13-42-50/left_timestamp_metadata.h5py'))
O = h5r(opjD('bdd_car_data_Sept2017_aruco_demo/h5py/Mr_Black_2017-09-02-13-42-50/original_timestamp_data.h5py'))


def Data_Packer(**Args):




	for we_are in ["the setup section"]:

		_ = {}
		_[CTR] = 0

	for we_are in ['function definitions']:





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

				for i in range(6*P[N_FRAMES]):
					img = O['left_image']['vals'][_[CTR]][:,:,1]	# i.e., (94, 168)
					img = np.expand_dims(img,axis=2)				# i.e., (94, 168, 1)
					list_of_images.append( img )
					_[CTR] += 1

				list_of_meta_data_floats_or_arrays=[0.0]
				steer = L['steer'][_[CTR]:_[CTR]+P[N_STEPS]]/99.
				motor = L['motor'][_[CTR]:_[CTR]+P[N_STEPS]]/99.
				list_of_target_floats_or_lists = list(steer) + list(motor)
				return name,list_of_images,list_of_meta_data_floats_or_arrays,list_of_target_floats_or_lists




	for we_are in ['the place where we name the functions']:

		_[NEXT] = _next



	for we_are in ['the return section.']:
	
		return _


