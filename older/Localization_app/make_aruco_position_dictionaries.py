from Parameters_Module import *

if True:
	#car = Args['CAR'] #'Mr_Black'
	for car in P['CAR_LIST']:
		h5py_data_folder = Args['H5PY'] #'/home/karlzipser/Desktop/all_aruco_reprocessed/full_raised_observer/h5py'
		runs = []
		all_runs_ = sggo(h5py_data_folder,'*')
		for r in all_runs_:
			if car in r:
				if fname(r)[0] == 'M':
					if car+'_2' in r:
						runs.append(r)
				else:
					runs.append(r)
		pprint(runs)
		topics = ['aruco_position_x','aruco_position_y','aruco_heading_x','aruco_heading_y']
		All_100ms_data = {}
		for topic in topics:
			All_100ms_data[topic] = {}
		for r in runs:
			print r
			Data_100ms = {}
			if len(sggo(r,'aruco_position.h5py')) > 0:
				F = h5r(opj(r,'aruco_position.h5py'))
				TS_100ms = {}
				for t in F['ts']:
					TS_100ms[dp(t,1)] = True
				Data_100ms['ts'] = sorted(TS_100ms.keys())
				for topic in topics:
					print topic, len(Data_100ms['ts']),len(F['ts'][:]),len(F[topic][:])
					Data_100ms[topic] = np.interp(Data_100ms['ts'],F['ts'][:len(F[topic][:])],F[topic][:])
				for topic in topics:
					for i in rlen(Data_100ms[topic]):
						All_100ms_data[topic][Data_100ms['ts'][i]] = Data_100ms[topic][i]
				F.close()
		unix('mkdir -p '+opj(pname(h5py_data_folder),'aruco_position_dictionaries'))
		so(opj(pname(h5py_data_folder),'aruco_position_dictionaries',car+'_aruco_position_dictionary'),All_100ms_data)
	
print('Done!')

#EOF
if False:
	aruco_position_dictionaries_src_path = '/home/karlzipser/Desktop/all_aruco_reprocessed/full_raised_observer/aruco_position_dictionaries'
	aruco_position_dictionaries_dst_path = '/home/karlzipser/Desktop/all_aruco_reprocessed/full_raised/aruco_position_dictionaries'
	dics = sggo(aruco_position_dictionaries_src_path,'*.pkl')
	pprint(dics)
	for d in dics:
		unix_str = d2s('ln -s',d,opj(aruco_position_dictionaries_dst_path,fname(d).replace('.pkl','_observer.pkl')))
		print unix_str
		unix(unix_str,False)