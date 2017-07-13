

path = '/Volumes/SSD_2TB/bair_car_data_new_28April2017/hdf5/runs/caffe_direct_rewrite_test_24Apr17_14h07m06s_Mr_Blue.hdf5'

def yprint(s,verbose):
	if verbose:
		cprint(s,'yellow')
VERBOSE = True

def Timeseries_Segments_hdf5(d):
	D = {}
	D['path'] = d['path']
	True
	D['type'] = 'Timeseries_Segments_hdf5'
	D['Purpose'] = d2s(inspect.stack()[0][3],':','Interface for loading timeseries segments from hdf5')
	def _load_hdf5(d):
		path = d['path']
		True
		F = h5py.File(path)
		Lb = F['labels']
		S = F['segments']
		return Lb,S
	def _load():
		# remember timestamp name
		labels,segments = _load_hdf5({'path':D['path']})
		True
		D['labels'] = {}
		for q in labels.keys():
			D['labels'][q] = labels[q]
		D['segments'] = {}
		D['timestamp_dic'] = {}
		yprint(d2s('Loading',path,'. . .'),VERBOSE)
		for q in segments.keys():
			q_int = int(q)
			D['segments'][q_int] = segments[q]
			timestamps = segments[q]['left_timestamp']
			for i in range(len(timestamps)):
				D['timestamp_dic'][timestamps[i]] = [q_int,i]
		D['data_names'] = segments[q].keys()
		yprint(d2s('. . . done.'),VERBOSE)
	def _get(d):
		label_name = None
		segment_num = None
		if 'label' in d:
			label_name = d['label']
		if 'segment' in d:
			segment_num = d['segment']
		assert(not(label_name == None and segment_num == None))
		assert(not(label_name != None and segment_num != None))
		True
		if label_name != None:
			return D['labels'][label_name][0]
		elif segment_num != None:
			return D['segments'][segment_num]
	D['get'] = _get
	_load()
	return D

TS = Timeseries_Segments_hdf5({'path':path})
zd_set(TS)
zd()
a = TS['get']({'label':'aruco_ring'})
b = TS['get']({'segment':1})



def run_name_from_path(d):
	path = d['path']
	True
	return (fname(path).split('.'))[0]

F = h5py.File(path)
timer = Timer(0)
for q in [F['segments']['0']]:
	for i in range( len(F['segments']['0']['steer']) ):
		s = F['segments']['0']['steer'][i]
print timer.time()
timer = Timer(0)
for q in [F['segments']['0']]:
	steer = F['segments']['0']['steer']
	s = steer[i]
print timer.time()

so(np.array(steer),opjD('steer'))
timer = Timer(0)
ss = lo(opjD('steer'))
timer.time()

F = h5py.File(path)
F['segments']['0']['steer'][199]

run_name = run_name_from_path({'path':path})

D = {}
D[run_name] = h5py.File(path)
D[run_name]['segments']['0']['steer'][199]


Names = ['dic','name','test','first','second','INIT_DONE']
for l in Names:
	exec(d2n(l,'=',"'",l,"'"))
Globals = {}
g = Globals
g[INIT_DONE] = True

def dic_exec_str():
	return """
d = args_to_dictionary(args)
for k in keys:
	if type(k) == str:
		assert(k in d)
		exec(k+'='+"'"+k+"'")
	elif type(k) == list:
		exec(k[0]+'='+"'"+k[0]+"'")
		if k[0] not in d:
			d[k[0]] = k[1]
			"""





def fun2(*args):
	keys = [first,[second,2]]
	exec(dic_exec_str())
	if True:
		print(d[first]-d[second])
		for k in sorted(d.keys()):
			print(d2s(k,':',d[k]))
	return d



def nice_print_dic(*args):
	keys = ['dic',['name','no name']]
	exec(dic_exec_str())
	if True:
	    pd2s(name,':',d[name])
	    sk = sorted(d[dic].keys())
	    for k in sk:
	        pd2s(tb,k,'=',d[dic][k])
	    print('')






def fun(*args):
	keys = ['first',['second',2]]
	d = args_to_dictionary()
	for k in keys:
		if type(k) == str:
			assert(k in d)
			exec(k+'='+"'"+k+"'")
		elif type(k) == list:
			exec(k[0]+'='+"'"+k[0]+"'")
			if k[0] not in d:
				d[k[0]] = k[1]
	if True:
		print(d[first])
		print(d[second])
		print(d.keys())













