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

		d = zload_obj({'path':path})
		for k in D.keys():
			if type(D[k]) == list:
				del D[k]
		for k in d.keys():
			D[k] = d[k]
		_validate_timestamps()
	D['load'] = _load
	def _save(d):
		path = d['path']
		zsave_obj({'obj':D,'path':d['path']})
	D['save'] = _save
	return D


def SomeData():
	D = TimestampedData()
	D['Purpose'] = d2s(inspect.stack()[0][3],':','A specific type of dataset.\n') + D['Purpose']
	D['type'] = 'SomeData'
	D['steer'] = []
	D['motor'] = []
	D['encoder'] = []
	return D


q = SomeData()
q['ts'] = np.random.randn(5)
q['steer'] = np.random.randn(4)
q['motor'] = np.random.randn(4)
q['encoder'] = np.random.randn(4)

q['save']({'path':opjD('qq')})

#v = SomeData()
#v['load']({'path':opjD('qq')})

