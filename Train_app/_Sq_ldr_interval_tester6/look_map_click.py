from kzpy3.vis3 import *
exec(identify_file_str)
from kzpy3.Data_app.classify_data import find_locations,run_paths
exec(identify_file_str)


if 'm' not in locals():
    m = lo(opjD('m'))

Arguments['cluster_list'] = opjD('cluster_list_166.pkl')
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
        if m[x,y] < 0:
            traj_img *= 0
        if False:
            if len(cluster_list[m[x,y]])>4:
                traj_img *= 0
        t.append(traj_img)


t = na(t)

w = vis_square2(z55(t),2,127)
#print cluster
mi(w,'rgb');spause()

k = 'rgb3'
#k = 'flat2'
k = 'ignore3'
k = 'rgb separate'
k = 'rgb separate 2'
k = 'strong edge'
k = 'rgb separate 3'
k = 'rgb blurry'
k = 'strong edge 2'
k = 'rgb blurry 2'
k = 'strong edge 3'
k = 'soft edge'
k = 'pointy corner'
k = 'center yellow'
k = 'rgb blurry 3'
k = 'rgb blurry 4'
k = 'other'

if k not in Clusters:
    Clusters[k] = []
while True:
    cg('topic is',"\""+k+"\"")
    xy_list = Cdat['CLICK'](NUM_PTS=1)
    mx = int(xy_list[0][0]/43)
    my = int(xy_list[0][1]/25)
    idnum = m[my,mx]
    if False:#idnum in [961,258]:
        k = 'other'
        cr("Changing topic!")
        break
    cg(mx,my,idnum)
    Clusters[k].append(idnum)
    pts_plot(na(xy_list),'w')


if False:
    Cluster_directional2 = {}

    Cluster_directional2['rgb separate'] = \
        Clusters['rgb separate'] + \
        Clusters['rgb separate 2'] + \
        Clusters['rgb separate 3']

    Cluster_directional2['rgb blurry'] = \
        Clusters['rgb blurry'] + \
        Clusters['rgb blurry 2'] + \
        Clusters['rgb blurry 3'] + \
        Clusters['rgb blurry 4']

    Cluster_directional2['strong edge'] = \
        Clusters['strong edge'] + \
        Clusters['strong edge 2'] + \
        Clusters['strong edge 3']

    Cluster_directional2['pointy corner'] = \
        Clusters['pointy corner']

    Cluster_directional2['center yellow'] = \
        Clusters['center yellow']

    Cluster_directional2['soft edge'] = \
        Clusters['soft edge']

    Cluster_directional2['strong edge'] = \
        Clusters['strong edge']

    Cluster_directional2['other'] = \
        Clusters['other']

    so(opjD('Clusters_directional2'),Cluster_directional2)




#EOF