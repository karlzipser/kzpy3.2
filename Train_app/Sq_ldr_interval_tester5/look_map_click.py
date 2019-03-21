from kzpy3.vis3 import *
exec(identify_file_str)
from kzpy3.Data_app.classify_data import find_locations,run_paths
exec(identify_file_str)


if 'm' not in locals():
    m = lo(opjD('m'))

Arguments['cluster_list'] = opjD('cluster_list.pkl')
cluster_list = lo(Arguments['cluster_list'])

files = sggo('/home/karlzipser/Desktop/Data/Network_Predictions_projected/*.net_projections.h5py')
Files = {}
for f in files:
    name = fname(f).split('.')[0]
    Files[name] = h5r(f)['normal']


CA()
fig = figure('rgb')
Cdat = Click_Data(FIG=fig)
xy_list = Cdat['CLICK'](NUM_PTS=1)
pts_plot(na(xy_list),'r')


t = []
#mm = m.flatten()

if 'Clusters' not in locals():
    Clusters = {}

for x in range(32):
    for y in range(32):

        C = cluster_list[m[x,y]][0]
        other_name = C['name']
        other_index = C['index']

        traj_img = Files[other_name][other_index].copy()
        
        for k in Clusters.keys():
            if m[x,y] in Clusters[k]:
                traj_img /=4
                traj_img += 64
                break
        t.append(traj_img)

t = na(t)

w = vis_square2(z55(t),2,127)
#print cluster
mi(w,'rgb');spause()

k = 'rgb3'
#k = 'flat2'
k = 'ignore3'

if k not in Clusters:
    Clusters[k] = []
while True:
    xy_list = Cdat['CLICK'](NUM_PTS=1)
    mx = int(xy_list[0][0]/43)
    my = int(xy_list[0][1]/25)
    idnum = m[my,mx]
    cg(mx,my,idnum)
    Clusters[k].append(idnum)
    pts_plot(na(xy_list),'w')




#EOF