from kzpy3.vis3 import *
exec(identify_file_str)
from kzpy3.Data_app.classify_data import find_locations,run_paths
exec(identify_file_str)

if False:
    dic_do_it(H,'base_3',hide_topics=['sparse','base_1','base_2','base_3','base_4','base_5',])
    dic_do_it(H,remove=True,topic='base_3')
    dic_do_it(H,hide_topics=['sparse','two_3rds_base','half_base','mini_base','broad_base',],topic='half_base')
    dic_do_it(H,hide_topics=['sparse','separated_top','round_top','pointy_top','notched_top',],topic='flat_top')

    base_position = ['base_1','base_2','base_3','base_4','base_5',]

    base_width = ['two_3rds_base','half_base','mini_base','broad_base',]

    traj_separation = ['separate','nearly_separate','mixed',]

    top_type = ['separated_top','round_top','pointy_top','notched_top','flat_top']

    topics = ['two_3rds_base','separate','separated_top','base_2','half_base','round_top','mini_base',
         'pointy_top','nearly_separate','all_1024','broad_base','sparse','mixed','base_1','top_3','base_3','base_4',
         'base_5','notched_top',]

    sparse = ['sparse']

    for tq in top_type:
        dic_do_it(H,just_show=True,topic=tq)
        cy(tq,ra=1)

CA()
fig = figure('rgb',figsize=(30,20))
Cdat = Click_Data(FIG=fig)

if 'm' not in locals():
    m = lo(opjD('m'))

Arguments['cluster_list'] = opjD('cluster_list_25_1st_pass.pkl')
cluster_list = lo(Arguments['cluster_list'])

files = sggo('/home/karlzipser/Desktop/Data/Network_Predictions_projected/*.net_projections.h5py')
Files = {}
for f in files:
    name = fname(f).split('.')[0]
    Files[name] = h5r(f)['normal']

if 'H' not in locals():
    H = lo(most_recent_file_in_folder(opjD('H_dics'))) 

"""
H = {}
hand_clicked_clusters = opjD('hand_clicked_clusters')
clist = sggo(hand_clicked_clusters,'*.pkl')
for c in clist:
    f = fname(c).replace(".pkl",'')
    exec_str = d2n("H['",f,"'] =","list(set(lo('",c,"')))")
    exec(exec_str)
"""

def dic_do_it(H={},topic='',hide_topics=[],just_show=False,remove=False):
    assert len(topic) > 0
    grey = H[topic]
    hide = []
    for h in hide_topics:
        if h != topic:
            hide += H[h]
        else:
            cr('not hiding',h,'which is in hide_topics')
    if topic not in H:
        H[topic] = []
    cg('topic:',topic)
    cb('hide:',hide)
    cg('grey:',grey)

    if just_show:
        do_it(topic,show=H[topic])
    elif remove:
        remove_hidek = H.keys()
        remove_hidek.remove(topic)
        remove_hide = []
        for r in remove_hidek:
            remove_hide += H[r]
        remove_list = do_it(topic,show=H[topic],remove=True)
        for r in remove_list:
            cr('remove',r)
            H[topic].remove(r)
    else:
        H[topic] += do_it(topic,hide=hide,grey=grey,show=None)
        for h in H:
            H[h] = list(set(H[h]))
        soD(H,d2n('H_dics/H.',time.time()))


def do_it(topic='',hide=[],grey=[],show=None,remove=False):

    t = []
    
    data_list = []

    for x in range(32):
        for y in range(32):

            C = cluster_list[m[x,y]][0]
            other_name = C['name']
            other_index = C['index']

            traj_img = Files[other_name][other_index].copy()
            
            if type(show) == list:
                if m[x,y] not in show:
                    traj_img *= 0
            else:
                if m[x,y] in grey:
                    traj_img /=4
                    traj_img += 64
                    
                if m[x,y] in hide:
                    traj_img *= 0

                if m[x,y] < 0:
                    traj_img *= 0

            t.append(traj_img)

    t = na(t)

    w = vis_square2(z55(t),2,127)

    mi(w,'rgb',img_title=topic);spause()


    if type(show) != list or remove == True:
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

        saved_log.append([topic,data_list,time.time()])

        so(opjD('saved_log'),saved_log)

    return data_list







#EOF