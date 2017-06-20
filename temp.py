def TimestampedData():
	D = {}
	D['type'] = 'TimestampedData'
	D['Purpose'] = d2s(inspect.stack()[0][3],':','Dictionary structure for holding lists of data corresponding to list of timestamps.')
	D['ts'] = []
	def _validate_timestamps():
		len_ts = len(D['ts'])
		for k in D.keys():
			if type(D[k]) == list:
				assert(len(D[k]) == len_ts)
	def _load(d):
		path = d['path']
		assert(len(gg(path))>0)
		e = zload_obj({'path':path})
		#print(d2s('e =',e))
		for k in D.keys():
			if type(D[k]) == list:
				del D[k]
		for k in e.keys():
			D[k] = e[k]
		_validate_timestamps()
	D['load'] = _load
	def _save(d):
		path = d['path']
		zsave_obj({'obj':D,'path':d['path']})
	D['save'] = _save
	return D


def Left_Image_Bound_To_Data_TS():
	D = TimestampedData()
	D['Purpose'] = d2s(inspect.stack()[0][3],':','Hold left_image_boud_to_data in TimestampedData format.\n') + D['Purpose']
	D['type'] = 'Left_Image_Bound_To_Data_TS'
	D['acc'] = []
	D['encoder'] = []
	D['gyro'] = []
	D['motor'] = []
	D['right_image'] = []
	D['state'] = []
	D['steer'] = []
	def _translate_from_left_image_bound_to_data(d):
		path = d['path']
		L=lo(path)
		D['ts'] = sorted(L.keys())
		for t in a['ts']:
			for k in L[t].keys():
				D[k].append(L[t][k])
	D['translate_from_left_image_bound_to_data'] = _translate_from_left_image_bound_to_data
  	return D


a = Left_Image_Bound_To_Data_TS()
a['translate_from_left_image_bound_to_data'](
	{'path':'/Volumes/SSD_2TB/bair_car_data_new_28April2017/meta/caffe2_z2_color_direct_local_11Apr17_15h25m02s_Mr_Silver/left_image_bound_to_data.pkl'})
a['save']({'path':opjD('meta','caffe2_z2_color_direct_local_11Apr17_15h25m02s_Mr_Silver','left_image_bound_to_data_TS')})


v = Left_Image_Bound_To_Data_TS()
v['load']({'path':opjD('meta','caffe2_z2_color_direct_local_11Apr17_15h25m02s_Mr_Silver','left_image_bound_to_data_TS')})
v['save']({'path':opjD('v')})

