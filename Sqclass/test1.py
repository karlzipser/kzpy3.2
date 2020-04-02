from kzpy3.vis3 import *
from kzpy3.Train_app.Sq_ldr_interval_tester5_modified.Main import get_similarity
from kzpy3.Learn.clusters import Clusters
from main import *


import Menu.main
M = Menu.main.start_Dic(dic_project_path=pname(opjh(__file__)))
M['load']()

#if 'C' not in locals():
C = Clusters(get_similarity)
path = opjD('Destkop_clusters_and_not_essential_24July2019')
cluster_averages = lo(opj(path,'cluster_averages.pkl'))






net_name = fname(pname(__file__))

G = SqueezeNet().cuda()

NETWORK_OUTPUT_FOLDER = opjD('Networks',net_name)

load(G,NETWORK_OUTPUT_FOLDER)

torch.cuda.set_device(0)




P = {
    'vel-encoding coeficient':  1.0/2.3,
    'vec sample frequency': 30,#3.33,
}

def vec(heading,encoder,motor,sample_frequency,P):
    velocity = encoder * P['vel-encoding coeficient'] # rough guess
    if motor < 49:
        velocity *= -1.0
    a = [0,1]
    a = array(rotatePoint([0,0],a,heading))
    a *= velocity/sample_frequency
    return array(a)

#def f(x,A,B):
#    return A*x + B

def f___(x,A,B):
    return A*x+B

    


def get_predictions2D(headings,encoders,motors,sample_frequency,P):
    xy = array([0.0,0.0])
    xys = []
    for i in range(len(headings)):
        v = vec(headings[i],encoders[i],motors[i],P['vec sample frequency'],P) #3.33)
        xy += v
        xys.append(xy.copy())
    pts2D_1step = na(xys)
    return pts2D_1step


run_path = opjh('Desktops_older',
        'Desktop_19Feb19_08h49m53s',
        'model_car_data_July2018_lrc',
        'locations/local/left_right_center/h5py',
        #'Mr_Black_25Jul18_14h44m55s_local_lrc',
        #'Mr_Black_25Jul18_14h29m56s_local_lrc',
        'Mr_Black_24Jul18_20h04m17s_local_lrc',
        )
run_path = '/home/karlzipser/Desktop/Data/2_TB_Samsung_n/mid_Dec2018_with_lidar_image/locations/local/left_right_center/h5py/tegra-ubuntu_12Dec18_15h04m54s'
run_path = '/home/karlzipser/Desktop/Data/1_TB_Samsung_n1/tu_25to26Oct2018/locations/local/left_right_center/h5py/tegra-ubuntu_25Oct18_10h21m55s'
run_projected_path = '/home/karlzipser/Desktop/Data/Network_Predictions_projected/tegra-ubuntu_25Oct18_10h21m55s.net_projections.h5py'


if 'L' not in locals():
    L = h5r(opj(
        run_path,
        'left_timestamp_metadata_right_ts.h5py'
    ))
if 'O' not in locals():
    O = h5r(opj(
        run_path,
        'original_timestamp_data.h5py'
        ))
if 'Q' not in locals():
    Q = h5r(run_projected_path)


h = L['gyro_heading_x'][:]
e = L['encoder'][:]
em = L['encoder_meo'][:]
m = L['motor'][:]

pts = get_predictions2D(h,e,m,30,P)

slow_pts = []
for i in rlen(pts):
    if em[i] < 0.25:
        slow_pts.append(pts[i]) 


def get_index_of_nearest_point(pts,p):
    min_dist = 10**30
    min_indx = -999
    def dist(a,b):
        return np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
    for i in rlen(pts):    
        d = dist(pts[i,:],p)
        if d < min_dist:
            min_indx = i
            min_dist = d
    assert(i >= 0 and i < len(pts))
    return min_indx

    


#n = 30*30
m = 50
#s = 0.5
#M['Q']['num_clusters_to_use'] = 10
#M['Q']['num_clusters_to_average'] = 5
load_timer = Timer(1)
cycle_timer = Timer(5)
Abort = Toggler()

CA()

while True: 
    clf()
    fig = figure(1)
    pts_plot(pts,sym=',',color='b')
    pts_plot(slow_pts,sym=',',color='r')
    plot(pts[0,0],pts[0,1],'og')
    plot(pts[-1,0],pts[-1,1],'or')
    pts_plot(slow_pts,sym='x',color='r')
    plt_square()
    xylim(min(pts[:,0])-m,max(pts[:,0])+m,min(pts[:,1])-m,max(pts[:,1])+m)
    Cdat = Click_Data(FIG=fig,NO_SHOW=True)
    xy_list = Cdat['CLICK'](NUM_PTS=1)
    if None in xy_list[0]:
        print('done.')
        break
    indx = get_index_of_nearest_point(pts,xy_list[0])
    pts_plot([pts[indx,:]],sym='.',color='g')
    spause()

    xy_list = Cdat['CLICK'](NUM_PTS=1)
    if None in xy_list[0]:
        print('done.')
        break
    indx2 = get_index_of_nearest_point(pts,xy_list[0])
    pts_plot([pts[indx2,:]],sym='.',color='r')

    if indx > indx2:
        clp(' Warning, indicies reversed to have time direction correct ','`wrb')
        a = indx2
        indx2 = indx
        indx = a

    spause()

    xs = pts[indx:indx2,0]
    ys = pts[indx:indx2,1]
    
    xylim(min(xs)-10,max(xs)+10,min(ys)-10,max(ys)+10)
    pts_plot(slow_pts,sym='x',color='r')

    spause()




    if True:#try:
        for j in range(indx,indx2):
            if not np.mod(j,30*1):

                plot(pts[j,0],pts[j,1],'k.')

                spause()

            k = mci(Q['normal'][j],delay=1,scale=6,title='ldr')

            k = mci(O['left_image']['vals'][j],delay=33,scale=3,title='img')

            v = Q['normal'][j].transpose(2,1,0)

            if True:
                output = G.forward(torch.from_numpy(na([v])).cuda().float())
                output = output.data.cpu().numpy()[0]
                r = np.argsort(-output)
                assert r.max() <= 1024
                assert r.min() >=0
                #cg(r)
                cluster_mask = zeros(1024)
                cluster_mask[r[:M['Q']['num_clusters_to_use']]] = 1
                #figure('cluster_mask');clf();plot(cluster_mask);spause()

            if True:
                r = C['find_most_similar_cluster'](Q['normal'][j],show=False,use_random=False,cluster_mask=cluster_mask)
                #figure('r');clf();plot(r);spause()
                #cy(r)

            img = cluster_averages[r[0]]

            if 'img_weighted_prev' not in locals():
                img_weighted_prev = 0.0*img
            img_weighted = 0.0*img
            for e in range(M['Q']['num_clusters_to_average']):#int(1024*5/100.)):
                img_weighted += output[r[e]] * cluster_averages[r[e]].astype('float')

            s = M['Q']['s']

            img_weighted = z55((1.-s)*img_weighted+(s)*img_weighted_prev)
            img_weighted_prev = img_weighted
            k = mci(img_weighted,delay=1,scale=6,title='img_weighted')

            if load_timer.check():
                load_timer.reset()
                M['load']()
                if Abort['test'](M['Q']['ABORT']):
                    sys.exit()

            cycle_timer.freq('cycle_timer')

        raw_enter()
    else:#except:
        print('exception')

# net_23Mar20_10h23m49s.0.0043994044.cuda.infer
# scp -r -P 1022 karlzipser@169.229.219.140:'Desktop/Networks/Sqclass/weights/net_23Mar20_10h23m49s.0.0043994044.cuda.infer' Desktop/Networks/Sqclass/weights
        
#,b

raw_enter()






#EOF