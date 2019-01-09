
from kzpy3.vis3 import *
import kzpy3.VT_net3.default_values as default_values
import fit3d
import rospy
import std_msgs.msg
import geometry_msgs.msg
import torch
torch.set_default_tensor_type('torch.FloatTensor') 
torch.cuda.set_device(0)
torch.cuda.device(0)
P = default_values.P

########################################################################################
########################################################################################
########################################################################################
####
NET = {}
NET['ts'] = time.time()
NET['headings'] = {}
NET['headings'][0] = zeros(10)
NET['headings'][1] = zeros(10)
NET['headings'][2] = zeros(10)
NET['encoders'] = {}
NET['encoders'][0] = zeros(10)
NET['encoders'][1] = zeros(10)
NET['encoders'][2] = zeros(10)
NET['motor'] = {}
NET['motor'][0] = zeros(10)
NET['motor'][1] = zeros(10)
NET['motor'][2] = zeros(10)
NET['gyro_heading_x'] = 0
CAR = {}
CAR['motor'] = 0
CAR['gyro_heading_x'] = 0
CAR['encoder'] = 0
def header0_callback(data):
    NET['headings'][0] = na(data.data).astype(float)/1000.
rospy.Subscriber('/header0', std_msgs.msg.Int32MultiArray, callback=header0_callback)
def header1_callback(data):
    NET['headings'][1] = na(data.data).astype(float)/1000.
rospy.Subscriber('/header1', std_msgs.msg.Int32MultiArray, callback=header1_callback)
def header2_callback(data):
    NET['headings'][2] = na(data.data).astype(float)/1000.
rospy.Subscriber('/header2', std_msgs.msg.Int32MultiArray, callback=header2_callback)
def encoder0_callback(data):
    NET['encoders'][0] = na(data.data).astype(float)/1000.
rospy.Subscriber('/encoder0', std_msgs.msg.Int32MultiArray, callback=encoder0_callback)
def encoder1_callback(data):
    NET['encoders'][1] = na(data.data).astype(float)/1000.
rospy.Subscriber('/encoder1', std_msgs.msg.Int32MultiArray, callback=encoder1_callback)
def encoder2_callback(data):
    NET['encoders'][2] = na(data.data).astype(float)/1000.
rospy.Subscriber('/encoder2', std_msgs.msg.Int32MultiArray, callback=encoder2_callback)

def motor0_callback(data):
    NET['motor'][0] = na(data.data)
rospy.Subscriber('/motor0', std_msgs.msg.Int32MultiArray, callback=motor0_callback)
def motor1_callback(data):
    NET['motor'][1] = na(data.data)
rospy.Subscriber('/motor1', std_msgs.msg.Int32MultiArray, callback=motor1_callback)
def motor2_callback(data):
    NET['motor'][2] = na(data.data)
    NET['ts_prev'] = NET['ts']
    NET['ts'] = time.time()
    NET['sample_frequency'] = 1.0 / (NET['ts']-NET['ts_prev'])
    NET['gyro_heading_x_prev'] = NET['gyro_heading_x']
    NET['gyro_heading_x'] = CAR['gyro_heading_x']
    NET['d_heading'] = NET['gyro_heading_x'] - NET['gyro_heading_x_prev']
    NET['velocity'] = CAR['encoder'] * P['vel-encoding coeficient']
    NET['trajectory_vector_magnitude'] = NET['velocity'] / NET['sample_frequency']
rospy.Subscriber('/motor2', std_msgs.msg.Int32MultiArray, callback=motor2_callback)

def gyro_heading_x_callback(data):
    CAR['gyro_heading_x'] = data.x
rospy.Subscriber('/bair_car/gyro_heading', geometry_msgs.msg.Vector3, callback=gyro_heading_x_callback)
def encoder_callback(data):
    CAR['encoder'] = data.data
rospy.Subscriber('/bair_car/encoder', std_msgs.msg.Float32, callback=encoder_callback)
def motor_callback(data):
    CAR['motor'] = data.data
rospy.Subscriber('/bair_car/motor', std_msgs.msg.Int32, callback=motor_callback)
rospy.init_node('VT_node',anonymous=True,disable_signals=True)
####
########################################################################################
########################################################################################
########################################################################################


########################################################################################
########################################################################################
########################################################################################
####
def vec(heading,encoder,motor,sample_frequency):
    velocity = encoder * P['vel-encoding coeficient']
    if motor < 49:
        velocity *= -1.0
    a = [0,1]
    a = array(rotatePoint([0,0],a,heading))
    a *= velocity/sample_frequency
    return a

def get_latest_network_2D_trajectory_predictions(headings,encoders,motors,direction_code):
    assert len(headings) == len(encoders)
    assert len(headings) == len(motors) # this means motor predictions
    n = zeros((1+len(headings),4))
    for i in range(0,len(headings)):
        n[i+1,:2] = n[i,:2] + vec(headings[i],encoders[i],motors[i],P['net sample frequency'])
        n[i+1,-2:] = (NET['ts'],direction_code)
    new_xys = n
    return new_xys
####
########################################################################################
########################################################################################
########################################################################################

xys = zeros([2,4])
Direction_codes = {'left':0,'direct':1,'right':2}
Direction_colors = {0:[255,0,0],1:[0,0,255],2:[0,255,0]}
Img = CV2Plot(
        height_in_pixels=300,
        width_in_pixels=300,
        pixels_per_unit=40,
        x_origin_in_pixels=150,
        y_origin_in_pixels=300)
use_GPU = False
timer = Timer(30)

img1 = zeros((23,41,3))#,np.uint8)
rmax = 7
RGBs = {'direct':(0,0,255),'right':(0,255,0),'left':(255,0,0)}

while True:#not timer.check():

    for direction in ['left','right','direct']:
        i = Direction_codes[direction]

        d_heading = NET['d_heading']

        trajectory_vector_magnitude = NET['trajectory_vector_magnitude']
        if use_GPU:
            xys[:,:2] = rotatePolygon_cuda(xys[:,:2],-d_heading)
        else:
            xys[:,:2] = rotatePolygon(xys[:,:2],-d_heading) # rotate existing points away from heading
        xys = na(xys)
        xys[:,1] -= trajectory_vector_magnitude # move points down so origin is new starting point
        new_xys = get_latest_network_2D_trajectory_predictions(
                        NET['headings'][i],
                        NET['encoders'][i],
                        NET['motor'][i],
                        Direction_codes[direction])
        xys = np.concatenate((xys,new_xys),0)  # concatenate these to other points

    if len(xys) > P['num timesteps']*3:
        xys = xys[-P['num timesteps']*3:,:]

    Img['clear']()
    Img['pts_plot'](xys[:,:2]) 
    for xy in xys:
        Img['plot point (xy_version)'](xy[0],xy[1],Direction_colors[xy[3]])
    Img['show'](title='2d points',scale=2.0,delay=33)

    img1 *= 0
    for a in xys:

        if a[1]<0:
            continue
        try:
            r = int(5.0/np.sqrt(a[0]**2+(a[1])**2))
        except:
            r = 1

        b = fit3d.Point3(a[0], 0, a[1]-P['backup parameter'])
        c = fit3d.project(b, fit3d.mat)

        try:
            good = True
            if c.x < 0 or c.x >= 168:
                good = False
            elif c.y < 0 or c.y >= 94:
                good = False
            if good:             
                if r < rmax:
                    pass#cv2.circle(img,(int(c.x),int(c.y)),r,RGBs[behavioral_mode])
            good = True
            cx = intr(c.x * 0.245)
            cy = intr(c.y * 0.245)
            if cx < 0 or cx >= 41:
                good = False
            elif cy < 0 or cy >= 23:
                good = False
            if good:               
                #img1[cy,cx,:] = Direction_colors[a[3]]
                print cy,cx,a[3]
                img1[cy,cx,int(a[3])] += 1
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
    for y in range(11,23):
        for c in range(3):
            if img1[y,:,c].max() > 0:
                img1[y,:,c] = z2o(img1[y,:,c])
    mi(img1);spause()
    #img1 = (255*img1).astype(np.uint8)
    #mci(img1,scale=4.0)





#EOF
