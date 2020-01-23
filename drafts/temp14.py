

from kzpy3.Learn.get_data.runs import All_runs


def Clusters(similarity_function=similarity):

	path = opjD('Destkop_clusters_and_not_essential_24July2019')
	
	affinity = lo(opj(path,'affinity'))
	# np.float, shape == (1024, 1024)
	# affinity of every cluster for every other

	cluster_list = lo(opj(path,'cluster','cluster_list_25_1st_pass_11April2019_bkp.pkl'))
	# list len 1024 of lists of run-name/index pairs, one for each cluster

	runs = All_runs['validate']# + All_runs['train']

    for r in runs:

        Run_coder[run_ctr] = r

        if False:
	        H = find_files_recursively(opjD('Data'),r,DIRS_ONLY=True)

	        if len(H['paths']) == 0:
	            cr(r,'not found.')
	            continue
	        else:
	            cg(r,'found.')

        Runs[r] = {
            'original_timestamp_data':{},
            'flip_images':{},
            'left_timestamp_metadata_right_ts':{},
            'net_projections':{},
            'activations/data':{},
            'activations/indicies':{},
        }
        
        Runs[r]['original_timestamp_data'] = \
            {'path':opj(opjD('Data'),H['paths'].keys()[0],r,'original_timestamp_data.h5py'),'data':None}

        Runs[r]['flip_images'] = \
            {'path':opj(opjD('Data'),H['paths'].keys()[0],r,'flip_images.h5py'),'data':None}

        Runs[r]['left_timestamp_metadata_right_ts'] = \
            {'path':opj(opjD('Data'),H['paths'].keys()[0],r,'left_timestamp_metadata_right_ts.h5py'),'data':None}

        Runs[r]['net_projections'] = \
            {'path':opj(opjD('Data'),'Network_Predictions_projected',r+'.net_projections.h5py'),'data':None}

        Runs[r]['activations/data'] = \
            {'path':opj(pname(pname(_Runs[r])),'data',r+'.h5py'),'data':None}

        Runs[r]['activations/indicies'] = \
            {'path':opj(pname(pname(_Runs[r])),'indicies',r+'.h5py'),'data':None}

        Runs[r]['button_number'] = None
        Runs[r]['encoder'] = None

        for k in Runs[r].keys():
            if k not in [
            	'button_number',
            	'encoder',
            	'original_timestamp_data',
            	'flip_images',
            	'left_timestamp_metadata_right_ts',
            	'activations/data',
            	'activations/indicies',
            ]:
                if Runs[r][k]['data'] == None:
                    Runs[r][k]['data'] = h5r(Runs[r][k]['path'])
        if False:
	        for kk in ['button_number','encoder']:
	            if Runs[r][kk] == None:
	                Runs[r][kk] = Runs[r]['left_timestamp_metadata_right_ts']['data'][kk][:]

	        length = len(Runs[r]['original_timestamp_data']['data']['left_image']['vals'])
	        for i in range(length):
	            if Runs[r]['button_number'][i] != 4 and Runs[r]['encoder'][i] > 0.1:
	                good_list.append((run_ctr,i))

	        Runs[r]['activations/reverse-indicies'] = \
	            {'data':np.zeros(len(Runs[r]['left_timestamp_metadata_right_ts']['data']['motor']),int)-1}


	        Runs[r]['activations/indicies']['data'] = \
	            Runs[r]['activations/indicies']['data'][P['type'][1]+'.squeeze_activation']

	        u = Runs[r]['activations/indicies']['data'][:]
	        v = Runs[r]['activations/reverse-indicies']['data']
	        
	        for i in rlen(u):
	            ii = u[i].astype(int)

	            if ii < len(v) and ii > -1:
	                v[ii] = i
	            run_ctr += 1

	def _function_make_average_clusters():
		avg_list = []
		avg_img = np.zeros(shape(23,41,3))
		for i in range(1024):
			avg_img *= 0
			for j in rlen(cluster_list[i]):
				info = cluster_list[i][j]
				cluster_img = Runs[info['name']]'net_projections']['data'][info['index']]
				avg_img += cluster_img
			avg_img /= (1.0*cluster_list[i])
			avg_list.append(avg_img.astype(np.uint8))
			mi(avg_list[1]);spause();raw_enter()
		D['cluster_averages'] = avg_list
		if len(sggo(path,'cluster_averages.pkl') == 0):
			q = raw_input('save cluster_averages? y/n ')
			if q == 'y':
				cg('saving cluster_averages.pkl')
				so(opj(path,'cluster_averages.pkl'))

	def _function_find_most_similar_cluster(img,use_random=True):
		similarity_list = []
		for i in range(1024):
			if use_random:
				info = rndchoice(cluster_list[i])
				cluster_img = Runs[info['name']]'net_projections']['data'][info['index']]
			similarity_list.append(similarity(img,cluster_img))
		most_similar = np.argsort(similarity_list)
		return most_similar

	D['Runs'] = Runs
	D['affinity'] = affinity
	D['cluster_list'] = cluster_list
	D['find_most_similar_cluster'] = _function_find_most_similar_cluster
	D['function_make_average_clusters'] = _function_make_average_clusters

	return D
        






#EOF

if False:
	for i in range(1024):
		for x in range(32):
			for y in range(32):
				c[x,y]=p[i][m[x,y]]
		mi(c);spause();cg(i,ra=1)
