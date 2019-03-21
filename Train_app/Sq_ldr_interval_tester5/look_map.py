from kzpy3.vis3 import *
exec(identify_file_str)
from kzpy3.Data_app.classify_data import find_locations,run_paths
exec(identify_file_str)
#10 corner, 14, 16
"""
locations = []
Runs = {}
find_locations(opjD('Data'),locations,False)
run_paths(locations,Runs)
Images = {}
for r in Runs.keys():
    O_path = opjD(Runs[r],'original_timestamp_data.h5py')
    O = h5r(O_path)
    Images[r] = O['left_image']['vals']
"""



Arguments['cluster_list'] = opjD('cluster_list.pkl')
cluster_list = lo(Arguments['cluster_list'])

files = sggo('/home/karlzipser/Desktop/Data/Network_Predictions_projected/*.net_projections.h5py')
Files = {}
for f in files:
    name = fname(f).split('.')[0]
    Files[name] = h5r(f)['normal']

CA()
t = []
mm = m.flatten()
for cluster in rlen(cluster_list):
    #s = []
    
    #z = np.zeros((23,41,3))
    n = rlen(cluster_list[cluster])
    #if len(n) < 6:
    #    continue
    #random.shuffle(n) 292
    for i in [0]:#n:
        C = cluster_list[mm[cluster]][i]
        other_name = C['name']
        other_index = C['index']
        #other_img = Images[other_name][other_index].copy()
        traj_img = Files[other_name][other_index].copy()
        #z += traj_img
        #s.append(other_img)
        t.append(traj_img)
    #s = na(s)
t = na(t)
#v = vis_square2(z55(s),10,127)
w = vis_square2(z55(t),10,127)
print cluster
mi(w,'rgb');#mi(w,'traj');spause()
#mi(z55(z),'z')
#raw_enter()


#raw_enter()


#EOF