##############################################################
####################### IMPORT ################################
## python kzpy3/VT_net2__5April2019/main.py run tegra-ubuntu_29Oct18_13h28m05s
## can run with ROS with car network running, or from preprocessed data.
############
from kzpy3.vis3 import *
from scipy.optimize import curve_fit
import kzpy3.Menu_app.menu2 as menu2
import default_values
import fit3d#_torch as fit3d
exec(identify_file_str)
_ = default_values._

project_path = pname(__file__).replace(opjh(),'')
if project_path[0] == '/':
    project_path = project_path[1:]
sys_str = d2s('mkdir -p',opj(project_path,'__local__'))
cg(sys_str)
os.system(sys_str)
cg("To start menu:\n\tpython kzpy3/Menu_app/menu2.py path",project_path,"dic _")

##
#############################################################
#############################################################

#############################################################
####################### MENU ################################
##
if _['start menu automatically'] and using_linux():
    dic_name = "_"
    sys_str = d2n("gnome-terminal --geometry 40x30+100+200 -x python kzpy3/Menu_app/menu2.py path ",project_path," dic ",dic_name)
    cr(sys_str)
    os.system(sys_str)

parameter_file_load_timer = Timer(_['load_timer_time'])

def load_parameters(_,customer='VT menu'):
    if parameter_file_load_timer.check():
        Topics = menu2.load_Topics(project_path,first_load=False,customer=customer)
        if type(Topics) == dict:
            for t in Topics['To Expose'][customer]:
                if t in Arguments:
                    topic_warning(t)
                if '!' in t:
                    pass
                else:
                    _[t] = Topics[t]
        parameter_file_load_timer.reset()

##
##############################################################
##############################################################

##############################################################
##############################################################
##
assert 'run' in Arguments
runs = lo(opjD('Data/Network_Predictions/runs.pkl'))
Runs = {}
for r in runs:
    Runs[fname(r)] = r
run_path = Runs[Arguments['run']]
run_path = run_path.replace('/media/karlzipser','/home/karlzipser/Desktop/Data')

if True:
    U = lo(opjD('Data/Network_Predictions',fname(run_path)+'.net_predictions.pkl'))
    L,O,___ = open_run(run_name=Arguments['run'],h5py_path=pname(run_path),want_list=['L','O'])
    _['headings'] = L['gyro_heading_x'][:]
    _['encoders'] = L['encoder'][:]

Left_timestamps_to_left_indicies = {}
t0 = L['ts'][0]

if _['save metadata']:
    metadata_img_list = []
blank_meta = np.zeros((23,41,3),np.uint8)
for i in rlen(L['ts']):
    t = (1000.0*(L['ts'][i] - t0)).astype(int)
    Left_timestamps_to_left_indicies[t] = i
    if _['save metadata']:
        metadata_img_list.append(blank_meta)
##
##############################################################
##############################################################


##############################################################
##############################################################
##
Colors = {'direct':'b','left':'r','right':'g'}
RGBs = {'direct':(0,0,255),'right':(0,255,0),'left':(255,0,0)}
Color_index = {'direct':2,'right':1,'left':0}
##
##############################################################
##############################################################


##############################################################
##############################################################
###
S = {}
bcs = '/bair_car/'
S['ts'] = 0
S['ts_prev'] = 0
S['sample_frequency'] = 0
S['gyro_heading_x'] = 0
S['gyro_heading_x_prev'] = 0
S['d_heading'] = 0
S['encoder'] = 0

import std_msgs.msg
import geometry_msgs.msg
from std_msgs.msg import Int32MultiArray
from sensor_msgs.msg import Image
import cv_bridge
bridge = cv_bridge.CvBridge()

for modality in ['headings','encoders','motors']:
    for side in ['left','direct','right']:
        s = """
def MODALITY_SIDE_callback(data):
    S['MODALITY_SIDE'] = na(data.data).astype(float)/1000.

rospy.Subscriber('/MODALITY_SIDE', std_msgs.msg.Int32MultiArray, callback= MODALITY_SIDE_callback)


        """
        s = s.replace('MODALITY',modality).replace('SIDE',side)
        #print s
        exec(s)

def encoder_callback(data):
    S['encoder'] = data.data

rospy.Subscriber(bcs+'encoder', std_msgs.msg.Float32, callback=encoder_callback)

def gyro_heading_x_callback(data):
    S['gyro_heading_x_prev'] = S['gyro_heading_x']
    S['gyro_heading_x'] = data.x
    S['d_heading'] = S['gyro_heading_x'] - S['gyro_heading_x_prev']
    S['ts_prev'] = S['ts']
    S['ts'] = time.time()
    S['sample_frequency'] = 1.0 / (S['ts']-S['ts_prev'])

rospy.Subscriber(bcs+'gyro_heading', geometry_msgs.msg.Vector3, callback=gyro_heading_x_callback)

def left_callback(data):
    S['left_image'] = bridge.imgmsg_to_cv2(data,'rgb8')


rospy.Subscriber(
    bcs+"/zed/left/image_rect_color",
    Image,
    left_callback,
    queue_size = 1)


###
#####################################################
#####################################################

if True:
    Pub = {}
    for modality in ['headings','encoders','motors']:
        Pub[modality] = {}
        for behavioral_mode in _['behavioral_mode_list']:
            Pub[modality][behavioral_mode] = rospy.Publisher(modality+'_'+behavioral_mode,Int32MultiArray,queue_size = 10)
    Pub['gyro_heading'] = rospy.Publisher(bcs+'gyro_heading', geometry_msgs.msg.Vector3, queue_size=10)
    Pub['encoder'] = rospy.Publisher(bcs+'encoder',std_msgs.msg.Float32,queue_size=5)

rospy.init_node('VT_node',anonymous=True,disable_signals=True)
###
##############################################################
##############################################################


##############################################################
##############################################################
###
def vec(heading,encoder,motor,sample_frequency,_):
    velocity = encoder * _['vel-encoding coeficient'] # rough guess
    if motor < 49:
        velocity *= -1.0
    a = [0,1]
    a = array(rotatePoint([0,0],a,heading))
    a *= velocity/sample_frequency
    return array(a)


def f(x,A,B):
    return A*x + B


def get_predictions2D(headings,encoders,motors,sample_frequency,_):
    xy = array([0.0,0.0])
    xys = []
    for i in range(len(headings)):
        v = vec(headings[i],encoders[i],motors[i],_['vec sample frequency'],_) #3.33)
        xy += v
        xys.append(xy.copy())
    if False:
        points_to_fit = na(xys[:3])
        x = points_to_fit[:,0]
        y = points_to_fit[:,1]
        m,b = curve_fit(f,x,y)[0]
        ang = np.degrees(angle_between([0,1],[1,m]))
    pts2D_1step = na(xys)
    return pts2D_1step


def get_prediction_images_3D(pts2D_1step_list,img,_):#left_index):
    rmax = 7
    metadata_version_list = None
    img1 = cv2.resize(img,(41,23))
    metadata_version_list = []
    img2 = 0*img1.astype(np.float)
    for q in range(len(pts2D_1step_list)-1,-1,-1):
        Pts2D_1step = pts2D_1step_list[q]

        for behavioral_mode in Pts2D_1step.keys():
            pts2D_1step = Pts2D_1step[behavioral_mode]
            for i in rlen(pts2D_1step):
                a = pts2D_1step[i,:]
                if a[1]<0:
                    continue
                try:
                    r = int(5.0/np.sqrt(a[0]**2+(a[1])**2))
                except:
                    r = 1
        
                b = fit3d.Point3(a[0], 0, a[1]-_['backup parameter'])
                c = fit3d.project(b, fit3d.mat)

                try:
                    if True:
                        good = True
                        if c.x < 0 or c.x >= 168:
                            good = False
                        elif c.y < 0 or c.y >= 94:
                            good = False
                        if good:             
                            if r < rmax:
                                cv2.circle(img,(int(c.x),int(c.y)),r,RGBs[behavioral_mode])
                    good = True
                    cx = intr(c.x * 0.245)
                    cy = intr(c.y * 0.245)
                    if cx < 0 or cx >= 41:
                        good = False
                    elif cy < 0 or cy >= 23:
                        good = False
                    if good:               
                        img1[cy,cx,:] = RGBs[behavioral_mode]
                        img2[cy,cx,Color_index[behavioral_mode]] += 1

                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    CS_('Exception!',emphasis=True)
                    CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
                    cr(r)

    img = cv2.resize(img,(168*2,94*2))
    if _['use center line']:
        img[:,168,:] = int((127+255)/2)
    left_camera_3D_img = img


    for y in range(11,23):
        for c in range(3):
            if img2[y,:,c].max() > 0:
                img2[y,:,c] = z2o(img2[y,:,c])
    metadata_3D_img = (255*img2).astype(np.uint8)

    return left_camera_3D_img,metadata_3D_img
##
##############################################################
##############################################################
###
def get__pts2D_multi_step(d_heading,encoder,sample_frequency,headings,encoders,motors,pts2D_multi_step,_):

    Pts2D_1step = {}

    for behavioral_mode in _['behavioral_mode_list']:

        Pts2D_1step[behavioral_mode] = \
            get_predictions2D(
                headings[behavioral_mode],
                encoders[behavioral_mode],
                motors[behavioral_mode],
                sample_frequency,
                _)
    
    pts2D_multi_step.append({})

    for behavioral_mode in _['behavioral_mode_list']:
        
        if len(pts2D_multi_step) > _['num timesteps']:
            pts2D_multi_step = pts2D_multi_step[-_['num timesteps']:]

        pts2D_multi_step[-1][behavioral_mode] = Pts2D_1step[behavioral_mode] #list(Pts2D_1step[behavioral_mode])

    velocity = encoder * _['vel-encoding coeficient']

    trajectory_vector = na([0,1]) * velocity / sample_frequency

    for behavioral_mode in _['behavioral_mode_list']:

        for i in rlen(pts2D_multi_step):
            pts2D_multi_step[i][behavioral_mode] = rotatePolygon(pts2D_multi_step[i][behavioral_mode],-d_heading)

        pts2D_multi_step[-1][behavioral_mode].append(trajectory_vector)

        for i in rlen(pts2D_multi_step):

            pts2D_multi_step[i][behavioral_mode] = pts2D_multi_step[i][behavioral_mode] - pts2D_multi_step[-1][behavioral_mode][-1]

    return pts2D_multi_step
###
##############################################################




################################################################
################################################################
###
def prepare_2D_and_3D_images(Prediction2D_plot,pts2D_multi_step,source,_):

    d_heading,gyro_heading_x,encoder,sample_frequency,headings,encoders,motors = get_SOURCE_DEPENDENT_data(source,_)

    pts2D_multi_step = get__pts2D_multi_step(d_heading,encoder,sample_frequency,headings,encoders,motors,pts2D_multi_step,_)

    Prediction2D_plot['clear']()

    for behavioral_mode in _['behavioral_mode_list']:

        for i in rlen(pts2D_multi_step):

            Prediction2D_plot['pts_plot'](na(pts2D_multi_step[i][behavioral_mode]),Colors[behavioral_mode],add_mode=_['add_mode'])

    #img = get_SOURCE_DEPENDENT_img(source,_)
    img = S['left_image']

    left_camera_3D_img,metadata_3D_img = get_prediction_images_3D(pts2D_multi_step,img,_)

    return Prediction2D_plot,left_camera_3D_img,metadata_3D_img
###
################################################################
################################################################
###
def show_maybe_save_images(Prediction2D_plot,left_camera_3D_img,metadata_3D_img,_):

    if _['save metadata']:
        metadata_img_list[left_index] = metadata_3D_img

    if _['show timer'].check():
        _['show timer'] = Timer(_['show timer time'])
        #Prediction2D_plot['show'](scale=_['Prediction2D_plot scale'])
        img = Prediction2D_plot['image']
        img = z55(np.log10(1.0*img+1.0)*10.0)
        img = cv2.resize(img, (0,0), fx=4, fy=4, interpolation=0)
        img[4*41+1,:,:] = 128
        img[:,4*31+1,:] = 128
        mci(img,title='X',scale=1)
        mci(left_camera_3D_img,title='left_camera_3D_img',delay=_['cv2 delay'],scale=_['3d image scale'])
        mci(metadata_3D_img,title='metadata_3D_img',delay=_['cv2 delay'],scale=_['metadata_3D_img scale'])
###
################################################################
################################################################
################################################################
###




################################################################
################################################################
###
def get_SOURCE_DEPENDENT_data(source,_):

    headings,encoders,motors = {},{},{}

    if source == 'preprocessed':

        indx = _['index']

        d_heading = _['headings'][indx]-_['headings'][indx-1]

        gyro_heading_x = _['headings'][indx]

        encoder = _['encoders'][indx]

        #sample_frequency = 1.0 / (L['left_timestamp_index'][_['index']]-L['left_timestamp_index'][_['index']-1])

        sample_frequency = 30.0
        S['sample_frequency'] = sample_frequency #temp

        for behavioral_mode in _['behavioral_mode_list']:

            headings[behavioral_mode] = _['U_heading_gain'] * U[behavioral_mode][_['index']]['heading']

            encoders[behavioral_mode] = U[behavioral_mode][_['index']]['encoder']

            motors[behavioral_mode] = L['motor'][_['index']:_['index']+len(headings[behavioral_mode])]

    elif source == 'ROS':

        headings['left'] =      S['headings_left']
        headings['direct'] =    S['headings_direct']
        headings['right'] =     S['headings_right']
        encoders['left'] =      S['encoders_left']
        encoders['direct'] =    S['encoders_direct']
        encoders['right'] =     S['encoders_right']
        motors['left'] =        S['motors_left']
        motors['direct'] =      S['motors_direct']
        motors['right'] =       S['motors_right']
        d_heading =             S['d_heading']
        gyro_heading_x =        S['gyro_heading_x']
        encoder =               S['encoder']
        sample_frequency =      S['sample_frequency']

    else:

        assert False

    return d_heading,gyro_heading_x,encoder,sample_frequency,headings,encoders,motors
###
################################################################
################################################################
###
def get_SOURCE_DEPENDENT_img(source,_):
    left_index = Left_timestamps_to_left_indicies[(1000.0*(U['ts'][_['index']] - t0)).astype(int)]
    img = O['left_image']['vals'][left_index].copy()
    return img
###
################################################################
################################################################






if __name__ == '__main__':
    

    Prediction2D_plot = CV2Plot(height_in_pixels=141,width_in_pixels=62,pixels_per_unit=7,y_origin_in_pixels=41)

    Prediction2D_plot['verbose'] = False

    #

    pts2D_multi_step = []

    while _['index'] < len(U['ts']) and not _['ABORT']:
        try:
            load_parameters(_)

            Data = {}

            if True:
                d_heading,gyro_heading_x,encoder,sample_frequency,Data['headings'],Data['encoders'],Data['motors'] = get_SOURCE_DEPENDENT_data('preprocessed',_)

                for modality in ['headings','encoders','motors']:
                    for behavioral_mode in _['behavioral_mode_list']:
                        Pub[modality][behavioral_mode].publish(data=1000*Data[modality][behavioral_mode])
                Pub['gyro_heading'].publish(geometry_msgs.msg.Vector3(*[gyro_heading_x,0,0]))
                Pub['encoder'].publish(data=encoder)

                #time.sleep(0.1)
            

            if True:
                if True:#try:
                    #print S
                    Prediction2D_plot,left_camera_3D_img,metadata_3D_img = \
                        prepare_2D_and_3D_images(Prediction2D_plot,pts2D_multi_step,'ROS',_)

                    show_maybe_save_images(Prediction2D_plot,left_camera_3D_img,metadata_3D_img,_)  

        except Exception as e:
            cr('*** index',_['index'],'failed ***')
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)  
                #
                ##########################################################
        
        if False:
            _['index'] += _['step_size']
            _['timer'].freq(d2s("_['index'] =",_['index'], int(100*_['index']/(1.0*len(U['ts']))),'%',"S['sample_frequency'] =",dp(S['sample_frequency'],1),"S['d_heading'] =",dp(S['d_heading'])))

        

    if _['save metadata']:
        file_path = opj(_['dst path'],fname(run_path)+'.net_projections.h5py')
        os.system(d2s('mkdir -p',pname(file_path)))
        cb("F = h5w(",file_path,")")
        metadata_img_list_FLIP = []
        for img in metadata_img_list:
            metadata_img_list_FLIP.append(cv2.flip(img,1))
        F = h5w(file_path)
        Data = {'normal':na(metadata_img_list,np.uint8),'flip':na(metadata_img_list_FLIP,np.uint8),}
        for d in Data:
            cb("F.create_dataset(",d,",data=Data[",d,"])")
            F.create_dataset(d,data=Data[d])
        F.close()
        cb("F.close()")

###
##############################################################
##############################################################
##############################################################

cg('\n\nDone.\n')

#EOF
