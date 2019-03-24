from kzpy3.vis3 import *
exec(identify_file_str)
from kzpy3.Data_app.classify_data import find_locations,run_paths
exec(identify_file_str)

CA()
fig = figure('rgb',figsize=(30,20))
Cdat = Click_Data(FIG=fig)

if 'm' not in locals():
    m = lo(opjD('m'))

Arguments['cluster_list'] = opjD('cluster_list_166.pkl')
cluster_list = lo(Arguments['cluster_list'])

files = sggo('/home/karlzipser/Desktop/Data/Network_Predictions_projected/*.net_projections.h5py')
Files = {}
for f in files:
    name = fname(f).split('.')[0]
    Files[name] = h5r(f)['normal']





def do_it(topic,hide=[],grey=[]):

    t = []
    
    data_list = []

    for x in range(32):
        for y in range(32):

            C = cluster_list[m[x,y]][0]
            other_name = C['name']
            other_index = C['index']

            traj_img = Files[other_name][other_index].copy()
            
            if m[x,y] in grey:
                traj_img /=4
                traj_img += 64
                
            if m[x,y] in hide:
                traj_img *= 0

            if m[x,y] < 0:
                traj_img *= 0

            if False:
                if len(cluster_list[m[x,y]])>4:
                    traj_img *= 0

            t.append(traj_img)

    t = na(t)

    w = vis_square2(z55(t),2,127)

    mi(w,'rgb');spause()

    k = 'new'
    if k not in Clusters:
        Clusters[k] = []

    while True:
        cg('topic is',"\""+k+"\"")
        xy_list = Cdat['CLICK'](NUM_PTS=1)
        if xy_list == [[None,None]]:
            cr("exiting do_it()")
            break
        mx = int(xy_list[0][0]/43)
        my = int(xy_list[0][1]/25)
        idnum = m[my,mx]

        cg(mx,my,idnum)
        data_list.append(idnum)
        pts_plot(na(xy_list),'w')

    try:
        saved_log = loD('saved_log')
    except:
        saved_log = []

    saved_log.append([topic,dl,time.time()])

    so(opjD('saved_log'),saved_log)

    return data_list

#do_it()







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

    sparse += do_it('sparse',hide=mini_base+half_base+broad_base+two_3rds_base,grey=sparse)
    half_base += do_it('half_base',hide=sparse+mini_base+broad_base+two_3rds_base,grey=half_base)
    broad_base += do_it('broad_base',hide=mini_base+sparse+half_base+two_3rds_base,grey=broad_base)
    two_3rds_base += do_it('two_3rds_base',hide=sparse+mini_base+half_base+broad_base,grey=two_3rds_base)
    mini_base += do_it('mini_base',hide=sparse+half_base+broad_base+two_3rds_base,grey=mini_base)

    so(opjD('sparse'),sparse)
    so(opjD('half_base'),half_base)
    so(opjD('broad_base'),broad_base)
    so(opjD('two_3rds_base'),two_3rds_base)
    so(opjD('mini_base'),mini_base)

if False:
    c=loD('cluster_list_166')
    clens = []
    for d in c:
        clens.append(len(d))
    hist(clens)


#EOF