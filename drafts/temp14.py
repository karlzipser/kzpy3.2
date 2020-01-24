

from kzpy3.Learn.get_data.runs import All_runs


#
def Clusters(similarity):

    global affinity,cluster_list

    D = {}

    if True:#type(affinity) == type(None):
        path = opjD('Destkop_clusters_and_not_essential_24July2019')
        affinity = lo(opj(path,'affinity'))
        # np.float, shape == (1024, 1024)
        # affinity of every cluster for every other

        cluster_list = lo(opj(path,'cluster','cluster_list_25_1st_pass_11April2019_bkp.pkl'))
        # list len 1024 of lists of run-name/index pairs, one for each cluster

        if len(sggo(path,'cluster_averages.pkl')) == 1:
            D['cluster_averages'] = lo(opj(path,'cluster_averages.pkl'))


    runs = All_runs['validate'] + All_runs['train']

    Runs = {}

    for r in runs:

        #Run_coder[run_ctr] = r

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
        
        """
        Runs[r]['original_timestamp_data'] = \
            {'path':opj(opjD('Data'),H['paths'].keys()[0],r,'original_timestamp_data.h5py'),'data':None}

        Runs[r]['flip_images'] = \
            {'path':opj(opjD('Data'),H['paths'].keys()[0],r,'flip_images.h5py'),'data':None}

        Runs[r]['left_timestamp_metadata_right_ts'] = \
            {'path':opj(opjD('Data'),H['paths'].keys()[0],r,'left_timestamp_metadata_right_ts.h5py'),'data':None}
        """
        Runs[r]['net_projections'] = \
            {'path':opj(opjD('Data'),'Network_Predictions_projected',r+'.net_projections.h5py'),'data':None}
        """
        Runs[r]['activations/data'] = \
            {'path':opj(pname(pname(_Runs[r])),'data',r+'.h5py'),'data':None}

        Runs[r]['activations/indicies'] = \
            {'path':opj(pname(pname(_Runs[r])),'indicies',r+'.h5py'),'data':None}
        """
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
        avg_img = np.zeros((23,41,3))
        for i in range(1024):
            avg_img *= 0
            avg_ctr = 0.0
            for j in rlen(cluster_list[i]):
                info = cluster_list[i][j]
                if info['name'] not in Runs:
                    cr(info['name'],'not found')
                    #avg_img = None
                    continue
                else:
                    cg(info['name'],'found')
                cluster_img = Runs[info['name']]['net_projections']['data']['normal'][info['index']]
                              #c(Runs,c(info,'name'),'net_projections','data',c(info,'index'))
                avg_img += cluster_img
                avg_ctr += 1.0
            if avg_ctr < 1.0:
                avg_list.append(None)
            else:
                avg_img /= avg_ctr
                avg_list.append(z55(avg_img))
                img = avg_list[-1]
                #mi(img);spause();cg(img.min(),img.max());raw_enter()
        D['cluster_averages'] = avg_list
        if len(sggo(path,'cluster_averages.pkl')) == 0:
            q = raw_input('save cluster_averages? y/n ')
            if q == 'y':
                cg('saving cluster_averages.pkl')
                so(opj(path,'cluster_averages.pkl'),D['cluster_averages'])

    def _function_find_most_similar_cluster(img,use_random=False,show=True):
        similarity_list = []
        for i in range(1024):
            if use_random:
                info = rndchoice(cluster_list[i])
                cluster_img = Runs[info['name']]['net_projections']['data']['normal'][info['index']]
            else:
                cluster_img = D['cluster_averages'][i]
            similarity_list.append(similarity(img,cluster_img,show))
        most_similar = np.argsort(similarity_list)
        return most_similar

    D['Runs'] = Runs
    D['affinity'] = affinity
    D['cluster_list'] = cluster_list
    D['find_most_similar_cluster'] = _function_find_most_similar_cluster
    D['function_make_average_clusters'] = _function_make_average_clusters

    return D
        



from kzpy3.Train_app.Sq_ldr_interval_tester5_modified.Main import get_similarity

C = Clusters(get_similarity)

for n in range(300,500):#n = 401

    a = C['cluster_averages'][n]
    #C['Runs'][ a_key(C['Runs'])][]

    r = C['find_most_similar_cluster'](a,show=False,use_random=False)
    CA()
    mi(C['cluster_averages'][n],n)

    mi(C['cluster_averages'][r[1]],r[1])
    raw_enter()




#EOF


0 1->2 2->1
for i in [0,2,1]: # center left right [???]
red  left
center green
right blue

if False:
    for i in range(1024):
        for x in range(32):
            for y in range(32):
                c[x,y]=p[i][m[x,y]]
        mi(c);spause();cg(i,ra=1)




a,b,c = 2,4,8
p = rnd()*(a+b+c)
if p < a:
    print 'a'
elif p < a+b:
    print 'b'
else:
    print 'c'




def weighted_probs(weight_lst,repeats=1000):
    o = zeros(len(weight_lst))
    w = 1.0*sum(weight_lst)
    for r in range(repeats):
        p = rnd() * w
        v = 0
        for i in rlen(weight_lst):
            v += weight_lst[i]
            if p < v:
                o[i] += 1
                break
    return o/(1.0*repeats)
    

np.argsort(weighted_probs([1,2,9],1))




Colors = {
    0:(255,0,0),
    1:(0,255,0),
    2:(0,0,255)
}
img = imread(opjD('t.jpg'))#"/Users/karlzipser/Desktop/Ellen.jpg")
img = cv2.resize(img,(168,94))
img2=img.copy() * 0
h,w,d = shape(img)
for z in range(d):
    a,a_prev = None,None
    pt = None
    for y in range(h/2,h-5):
        if a != None:
            a_prev = a
        a = np.argsort(img[y,:,z])[-1]
        if a_prev == None:
            a_prev = a
        #print(a)
        #print a,a_prev,b
        b = int((a+a_prev)/2.0)
        if pt == None:
            pt = (b,y)
        s = int((y**2/47./3.)/10)
        print s
        cv2.line(img2,pt,(b,y),Colors[z],s)
        pt = (b,y)
        #img2[y,b-1:b+1,z] = 255
        #a_prev = a
CA()
mi(img2,3)



