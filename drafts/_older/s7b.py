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
	velocity = encoder/2.3  # rough guess
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
CA( )
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









########################################################################################
########################################################################################
########################################################################################
########################################################################################
###
def vec(heading,encoder,sample_frequency=30.0):
    velocity = encoder * P['vel-encoding coeficient']
    a = [0,1]
    a = array(rotatePoint([0,0],a,heading))
    a *= velocity/sample_frequency
    return a



path = opjD('Data/1_TB_Samsung_n1/left_direct_stop__29to30Oct2018/locations/local/left_direct_stop/h5py/tegra-ubuntu_29Oct18_13h28m05s')
L = h5r(opj(path,'left_timestamp_metadata_right_ts.h5py'))
O = h5r(opj(path,'original_timestamp_data.h5py'))
heading = L['gyro_heading_x'][:]
encoder = L['encoder'][:]
dheading = [0]
for i in range(1,len(heading)):
    dheading.append(heading[i]-heading[i-1])


def graphics_format(a,b,c,d):
    clf();plt_square();xylim(a,b,c,d)


CA()

P = {}
P['vel-encoding coeficient'] = (1.0/2.3)
sample_frequency = 30.0
prediction_sample_frequency = 3.33
unit_vector = na([0.,1.])


########################################################################################
#
def Pts():
    D = {}
    D['xy'] = [na([0.,0.])]
    D['indicies'] = [np.nan]
    D['mode'] = None
    D['max len'] = None
    D['cumulative heading'] = None
    D['i'] = None
    D['i start'] = None
    D['i stop'] = None
    D['sample_frequency'] = None
    D['step'] = None
    D['run straight through'] = None
    D['dheading'] = None
    D['encoder'] = None
    D['velocity'] = None
    D['step_size'] = None

    def function_type_1():
        D['cumulative heading'] += D['dheading'][D['i']]
        v = vec(D['cumulative heading'],D['encoder'][D['i']],D['sample_frequency'])
        D['xy'].append(v+D['xy'][-1])
    D['type 1'] = function_type_1

    def function_type_2():
        a = unit_vector * D['velocity'] / D['sample_frequency']
        D['xy'] = list(D['xy'])
        D['xy'].append(a+D['xy'][-1])
        D['xy'] = na(D['xy'])
        D['xy'] -= D['xy'][-1]
        D['xy'] = rotatePolygon(D['xy'],-D['dheading'][D['i']])
    D['type 2'] = function_type_2

    def function_step(f_type='type 1'):
        if D['i'] == None:
            D['i'] = D['i start']
        if D['i'] >= D['i stop']:
            return False
        D['indicies'].append(D['i'])
        D['velocity'] = D['encoder'][D['i']] * P['vel-encoding coeficient']
        if D['motor'][D['i']] < 49:
            D['velocity'] *= -1.0
        D[f_type]()
        if len(D['xy']) > D['max len']:
            for q in ['xy','indicies']:
                D[q] = D[q][-D['max len']:]
        D['i'] += D['step_size']
        return True
    D['step'] = function_step

    def function_show(reset_=True,mod_=3,lim_=200,pts_step=1,no_image=False,pt_color='r'):
        if np.mod(D['i'],mod_) == 0:
            #cb(D['i'])

            if D['velocity'] > 0:
                pcolor = pt_color
            else:
                pcolor = 'b'
            if reset_:
                graphics_format(-lim_,lim_,-lim_,lim_)
            pts_plot(na(D['xy'])[range(0,len(D['xy']),pts_step)],color=pcolor,sym='.')
            spause()
            if not no_image:
                mci(D['left_image'][D['i']],scale=2,delay=1)
    D['show'] = function_show

    return D
#
########################################################################################

start_i = 12000
lim_ = 2

R = Pts()
R['mode'] = 'dead reckoning'
R['i start'] = start_i
R['i stop'] = R['i start'] + 3000
R['cumulative heading'] = 0
R['dheading'] = dheading
R['encoder'] = encoder
R['motor'] = L['motor']
R['sample_frequency'] = 30.0
R['left_image'] = O['left_image']['vals']
R['max len'] = 9000
R['step_size'] = 1



while R['step']('type 2'):

    C = Pts()
    C['mode'] = 'direct prediction'
    C['max len'] = 30
    C['i start'] = R['i']-R['step_size']
    C['i stop'] = C['i start'] + C['max len']
    C['cumulative heading'] = 0
    C['dheading'] = dheading
    C['encoder'] = encoder
    C['motor'] = L['motor']
    C['sample_frequency'] = 30
    C['left_image'] = O['left_image']['vals']
    C['step_size'] = 1

    while C['step']('type 1'):
        cg(R['i'],C['i'],R['i']-C['i'])
        pass

    R['show'](reset_=False,mod_=1,lim_=lim_,pts_step=1)
    
    C['show'](mod_=1,lim_=lim_,pts_step=1,no_image=True,pt_color='g')

    R['xy']=list(R['xy'])
    pp = R['xy'].pop()
    R['xy'] += list(C['xy'])
    R['xy'].append(pp)
###
########################################################################################
########################################################################################
########################################################################################






########################################################################################
########################################################################################
########################################################################################
####
def CV2Plot(height_in_pixels,width_in_pixels,pixels_per_unit,x_origin_in_pixels=None,y_origin_in_pixels=None):
    if x_origin_in_pixels == None:
        x_origin_in_pixels = intr(width_in_pixels/2.0)
    if y_origin_in_pixels == None:
        y_origin_in_pixels = intr(height_in_pixels/2.0)
    D = {}
    D['verbose'] = True
    if D['verbose']:
        cy(x_origin_in_pixels,y_origin_in_pixels)
    D['image'] = zeros((height_in_pixels,width_in_pixels,3),np.uint8)
    def function_show():
        mci(D['image'],scale=4.0)
    def function_safe(px,py):
        if px >= 0:
            if py >= 0:
                if py < height_in_pixels:
                    if px < width_in_pixels:
                        return True
        if D['verbose']:
            cr('not safe')
        return False
    def function_get_pixel(x,y):
        px = intr(x * pixels_per_unit)
        py = intr(-y * pixels_per_unit)
        px += x_origin_in_pixels
        py += y_origin_in_pixels
        if D['verbose']:
            cb(x,y,"->",px,py)
        return px,py
    def function_add_point_pixel_version(px,py,c=[255,255,255]):
        if function_safe(px,py):
            D['image'][py,px,:] = c
    def function_add_point_xy_version(x,y,c=[255,255,255]):
        px,py = D['get pixel'](x,y)
        if D['safe?'](px,py):
            D['image'][py,px,:] = c
    def function_pts_plot(xys,c=[255,255,255]):
        if type(c) == str:
            if c == 'r':
                c = [255,0,0]
            elif c == 'g':
                c = [0,255,0]
            elif c == 'r':
                c = [0,0,255]  
            else:
                cr('warning, unknown color:',c)
                c = [255,255,255]
        for i in rlen(xys):
            D['add point (xy_version)'](xys[0],xys[1],c)
    def function_clear():
        D['image'] *= 0
    D['show'] = function_show
    D['safe?'] = function_safe
    D['add point (pixel_version)'] = function_add_point_pixel_version
    D['add point (xy_version)'] = function_add_point_xy_version
    D['get pixel'] = function_get_pixel
    D['pts_plot'] = function_pts_plot
    D['clear'] = function_clear
    return D
####
########################################################################################
########################################################################################
########################################################################################

import torch
P={}
P['WEIGHTS_FILE_PATH'] = '/home/karlzipser/Desktop/Networks/net_24Dec2018_12imgs_projections/weights/net_25Dec18_18h35m43s.infer'
save_data = torch.load(P['WEIGHTS_FILE_PATH'])
n = save_data['net']

a = n['pre_metadata_features.3.expand3x3.weight']

a=n['final_output.1.bias'].cpu().numpy()
b=zeros(40)
b[:20]=a
b[-20:]=a
n['final_output.1.bias'] = torch.from_numpy(b).cuda()

a=save_data['net']['final_output.1.weight'].cpu().numpy()
b=zeros((40,512,1,1))
b[:20,:,:,:]=a
b[-20:,:,:,:]=a
save_data['net']['final_output.1.weight'] = torch.from_numpy(b).cuda()
print(shape(save_data['net']['final_output.1.weight'].cpu().numpy()))
raw_enter()




########################################################################################
########################################################################################
########################################################################################
#####
import torch

from kzpy3.Train_app.nets.SqueezeNet40 import SqueezeNet
torch.set_default_tensor_type('torch.FloatTensor') 
torch.cuda.set_device(0)
torch.cuda.device(0)

def create_net():
    return SqueezeNet().cuda()

def load_net(path):
    save_data = torch.load(path)
    net = save_data['net']
    return net

def save_net(net,path):
    weights = {'net':net}
    torch.save(weights,path)

def show_net(net,layer,fig='',correction=False):
    p = net[layer] 
    q = p.cpu().numpy() 
    q = q[:,:,0,0]
    if correction:
        q[:,128]/=10.
    mi(q,fig+layer)
    figure(fig+layer+' ')
    plot([0,256],[0,0],'b-')
    plot(q.transpose(1,0),'ko')
    raw_enter()

save_net(create_net(),opjD('initial_weights.infer'))
A = load_net(opjD('initial_weights.infer'))
B = load_net(opjD('Networks/net_24Dec2018_12imgs_projections/weights/net_25Dec18_20h12m56s.infer'))
show_net(B,'post_metadata_features.0.squeeze.weight',correction=True)

B['post_metadata_features.0.squeeze.weight'] = A['post_metadata_features.0.squeeze.weight']
#save_net(B,opjD('trained_net_with_randomized_layer.infer'))
torch.save(B,opjD('trained_net_with_randomized_layer.infer'))
####
########################################################################################
########################################################################################
########################################################################################


D = {}
torch.set_default_tensor_type('torch.FloatTensor') 
torch.cuda.set_device(0)
torch.cuda.device(0)

D['net'] = SqueezeNet().cuda()
#D['criterion'] = torch.nn.MSELoss().cuda()
#D['optimizer'] = torch.optim.Adadelta(D['net'].parameters())
save_data = torch.load(opjD('Networks/net_24Dec2018_12imgs_projections/weights/net_25Dec18_20h12m56s.infer'))
#CS_("loading "+_['WEIGHTS_FILE_PATH'])
D['net'].load_state_dict(save_data['net'])


ctr = 0
for param in net.parameters():
    rg = True
    if ctr < 8:
        rg = False
    param.requires_grad = rg
    if rg:
        f = cg
    else:
        f = cr
    f(ctr,param.size())
    ctr += 1

A = load_net(opjD('initial_weights.infer'))
B = load_net(opjD('Networks/net_24Dec2018_12imgs_projections/weights/net_25Dec18_20h12m56s.infer'))





######################
#
"""
http://www.jonwitts.co.uk/archives/896
"""

import sys, termios, tty, os, time
 
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
 
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
 
button_delay = 0.2
 
while True:
    char = getch()
 
    if (char == "p"):
        print("Stop!")
        exit(0)
 
    if (char == "a"):
        print("Left pressed")
        time.sleep(button_delay)
 
    elif (char == "d"):
        print("Right pressed")
        time.sleep(button_delay)
 
    elif (char == "w"):
        print("Up pressed")
        time.sleep(button_delay)
 
    elif (char == "s"):
        print("Down pressed")
        time.sleep(button_delay)
 
    elif (char == "1"):
        print("Number 1 pressed")
        time.sleep(button_delay)
#
######################



while True:
    char = getch()
    print char







from kzpy3.utils2 import *

#
##################################################################
#

Int32 = 'std_msgs.msg.Int32'
Float32 = 'std_msgs.msg.Float32'
Vec3 = 'geometry_msgs.msg.Vector3'
Str = 'std_msgs.msg.String'
Img = 'sensor_msgs.msg.Image'

Queue_sizes = {
    Int32:5,
    Float32:5,
    Vec3:5,
    Str:5,
    Img:1,
}

def get_ros_start_strs(node_name):
    rospyinit_strs = ["\nrospy.init_node('"+node_name+"',anonymous=True,disable_signal=True)\n"]
    return rospyinit_strs


def get_ros_publisher_strs(Rostopics_to_publish,dic_name):
    print Rostopics_to_publish
    pub_setup_strs = []
    pub_publish_strs = []
    P_publisher_strs = {}
    for topic in Rostopics_to_publish:
        assert len(topic) == 2
        assert type(topic[0]) == str
        assert type(topic[1]) == str
        name = topic[0]
        rtype = topic[1]
        CS_(d2s(name,rtype))
        pub_name = get_safe_name(name)+'_pub'
        pub_setup_strs.append(
                d2n(dic_name,"['",name,"_pub']"," = rospy.Publisher('",name,"',",rtype,",queue_size=",Queue_sizes[rtype],')'))
    pub_setup_strs.append('\n')
    return pub_setup_strs


def get_ros_subscriber_strs(rostopics_subscribe_to,dic_name):
    subscription_strs = []
    callback_strs = []
    for topic in rostopics_subscribe_to:
        assert type(topic) == tuple
        assert len(topic) <= 3
        raw_name = topic[0]
        assert type(raw_name) == str
        safe_name = get_safe_name(raw_name)
        rtype = topic[1]
        assert type(rtype) == str
        if len(topic) == 3:
            make_callback = topic[2]
        else:
            make_callback = True
        assert type(make_callback) == bool
        if make_callback:
            callback_strs.append("""def """+safe_name+"""_callback(msg):\n\t"""+dic_name+"""['"""+raw_name+"""'] = msg.data\n""")
        subscription_strs.append("""rospy.Subscriber('"""+raw_name+"""',"""+rtype+""",callback="""+safe_name+"""_callback)""")
    subscription_strs.append('\n')
    return callback_strs,subscription_strs
#
##################################################################
#

node_name = 'run_arduino'

stopics = [
    ('cmd/steer',Int32),
    ('cmd/camera',Int32),
    ('cmd/motor',Int32,False),
    ('/os1_node/image',Img),
    ('data_saving',Int32),
]



ptopics = [
    ('human_agent',Int32),
    ('drive_mode',Int32),
    ('behavioral_mode',Int32),
    ('button_number',Int32),
    ('steer',Int32),
    ('motor',Int32),
    ('encoder',Float32),
    ('gyro',Float32),
    ('gyro_heading',Float32),
    ('acc',Vec3),
]
flex_names = [
    'FL0',
    'FL1',
    'FL2',
    'FL3',
    'FR0',
    'FR1',
    'FR2',
    'FR3',
    'FC0',
    'FC1',
    'FC2',
    'FC3',
]
for name in flex_names:
    ptopics.append( (name,Float32)  )


r = get_ros_start_strs(node_name)
c,s = get_ros_subscriber_strs(stopics,'_')
p = get_ros_publisher_strs(ptopics,'_')

def lp(lst):
    for e in lst:
        cb(e)

lp(r)
lp(c)
lp(s)
lp(p)













########################################################################################
########################################################################################
########################################################################################
####
def CV2Plot_v2(img,pixels_per_unit=1.0,x_origin_in_pixels=None,y_origin_in_pixels=None):
    height_in_pixels,width_in_pixels,__ = shape(img)
    if x_origin_in_pixels == None:
        x_origin_in_pixels = intr(width_in_pixels/2.0)
    if y_origin_in_pixels == None:
        y_origin_in_pixels = intr(height_in_pixels/2.0)
    D = {}
    D['verbose'] = True
    if D['verbose']:
        cy(x_origin_in_pixels,y_origin_in_pixels)
    D['image'] = img
    def function_show(autocontrast=True):
        
        img = D['image']
        if autocontrast:
            img = z2_255_by_channel(img)
            #cg(img.min(),img.max())
        mci(img,scale=4.0,delay=1)
    def function_safe(px,py):
        if px >= 0:
            if py >= 0:
                if py < height_in_pixels:
                    if px < width_in_pixels:
                        return True
        if D['verbose']:
            cr('not safe')
        return False
    def function_get_pixel(x,y):
        px = intr(x * pixels_per_unit)
        py = intr(-y * pixels_per_unit)
        px += x_origin_in_pixels
        py += y_origin_in_pixels
        if D['verbose']:
            cb(x,y,"->",px,py)
        return px,py
    def function_plot_point_xy_version(x,y,c=[255,255,255],add_mode=False):
        px,py = D['get pixel'](x,y)
        if D['safe?'](px,py):
            if not add_mode:
                D['image'][py,px,:] = c
            else:
                D['image'][py,px,:] += na(c,np.uint8)
    def function_pts_plot(xys,c=[255,255,255],add_mode=False):
        if type(c) == str:
            if add_mode:
                n = 1
            else:
                n = 255
            if c == 'r':
                c = [n,0,0]
            elif c == 'g':
                c = [0,n,0]
            elif c == 'b':
                c = [0,0,n]  
            else:
                cr('warning, unknown color:',c)
                c = [255,255,255]
        for i in rlen(xys):
            D['plot point (xy_version)'](xys[i,0],xys[i,1],c,add_mode)
    def function_clear():
        D['image'] *= 0
    D['show'] = function_show
    D['safe?'] = function_safe
    D['plot point (xy_version)'] = function_plot_point_xy_version
    D['get pixel'] = function_get_pixel
    D['pts_plot'] = function_pts_plot
    D['clear'] = function_clear
    return D

if False: # examples
    img=z2_255(np.random.randn(50,100,3))

    c = CV2Plot_v2(img,1)
    c['pts_plot'](na(np.random.randn(100,2)*10))
    c['show']()

    d = CV2Plot_v2(img,10.)
    d['pts_plot'](na(np.random.randn(100,2)*10))
    d['show']()
####
########################################################################################
########################################################################################
########################################################################################


def get_terminal_size():
    rows, columns = os.popen('stty size', 'r').read().split()
    return int(rows),int(columns)




<<<<<<< HEAD
def REctangle(x,y,dx,dy,width,height,color,mass):
    D = {}
    D['x'] = x
    D['y'] = y
    D['dx'] = dx
    D['dy'] = dy
    D['width'] = width
    D['height'] = height
    D['color'] = color
    D['mass'] = mass

    def function_show(img):
        pass
=======
timer = Timer(150)
rtimer = Timer(1/30.)
while not timer.check():
    if rtimer.check():
        rtimer.reset()
        nrows,ncols = get_terminal_size()
        x = 0.9*np.sin(time.time())
        y = 0.5*np.sin(time.time()*8.)
        xcol = int((x+1.0)/2.0 * ncols)
        ycol = int((y+1.0)/2.0 * ncols)
        row_str = ''
        for i in range(ncolumns):
            if i == xcol:
                row_str += 'X'
            elif i == ycol:
                row_str += 'Y'
            else:
                row_str += ' '
        #cprint(row_str,'yellow','on_blue')
        print(row_str)
    else:
        time.sleep(rtimer.time_s/5.)
>>>>>>> 89cddd9068408f8acc61ce1ddae1320ef512cd09

    return D

Keyboard_keys = {
    'p':'up right',
    '.':'down right',
    'q':'up left',
    'z':'up left',
    }

timer = Timer(15*minutes)
rtimer = Timer(1./30.*seconds*2)
while not timer.check():
    if rtimer.check():
        rtimer.reset()        
        x = 1.0*np.sin(time.time())
        y = 0.25*np.sin(time.time()*4.)
        xper = int((x+1.0)/2.0 * 100)
        yper = int((y+1.0)/2.0 * 100)
        row_str = format_row([('X',xper),('Y',yper),('|',50)])
        print(row_str)
    else:
        time.sleep(rtimer.time_s/5.)

_ = {}
_['box height'] = 500
_['box width'] = 200
_['img'] = zeros((_['box height'],_['box width']))

_['paddle height'] = 10
_['paddle width'] = 50

_['paddle'] = {}
_['paddle']['left'] = {}
_['paddle']['left']['x position'] = _['paddle width']/2
_['paddle']['left']['y position'] = _['box height']/2
_['paddle']['right'] = {}
_['paddle']['right']['x position'] = _['box width']-_['paddle width']/2
_['paddle']['right']['y position'] = _['box height']/2

for side in ['left','right']:
    x = _['paddle'][side]['x position']
    y = _['paddle'][side]['y position']
    pw = _['paddle width']
    ph = _['paddle height']
    img = _['img']
    img[y-ph/2:y+ph/2,x-pw/2:x+pw/2] = 127

_['img'][0,0] = 0
_['img'][0,1] = 255
mi(_['img'])



P={}
P['current state'] = 'none'
P['now in calibration mode'] = True
def State():
    D = {}
    D['type'] = 'State'
    D['Since-entry timer:'] = Timer()
    def function_can_enter(P):
        cy(D['type'])
        return False
    def function_upon_entry(P):
        cy(D['type'])
        P['current state'] = D['type']
        cb('entering state',D['type'])
        D['Since-entry timer:'].reset()
    def function_upon_exit(P):
        cy(D['type'])
        cb('leaving state',D['type'])
        pass
    def function_time_to_exit(P):
        cy(D['type'])
        return False
    def function_to_do(P):
        cy(D['type'])
        pass
    D['Can this state can be entered?'] = function_can_enter
    D['Upon entry do this...'] = function_upon_entry
    D['To do while in this state:'] = function_to_do
    D['Upon exit do this...'] = function_upon_exit
    u'√'
    return D


def Calibrate_0():
    D = State()
    D['type'] = 'Calibrate_0'
    D['Since-entry timer:'] = Timer(0.1)
    D['Upon entry do this... OVERRIDE'] = D['Upon entry do this...']
    def function_upon_entry(P):
        cg('from State:')
        D['Upon entry do this... OVERRIDE'](P)
        cg('from Calibrate_0:')
        cr('hi')
    def function_can_enter(P):
        cy(D['type'])
        if P['now in calibration mode']:
            if P['current state'] not in ['Calibrate_0','Calibrate_1','Calibrate_2']:
                return True
        return False
    def function_time_to_exit(P):
        cy(D['type'])
        if D['type'] != P['current state']:
            return False
        if D['Since-entry timer:'].check():
            return True
    D['Is it time to exit?'] = function_time_to_exit
    D['Can this state can be entered?'] = function_can_enter
    D['Upon entry do this...'] = function_upon_entry
    return D


C=Calibrate_0()
print C['Can this state can be entered?'](P)
print C['Upon entry do this...'](P)
print C['Is it time to exit?'](P)
print C['Can this state can be entered?'](P)
print C['Is it time to exit?'](P)



<<<<<<< HEAD
a=arange(6).reshape(3,2)
b=arange(2).reshape(2,1)
timer = Timer(5)
ctr = 0
while not timer.check():
    c = a.dot(b)
    ctr += 1
print ctr
timer = Timer(5)


a = randn(30*10*3,128,128)
b = randn(30*10*3,128,128)
ctr = 0
while not timer.check():
    c = a.dot(b)
    ctr += 1
print ctr



torch.set_default_tensor_type('torch.FloatTensor') 
torch.cuda.set_device(0)
torch.cuda.device(0)

a = torch.Tensor([[1,2,3],[1,2,3]]).view(-1,2)
b = torch.Tensor([[2,1]]).view(2,-1)
a = a.cuda()
b = b.cuda()
timer = Timer(5)
ctr = 0
while not timer.check():
    c = torch.mm(a,b)
    ctr += 1
print ctr

a = torch.Tensor(np.random.randn(100,3,3))
b = torch.Tensor(np.random.randn(100,3,1))
a = a.cuda()
b = b.cuda()
timer = Timer(5)
ctr = 0
while not timer.check():
    c = torch.bmm(a,b)
    ctr += 1
print ctr



timer = Timer(5)
a = torch.Tensor(randn(30*10*3,3,3))
b = torch.Tensor(randn(30*10*3,3,2))
a = a.cuda()
b = b.cuda()
ctr = 0
timer = Timer(5)
#while not timer.check():
c = torch.bmm(a,b)
ctr += 1
print ctr/timer.time()



a = torch.Tensor(randn(3,3))
b = torch.Tensor(randn(3,1))
print torch.mm(a,b)


timer = Timer()
a = torch.Tensor(randn(30*10*3,3,3))
b = torch.Tensor(randn(30*10*3,3,2))
a = a.cuda()
b = b.cuda()
ctr = 0
#while not timer.check():
c = torch.bmm(a,b)
ctr += 1
print ctr/timer.time(),timer.time()



a = torch.Tensor(randn(3,3))
b = torch.Tensor(randn(3,1))
print torch.mm(a,b)








class Point2:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Point3:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z


def project(p, mat):



    x = mat[0][0] * p.x + mat[0][1] * p.y + mat[0][2] * p.z + mat[0][3] * 1
    y = mat[1][0] * p.x + mat[1][1] * p.y + mat[1][2] * p.z + mat[1][3] * 1
    w = mat[3][0] * p.x + mat[3][1] * p.y + mat[3][2] * p.z + mat[3][3] * 1
    return Point2(168 * (x / w + 1) / 2., 94 - 94 * (y / w + 1) / 2.)



import torch
torch.set_default_tensor_type('torch.FloatTensor') 
torch.cuda.set_device(0)
torch.cuda.device(0)

mat = [
    [1.1038363893132925, 0, -0.06913056289047548, -0.011453007708049912],
    [-0.0015083235462127753, 1, -0.04276381228842596, -0.4265748298235925],
    [0.002382129088680296, 0, 1.114622282258332, 0.7840441986828541]]
batch_size = 10*3*30
n = 100
mat_batch = []
for i in range(batch_size):
    mat_batch.append(mat)
a = torch.Tensor(mat_batch).cuda()
timer = Timer()
for i in range(n):
    p = np.random.rand(batch_size,4,1)
    b = torch.Tensor(p).cuda()
    q = torch.bmm(a,b)
print timer.time()/(1.0*n)

q.cpu().numpy()




import torch
torch.set_default_tensor_type('torch.FloatTensor') 
torch.cuda.set_device(0)
torch.cuda.device(0)

def rotatePolygon_cuda(polygon,theta):
    """http://stackoverflow.com/questions/20023209/function-for-rotating-2d-objects
    Rotates the given polygon which consists of corners represented as (x,y),
    around the ORIGIN, clock-wise, theta degrees. Modified for pytorch."""
    # polygon must be of shape (n,2,1), not (n,2) which is typical.
    if len(shape(polygon)) == 2:
        new_shape = list(shape(polygon))+[1]
        A = zeros(new_shape)
        A[:,:,0] = polygon
        polygon = A
    theta = np.radians(theta)
    R = [[np.cos(theta),-np.sin(theta),],
        [np.sin(theta),np.cos(theta)]]
    S =  len(polygon) * [R]
    St = torch.Tensor(S).cuda()
    Pt = torch.Tensor(polygon).cuda() #4.71 1955 3252.39
    polygon = torch.bmm(St,Pt)
    return polygon





#CA()
U = CV2Plot(1000,1000,100,500,500,1.0)

n = 900
polygon = torch.Tensor(np.random.randn(n,2,1))
theta = 0.01
hz = Timer(5)
for i in range(100000000):
    r = rotatePolygon_cuda(polygon,i)
    r = r.cpu().numpy()
    
    #clf();plt_square(5)
    U['clear']()
    U['pts_plot'](r)
    U['show']()
    #spause()
    hz.freq()
    
print timer.time()




=======


class State:
    def __init__(self):
        pass
    def a(self):
        print(1)

class Exit_is_Timed(State):
    def __init__(self):
        pass
    def a(self):
        super(Exit_is_Timed,self).a()
        print(2)
>>>>>>> 74372d6520c7fec277a2c14d9342461af835d7b5






import roslib
from std_msgs.msg import Int32MultiArray
pub = rospy.Publisher('vals',Int32MultiArray,queue_size = 10)
rospy.init_node('blah')

while not rospy.is_shutdown():
    a = list((10000*np.random.rand(10)).astype(int))
    print a
    pub.publish(data=a)
    time.sleep(0.1)








def Cv2Plot(
        img,
        box_0to1 = None,        
        box_real = ((-1.0,1.0),(0,4.0*np.pi))
        row = (2,4),
        col = (1,3),
    ):

    if box_0to1 == None:
        for q in row,col:
            assert type(q) == tuple
            assert len(q) == 2
            for i in [0,1]:
                assert is_number(q[i])

    box_0to1 = (    
                ( (col[0]-1)/(1.0*col[1]),
                  (col[0])/(1.0*col[1]), ),
                ( (row[1]-row[0])/(1.0*row[1]),
                  (row[1]-row[0]+1)/(1.0*row[1]),),)

    height_in_pixels = shape(img)[0]
    width_in_pixels = shape(img)[1]
    row_height = int(height_in_pixels/row(1))
    col_width  = int(width_in_pixels /col(1))



########################################################################################
########################################################################################
########################################################################################
####
def Cv2Plot(
        img,
        x_pixels_per=1,
        y_pixels_per=1,
        x_origin=None,
        y_origin=None
    ):

    height_in_pixels = shape(img)[0]
    width_in_pixels = shape(img)[1]

    if x_origin == None:
        x_origin = 0.5
    if y_origin_ == None:
        y_origin0.5
    D = {}
    D['verbose'] = False
    D['image'] = img
    assert len(shape(img)) == 3
    assert type(img) == np.uint8

    def function_show(autocontrast=True,delay=1,title='image',scale=1.0):
        img = D['image']
        if autocontrast:
            img = z2_255_by_channel(img)
        mci(img,scale=scale,delay=delay,title=title)

    def function_safe(px,py):
        if px >= 0:
            if py >= 0:
                if py < height_in_pixels:
                    if px < width_in_pixels:
                        return True
        if D['verbose']:
            cr('not safe')
        return False

    def function_get_pixel(x,y):
        px = intr(x * x_pixels_per)
        py = intr(-y * y_pixels_per)
        px += x_origin * width_in_pixels
        py += y_origin * height_in_pixels
        if D['verbose']:
            cb(x,y,"->",px,py)
        return px,py

    def function_plot_point_xy_version(x,y,c=[255,255,255],add_mode=False):
        px,py = D['get pixel'](x,y)
        if D['safe?'](px,py):
            if not add_mode:
                D['image'][py,px,:] = c
            else:
                D['image'][py,px,:] += na(c,np.uint8)

    def function_pts_plot(xys,c=[255,255,255],add_mode=False):
        if type(c) == str:
            if add_mode:
                n = 1
            else:
                n = 255
            if c == 'r':
                c = [n,0,0]
            elif c == 'g':
                c = [0,n,0]
            elif c == 'b':
                c = [0,0,n]  
            else:
                cr('warning, unknown color:',c)
                c = [255,255,255]
        for i in rlen(xys):
            D['plot point (xy_version)'](xys[i,0],xys[i,1],c,add_mode)

    def function_clear():
        D['image'] *= 0
        
    D['show'] = function_show
    D['safe?'] = function_safe
    D['plot point (xy_version)'] = function_plot_point_xy_version
    D['get pixel'] = function_get_pixel
    D['pts_plot'] = function_pts_plot
    D['clear'] = function_clear
    return D

#
########################################################################################
#

########################################################################################
########################################################################################
########################################################################################
####













#EOF
