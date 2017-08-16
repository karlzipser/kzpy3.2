

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


def names_exec_str(*args):
	keys = ['names']
	exec(dic_exec_str())
	if True:
		print(da(d,first)-da(d,second))
		#print(d[first]-d[second])
		for k in sorted(d.keys()):
			print(d2s(k,':',d[k]))
	return d

equals = 'equals__'
nothing = 'nothing__'



def da(*args):
	"""
	# da = dictionary access
	# e.g.,
	W={1:{2:{3:4},100:[1,2,3]}}
	print(W)
	print(da(W,1,2))
	da(W,1,2,equals,9)
	print(W)
	print(da(W,1,2))
	da(W,1,100,equals,1000)
	print(W)
	print(da(W,1,100))
	"""
	Q = args[0]
	assert(type(Q)==dict)
	range_end = len(args)
	right_hand_side = nothing
	if len(args) > 3:
		if args[-2] == equals:
			right_hand_side = args[-1]
			range_end = len(args)-2
	for i in range(1,range_end):
		k = args[i]
		assert(type(k) in [str,int,long,bool,float,tuple])
		if k not in Q:
			Q[k] = {}
		if i == range_end-1:
			if right_hand_side != nothing:
				Q[k] = right_hand_side
				return
		Q = Q[k]
	return Q



def fun2(*args):
	keys = ['first',['second',2]]
	exec(dic_exec_str())
	if True:
		print(da(d,first)-da(d,second))
		#print(d[first]-d[second])
		for k in sorted(d.keys()):
			print(d2s(k,':',d[k]))
	return d

V = {}
W={1:{2:{3:4}}} 
V['W'] = W
def nice_print_dic(*args):
    if len(args) == 1 and type(args[0]) == dict:
        d = args[0]
    else:
        d = args_to_dictionary(args) # note, different from args_to_dic(d) !
    dic = d['dic']
    if type(dic) == str:
    	name = dic
    	dic = V[dic]
    elif 'name' in d:
        name = d['name']
    else:
        name = False
    if True:
        if name != 'False':
            pd2s(name,':')
        sk = sorted(dic.keys())
        for k in sk:
            pd2s(tb,k,':',dic[k])
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













