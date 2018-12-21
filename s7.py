###start
from kzpy3.vis3 import *
"""
https://stackoverflow.com/questions/76134/how-do-i-reverse-project-2d-points-into-3d
http://pyopengl.sourceforge.net/documentation/installation.html
"""

try:
    print len(encoders)
except:
    run_folder = '/media/karlzipser/preprocessed_5Oct2018_500GB/model_car_data_July2018_lrc/locations/local/left_right_center/h5py/Mr_Black_25Jul18_19h55m13s'
    cs("Loading L and O...")
    L = h5r(opjD(run_folder,"left_timestamp_metadata_right_ts.h5py"))
    O = h5r(opjD(run_folder,"original_timestamp_data.h5py"))
    headings = L['gyro_heading_x'][:]
    encoders = L['encoder'][:]








def vec(heading,encoder):
	velocity = encoder/2.3 # rough guess
	a = [0,1]
	a = array(rotatePoint([0,0],a,heading))
	a *= velocity/30.0
	return array(a)

from scipy.optimize import curve_fit

def f(x,A,B):
    return A*x + B

A,B = curve_fit(f,x,y)[0]




ang_prev = 0
fig1 = 99
figure(fig1)
clf()
plt_square()
l = 5.0
xy = array([0.0,0.0])
xys=[]
CA()
hz_timer = Timer(5)

cool_run_by_metal_bridge = 22000

if Truecool_run_by_metal_bridge    for i in range(22000,len(headings),1):
        heading = headings[i]
        encoder = encoders[i]
        v = vec(heading,encoder)
        xy += v # taken into consideration reverse driving
        xys.append(array(xy))
        graphics = False
        if np.mod(i,1) == 0:
            if len(xys) > 90+30:
                graphics = True
        if graphics:
            points = na(xys)[-120:]
            points -= points[30,:]
            points_to_fit = points[15:45,:]#na(xys)[-95:-90]
            x = points_to_fit[:,0]
            y = points_to_fit[:,1]
            m,b = curve_fit(f,x,y)[0]
            ang = np.degrees(angle_between([0,1],[1,m]))

            #print(int(ang))
            mci(O['left_image']['vals'][i-90],scale=2,delay=1,title='left camera')
            clf();plt_square();xylim(-l,l,-l,l)
            plot(0,1,'r.')
            plot(1,m,'r.')
            pts_plot(points[:30,:],'r',sym=',')
            pts_plot(points[30:,:],'r',sym=',')

            rpoints = na(rotatePolygon(points,ang))

            rpoints *= -1
            pts_plot(rpoints[:30,:],'k',sym=',')
            pts_plot(rpoints[30:,:],'k',sym='o')
            
            """
            points_to_fit = rpoints[30:45,:]#na(xys)[-95:-90]
            x = points_to_fit[:,0]
            y = points_to_fit[:,1]
            m,b = curve_fit(f,x,y)[0]
            ang2 = np.degrees(angle_between([0,1],[m,1]))
            
            rpoints2 = na(rotatePolygon(rpoints,-ang2/2))

            pts_plot(rpoints2[:30,:],'b',sym='.')
            pts_plot(rpoints2[30:,:],'b',sym='+')
            """
            d_ang = ang-ang_prev
            print(dp(ang),dp(d_ang),dp(ang2))
            #if np.abs(d_ang) > 1.5:
            #    raw_enter()
            ang_prev = ang
            spause()
        hz_timer.freq()














            """
            theta_ = angle_clockwise((0,1), (R[aruco_heading_x][vals][-1],R[aruco_heading_y][vals][-1]))
            xy_ = na([x_,y_])
            pts_pov_ = na(rotatePolygon(pts_-xy_,theta_))
            """

"""
use:

    grep -lr rotate * | xargs grep -lr heading

check out:

    ~/_kzpy3_older/kzpy_8Sept2018/Localization_app/localizer_listener.py

https://stackoverflow.com/questions/973473/getting-a-list-of-all-subdirectories-in-the-current-directory
"""


###stop


#run_name = "Mr_Purple_24Nov18_12h57m47s"
#run_name = "Mr_Purple_22Nov18_15h00m19s"
run_name = "tegra-ubuntu_20Nov18_10h59m22s"
segments = [[21254,56549]]

run_path = opj('/media/karlzipser/rosbags1/h5py/',run_name)
O = h5r(opj(run_path,'original_timestamp_data.h5py'))
L = h5r(opj(run_path,'left_timestamp_metadata_right_ts.h5py'))
len_left = len(O['left_image']['vals'])

"""
run_name = "Mr_Purple_24Nov18_12h57m47s"
segments=[
    [32998,35637],
    [3023,4859],
    [9324,10100],
    [13272,13800],
    [14050,14550],
    [17000,18575],
    [23850,26453],
    [29000,29500],
    [44164,45155],
    #[5500,10100],
    #[27800,31100],
]
"""
#segments=[[36000,40440],]
"""
segments = [
    [4400,5500],
    [11200,13800],
    [15300,18000],
    [22000,25600],
    [26000,26700],
    [27500,28920],
    [30500,31320],
    [38236,39550],
    [39768,41386]]
"""




for fctr in range(len(segments)):
    s1,s2 = segments[fctr]
    cr(s1,s2)

    dst = opjD(d2n("Frames_temp_",s1,"_",s2))
    os.system("mkdir "+dst)


    blink_frames = 30/6
    blink_on = True
    blink_ctr = 0
    ctr = 0
    for i in range(s1,s2,1):
        #print i
        frame = O['left_image']['vals'][i].copy()
        button_number = int(L['button_number'][i])

        #cg(button_number,blink_on,blink_ctr)

        if blink_on:
            if button_number == 1:
                #cr('here')
                frame[0:10,0:20,:] = na([255,0,0])
            elif button_number == 3:
                frame[0:10,-20:,:] = na([255,0,0])
                
        blink_ctr += 1

        if blink_ctr >= blink_frames:
            blink_on = False
        if blink_ctr >= 2* blink_frames:
            blink_on = True
            blink_ctr = 0

        #mi(frame);spause()
        imsave(opj(dst,d2n(ctr,'.png')),frame)
        ctr += 1


    frames_to_video_with_ffmpeg(dst,opjD(d2n(run_name,"__",s1,"_to_",s2,".mov")))









p = []
for i in range(0,len(o),100):
    p.append(np.mean(na(o[i:i+100])))













try:
    D.close()
except:
    pass
run_name = 'tegra-ubuntu_25Oct18_15h43m36s'

D = h5r(d2n('/media/karlzipser/1_TB_Samsung_n1/_.Depth_images.log.resize.flip.left_ts/',run_name,'.Depth_image.log.resize.flip.with_left_ts.h5py'))
r = D['resized']
s1,s2 = 2000,12000
dst = opjD(d2n("Frames_temp_",s1,"_",s2))
os.system("mkdir "+dst)
ctr = 0
for i in range(s1,s2):
    frame = cv2.resize(r[i],(168*2,16*2))
    if np.mod(i,10)==0:
        cg(i)
    imsave(opj(dst,d2n(ctr,'.png')),frame)
    ctr += 1
frames_to_video_with_ffmpeg(dst,opjD(d2n(run_name,"__",s1,"_to_",s2,".mov")))











# http://ros-users.122217.n3.nabble.com/2d-numpy-arr-msgs-td895779.html

for j in range(100):
    time.sleep(.250)
    k = np.random.randint(10000,50000)
    for l in range(k,k+60,3):
        c=O['left_image']['vals'][l]
        i = D['left_to_lidar_index'][l]
        a=D['resized'][i] 
        a32=cv2.resize(a,(168,32))
        b=zeros((94,168),np.uint8)+127
        b[-42:-10,:]=a32
        #mi(b,'b')
        mi(c,'c')
        mi(a32[:,43:125],'a32-')
        spause()



ctr = 0
timer = Timer(5.0)
while not timer.check():
    b=cv2.resize(a,(190/2,338))
    b[0,0,0] = 0
    ctr += 1
print ctr




beam_altitude_angles = [
    16.611,  16.084,  15.557,  15.029,  14.502,  13.975,  13.447,  12.920,
    12.393,  11.865,  11.338,  10.811,  10.283,  9.756,   9.229,   8.701,
    8.174,   7.646,   7.119,   6.592,   6.064,   5.537,   5.010,   4.482,
    3.955,   3.428,   2.900,   2.373,   1.846,   1.318,   0.791,   0.264,
    -0.264,  -0.791,  -1.318,  -1.846,  -2.373,  -2.900,  -3.428,  -3.955,
    -4.482,  -5.010,  -5.537,  -6.064,  -6.592,  -7.119,  -7.646,  -8.174,
    -8.701,  -9.229,  -9.756,  -10.283, -10.811, -11.338, -11.865, -12.393,
    -12.920, -13.447, -13.975, -14.502, -15.029, -15.557, -16.084, -16.611,
]


# 28 to 125
import sensor_msgs
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2
import rospy
import rosbag
data = []
for bv in ['/media/karlzipser/model_car_data_A1/raw_data8/tegra-ubuntu_11Oct18_17h11m39s/bair_car_2018-10-11-17-16-06_9.bag']:
    cprint(bv,'yellow')
    bagv = rosbag.Bag(bv)
    for m_ in bagv.read_messages(topics=['/os1_node/points']):
        timestampv = round(m_[2].to_time(),3) # millisecond resolution
        assert(is_number(timestampv))
        topic_ = m_[0].replace('/bair_car/','')
        topic_ = topic_.replace('/os1_node/','')
        if m_[0] == '/os1_node/points':
        ##print "here"
            try:
                # https://answers.ros.org/question/240491/point_cloud2read_points-and-then/
                valv_temp = list(sensor_msgs.point_cloud2.read_points(m_[1],skip_nans=True,field_names=('t','reflectivity','intensity',"x","y","z")))
                data.append(valv_temp)
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                CS_('Exception!',emphasis=True)
                CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)








reflectivity = []
intensity = []
for i in rlen(data):
    reflectivity += list(a[:,4])
    intensity += list(a[:,5])
reflectivity = na(reflectivity)
intensity = na(intensity)
CA()
figure('intensity');hist(intensity,200)
figure('reflectivity');hist(reflectivity,200)





from subprocess import Popen, PIPE, STDOUT

p1 = Popen(['open', '-a', 'Terminal', '-n'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
p2 = Popen(['open', '-a', 'Terminal', '-n'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

p1.communicate('ls')
p2.communicate('python kzpy3/Menu_app/menu2.py path kzpy3/VT dic P')



a = range(10)
ctr = 0
timer = Timer(5)
while not timer.check():
    a.append(1)
    a.pop(0)
    a = na(a)
    a = list(a)
    ctr+=1
cr(ctr)

a = arange(10)
ctr = 0
timer = Timer(5)
while not timer.check():
    a[0:9] = a[1:10]
    a[9] = 1
    ctr+=1
cr(ctr)


theta = 15
#sigma = 0.023
clf();plt_square()
#plot([0,0],[-1,1],'k:')
#plot([-1,1][0,0],'k:')
points = np.random.random((10,2))
points -= points[0,:]

pts_plot(points,'r')
dp = vec(theta,1)

points[0,:] += dp
plot(points[0,0],points[0,1],'k.')
rotatePolygon__array_version(points,-theta)
pts_plot(points,'b')
#points -= na([0,sigma])
#pts_plot(points,'k')































def vec(heading,encoder,sample_frequency=30.0):
    velocity = encoder * P['vel-encoding coeficient'] # rough guess
    a = [0,1]
    a = array(rotatePoint([0,0],a,heading))
    a *= velocity/sample_frequency
    return array(a)

U = lo( opjD('Data/16Nov2018_held_out_data/net_predictions.tegra-ubuntu_16Nov18_17h59m10s.pkl' ))
O = h5r(opjD('Data/16Nov2018_held_out_data/h5py/tegra-ubuntu_16Nov18_17h59m10s/original_timestamp_data.h5py' ))
L = h5r(opjD('Data/16Nov2018_held_out_data/h5py/tegra-ubuntu_16Nov18_17h59m10s/left_timestamp_metadata_right_ts.h5py'))


################################
# version to project ahead
def get_prediction_points(headings,encoders):
    points = [na([0.,0.])]
    theta_integrated = 0
    for h,e in zip(headings,encoders):
        theta_integrated += h
        v = vec(theta_integrated,e)
        p = na(points[-1]).copy()
        p += v
        points.append(p)
    return points
#
##################################
###################################
# move points back
points = []

dh_max = 0

P = {}
P['vel-encoding coeficient'] = (1.0/2.3)
figure(8)
timer = Timer(1)
i = 5000
#while not timer.check() and i<15337:
while i<16000:#len(L['encoder']):

    heading = L['gyro_heading_x'][i] - L['gyro_heading_x'][i-1]
    if np.abs(heading)>dh_max:
        dh_max = np.abs(heading)
    encoder = L['encoder'][i]
    clf();plt_square();xysqlim(30)
    timer.message(d2s(i,dp(heading),dp(encoder),dh_max))

    net_headings = U['direct'][i]['heading'].copy()
    net_headings -= net_headings[0]
    net_encoders = U['direct'][i]['encoder']
    points += get_prediction_points(net_headings,30*net_encoders)
    points = na(points)

    points -= points[0,:]

    v = vec(heading,encoder,3.0)

    points[0,:] += v

    rotatePolygon__array_version(points,-heading)
    pts_plot(points,color='b',sym=',')
    spause()
    points = list(points)
    try:
        pass#points = points[-600:]
    except:
        pass
    i+=1
    mci(O['left_image']['vals'][i],scale=3)
#
##################################




for behavioral_mode in  ['left','direct','right']:
    headings = U[behavioral_mode][index]['heading']
    encoders = U[behavioral_mode][index]['encoder']




h = L['gyro_heading_x']




dh=[]
for i in range(1,len(h)):
    dh.append(h[i]-h[i-1])
figure(4);hist(dh,200)

#P['Arduinos']['MSE'].write(write_str)










temp = (255*z2o(np.random.randn(94,168))).astype(np.uint8)
cv2.putText(
    temp,
    d2n('R','b',0),
    (10,70),
    cv2.FONT_HERSHEY_SIMPLEX,
    2,(255),4);
mi(temp)
mi(cv2.resize(temp,(41,23)),2)










lidar_ts = O['image']['ts'][:]
left_camera_ts = L['ts'][:]

lidar_index = 0

D_left_to_lidar_index = 0 * left_camera_ts

len_left_ts = len(left_camera_ts)

finished = False

for i in range(len_left_ts):
    if finished:
        break

    left_ts = left_camera_ts[i]

    while lidar_ts[lidar_index] < left_ts:

        if lidar_index >= len(lidar_ts)-1:
            finished = True
        if finished:
            break

        lidar_index += 1

    D_left_to_lidar_index[i] = lidar_index


.create_dataset('left_to_lidar_index',data=D_left_to_lidar_index)






ctr = 0
timer = Timer(5)
while not timer.check():
    zeros_metadata_size = zeros((1,1,23,41))
    ctr += 1
cg(ctr)








while True:
    n0 = np.random.randint(len(ll))
    for n1 in range(n0,n0+60):
        n2 = ll[n1]
        mi(m[n2],1)
        mi(l[n1],2)
        spause()
    raw_enter()








'/media/karlzipser/2_TB_Samsung_n3/mid_Dec2018_with_lidar_image/locations/local/left_right_center/h5py/tegra-ubuntu_12Dec18_16h59m28s'
'/media/karlzipser/2_TB_Samsung_n3/mid_Dec2018_with_lidar_image/locations/local/left_right_center/h5py/tegra-ubuntu_12Dec18_15h04m54s'
'/home/karlzipser/Desktop/Data/locations/local/left_right_center/h5py/tegra-ubuntu_11Dec18_16h05m42s'

rsync -ravL ~/Desktop/Networks/* /media/karlzipser/2_TB_Samsung_n3/Networks/




runs = lo(opjD('Data/Network_Predictions_13Dec2018/runs.pkl'))
Runs = {}
for r in runs:
    Runs[fname(r)] = r

Arguments['run']='tegra-ubuntu_15Nov18_20h52m45s'
run_path = Runs[Arguments['run']]
#O=h5r(opj(run_path,'original_timestamp_data.h5py')) 
O=h5r(opj(run_path,'original_timestamp_data.h5py')) 
P = h5r(opj('/home/karlzipser/Desktop/Data/Network_Predictions_projected',fname(run_path)+'.net_projections.h5py' ))
for i in range(9500,20000):
    mci(O['left_image']['vals'][i][:],title='O')
    mci(P['i0'][i][:],title='P')





import torch
import kzpy3.Train_app.Train_SqueezeNet_15Sept2018_1Nov_14Nov.Network_Module as Network_Module
Network = Network_Module.Pytorch_Network()
n=Network['net'] 
#save_data = torch.load('/home/karlzipser/Desktop/Networks/_net_15Sept2018_1Nov_with_reverse_/weights/net_11Dec18_23h35m53s.infer') 
#save_data = torch.load('/home/karlzipser/Desktop/Networks/net_15Sept2018_1Nov_with_reverse_with_12imgs/weights/net_17Dec18_15h32m44s.infer') 
save_data = torch.load(most_recent_file_in_folder('/home/karlzipser/Desktop/Networks/net_15Sept2018_1Nov_with_reverse_with_12imgs/weights'))
n=save_data['net'] 
p = n['post_metadata_features.0.squeeze.weight'] 
q = p.cpu().numpy() 
q = q[:,:,0,0] 
q[:,128]/=10.
#mi(q[:,:129])  
mi(q,5)




r = q.copy()
r[:,128:128+5] = 0
r[:,-10:] = 0
for i in range(16):
    r[i,:] = z2o(r[i,:])
mi(r,100)


O=h5r(opjD('Data/16Nov2018_held_out_data/h5py/tegra-ubuntu_16Nov18_17h44m50s/original_timestamp_data.h5py'))
O=h5r(opjD('Data/16Nov2018_held_out_data/h5py/tegra-ubuntu_16Nov18_17h44m50s/original_timestamp_data.h5py'))


i = 9999
d = {}
d['flip'] = False
if not d['flip']:
    I = O
else:
    I = F
d['left0'] =    I['left_image']['vals'][i][:]
d['left1'] =    I['left_image']['vals'][i+1][:]
d['right0'] =   I['right_image']['vals'][i][:]
d['right1'] =   I['right_image']['vals'][i+1][:]


data_moment_keys = ['encoder_meo',
 'name',
 'labels',
 'gyro_heading_x',
 'FLIP',
 'encoder_past',
 'right',
 'projections',
 'motor',
 'steer',
 'left',
]

"""
In [42]: dm['labels']
Out[42]: 
{'direct': 0,
 'follow': 0,
 'furtive': 0,
 'heading_pause': 0,
 'left': 0,
 'play': 0,
 'right': 1}
"""

def relu(x):
    return max(0,x)

def f(x,a,b):
    return relu(a*relu(x)+b*relu(x))


p=n['pre_metadata_features.0.weight']
q = p.cpu().numpy()

for o in range(3):
    w = []
    for x in range(3):
        for y in range(3):
            w.append(q[:,range(o,12,3),x,y])
    mi(w);spause();raw_enter()







abs(d['steer']-49) < 5:




a b c e g h k q u v w z





################################################################################
#
Arguments['path'] = opjD('Data/1_TB_Samsung_n1/left_direct_stop__31Oct_to_1Nov2018/locations/local/left_direct_stop')

data_path = Arguments['path']
behavioral_modes = ['left','right','direct','stop']
steers = ['low_steer','high_steer','reverse']

Data_moments_dic = lo(opj(data_path,'data_moments_dic.pkl'))

all_moments = []
for u in ['train','val']:
    for v in steers:
        if v in Data_moments_dic[u]:
            for i in rlen(Data_moments_dic[u][v]):
                Data_moments_dic[u][v][i]['steer_type'] = v
            all_moments += Data_moments_dic[u][v]

Organized_moments = {}

for a in all_moments:

    r = a['run_name']

    if r not in Organized_moments:
        Organized_moments[r] = {}
        for b in behavioral_modes:
            Organized_moments[r][b] = {}
            for s in steers:
                Organized_moments[r][b][s] = []

    b = a['behavioral_mode']
    if b == 'center':
        b = 'direct'
        a['behavioral_mode'] = b

    if b not in behavioral_modes:
        cr(b,'not in',behavioral_modes)

    Organized_moments[r][b][a['steer_type']].append(a)


S = {}
Ctrs = {}         
C = {'left':'r.','right':'g.','direct':'b.','stop':'c.','center':'y.','reverse':'k.'}
CA()

for r in Organized_moments.keys():
    ectr = 0
    ctr = 0

    L = h5r(opj(data_path,'h5py',r,'left_timestamp_metadata_right_ts.h5py'))
    
    S[r] = {}
    for b in ['left','right','direct']:
        S[r][b] = {}
        for s in steers:
            o = Organized_moments[r][b][s]

            S[r][b][s] = {}
            for m in o:

                i = m['left_ts_index'][1]

                if np.abs(m['motor']-49) < 2 and np.abs(m['steer']-49) < 2 and m['behavioral_mode'] in ['left','right','center']:
                    #cr('.')
                    ctr+=1
                    continue
                if L['encoder'][i] < 0.1:
                    #cr('+')
                    continue
                    ectr+=1
                try:
                    if np.std(L['steer'][i-30:i+30]) < 1.0:
                        #cr('x')
                        ectr+=1
                        continue
                        
                except:
                    continue

                S[r][b][s][i] = m
                ctr+=1

            _,indexed_moments = get_key_sorted_elements_of_dic(S[r][b][s])
            S[r][b][s] = indexed_moments
            if True:
                figure(1)
                ii=[]
                els=S[r][b][s]
                for e in els:
                    ii.append(e['left_ts_index'][1])
                cg(r,b,s,len(ii))   
                if b == 'direct' and s == 'reverse':
                    c = 'k.'
                else:
                    c = C[b]
                plot(ii,c); spause()
                
                #raw_enter()
    Ctrs[r] = ctr        
    cy(r,ectr,ctr,int(ectr*100.0/(ctr*1.0)),'%')
    L.close()
    #raw_enter()






Randomized_moments = {}
Indicies = {}
Counts = {}

for r in S.keys():
    Indicies[r] = []
    Counts[r] = {}
    cg('Randomized_moments for',r)
    Randomized_moments[r] = []

    n_desired_moments = int(Ctrs[r]*0.1)

    for b in ['left','right','direct']:
        for s in ['low_steer','high_steer','reverse']:
            random.shuffle(S[r][b][s])

    while len(Randomized_moments[r]) < n_desired_moments:
        len_prev = len(Randomized_moments[r])
        for b in ['left','right','direct']:
            for s in ['low_steer','high_steer','reverse']:
                if len(S[r][b][s]) > 0:
                    Randomized_moments[r].append(S[r][b][s].pop())
        if len_prev == len(Randomized_moments[r]):
            cr("*** waring no progress beyond",len_prev,"for",r)


    for b in ['left','right','direct']:
        Counts[r][b] = {}
        for s in ['low_steer','high_steer','reverse']:
            Counts[r][b][s] = 0
    for m in Randomized_moments[r]:
        Counts[r][m['behavioral_mode']][m['steer_type']] += 1
        Indicies[r].append(m['left_ts_index'][1])
#for r in S.keys():
#    figure(d2s(r,'indicies'));plot(Indicies[r],'.') 




#
################################################################################







{'behavioral_mode': 'center',
 'left_ts_index': (1539052884.214, 45979),
 'motor': 61,
 'right_ts_index': (1539052884.2160001, 45979),
 'run_name': 'tegra-ubuntu_08Oct18_19h15m18s',
 'steer': 24}



def get_key_sorted_elements_of_dic(d,specific=None):
    ks = sorted(d.keys())
    els = []
    for k in ks:
        if specific == None:
            els.append(d[k])
        else:
            els.append(d[k][specific])
    return ks,els




import h5py
import contextlib

filename = '/tmp/foo.hdf5'
propfaid = h5py.h5p.create(h5py.h5p.FILE_ACCESS)
settings = list(propfaid.get_cache())
settings[2] *= 5
propfaid.set_cache(*settings)
with contextlib.closing(h5py.h5f.open(filename, fapl=propfaid)) as fid:
    f = h5py.File(fid)

     

#EOF
