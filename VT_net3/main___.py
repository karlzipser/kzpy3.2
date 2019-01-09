
from kzpy3.vis3 import *
import kzpy3.VT_net3.default_values as default_values
import torch
torch.set_default_tensor_type('torch.FloatTensor') 
torch.cuda.set_device(0)
torch.cuda.device(0)
P = default_values.P
NET = {}
NET['ts'] = 0
CAR = {}
CAR['encoder'] = 0
CAR['gyro_heading_x'] = 0
CAR['sample_frequency'] = 30.

if not P['USE_ROS']:
##############################################################
#
    if username != 'nvidia':

        U=lo(opjD('Data/Network_Predictions/Mr_Black_27Jul18_18h46m35s.net_predictions.pkl'))
        runs = lo(opjD('Data/Network_Predictions/runs.pkl'))                                            
        Runs = {}                  
        for r in runs:        
            Runs[fname(r)] = r
        L,O,___=open_run(U['run_name'],Runs_dic=Runs)

    else:
        U=lo(opjm('rosbags/Data/Mr_Black_27Jul18_18h46m35s.net_predictions.pkl'))
        runs = lo(opjm('rosbags/Data/Network_Predictions/runs.pkl'))                                            
        Runs = {}                  
        for r in runs:        
            Runs[fname(r)] = r
        #L,O,___=open_run(U['run_name'],h5py_path='/media/karlzipser/rosbags/Data/h5py/Mr_Black_27Jul18_18h46m35s')
        L = h5r(opjm('rosbags/Data/h5py/Mr_Black_27Jul18_18h46m35s/left_timestamp_metadata_right_ts.h5py'))
        O = h5r(opjm('rosbags/Data/h5py/Mr_Black_27Jul18_18h46m35s/original_timestamp_data.h5py'))

    #
    ##############################################################
    def callback1(i):
        NET['ts previous'] = NET['ts']
        NET['ts'] =         U['ts'][i]
        CAR['sample_frequency'] = 1.0/(NET['ts']-NET['ts previous'])
        #cb(CAR['sample_frequency'])
        assert(NET['ts previous'] < NET['ts'])
    def callback2(i,direction):
        NET['headings'] =   U[direction][i]['heading']
        NET['encoders'] =   U[direction][i]['encoder']
        NET['motors'] =     U[direction][i]['motor']
        CAR['encoder_prev'] = CAR['encoder']
        CAR['encoder'] =        L['encoder'][i]
        CAR['gyro_heading_x_prev'] = CAR['gyro_heading_x']
        CAR['gyro_heading_x'] = L['gyro_heading_x'][i]
    t0 = U['ts'][0]
#
###################################################################
#
else:
    import rospy
    import std_msgs.msg
    import geometry_msgs.msg

    NET['headings'] = {}
    NET['headings'][0] = zeros(10)
    NET['headings'][1] = zeros(10)
    NET['headings'][2] = zeros(10)
    NET['encoders'] = {}
    NET['encoders'][0] = zeros(10)
    NET['encoders'][1] = zeros(10)
    NET['encoders'][2] = zeros(10)
    CAR['motor'] = 0


    def header0_callback(data):
        NET['headings'][0] = data.data
    rospy.Subscriber('/header0', std_msgs.msg.Int32MultiArray, callback=header0_callback)
    def header1_callback(data):
        NET['headings'][1] = data.data
    rospy.Subscriber('/header1', std_msgs.msg.Int32MultiArray, callback=header1_callback)
    def header2_callback(data):
        NET['headings'][2] = data.data
    rospy.Subscriber('/header2', std_msgs.msg.Int32MultiArray, callback=header2_callback)

    def encoder0_callback(data):
        NET['encoders'][0] = data.data
    rospy.Subscriber('/encoder0', std_msgs.msg.Int32MultiArray, callback=encoder0_callback)

    def encoder1_callback(data):
        NET['encoders'][1] = data.data
    rospy.Subscriber('/encoder1', std_msgs.msg.Int32MultiArray, callback=encoder1_callback)

    def encoder2_callback(data):
        NET['encoders'][2] = data.data
    rospy.Subscriber('/encoder2', std_msgs.msg.Int32MultiArray, callback=encoder2_callback)

    def gyro_heading_x_callback(data):
        CAR['gyro_heading_x'] = data.x
    rospy.Subscriber('/bair_car/gyro_heading', geometry_msgs.msg.Vector3, callback=gyro_heading_x_callback)

    def encoder_callback(data):
        CAR['encoder'] = data.data
    rospy.Subscriber('/bair_car/encoder', std_msgs.msg.Float32, callback=encoder_callback)

    def motor_callback(data):
        CAR['motor'] = data.data
    rospy.Subscriber('/bair_car/motor', std_msgs.msg.Int32, callback=motor_callback)

    """
        CAR['dt'] = CAR['t'] - CAR['t prev']
        CAR['t prev'] = CAR['t']
        CAR['t'] = time.time()
        CAR['gyro_heading_x'] = CAR['gyro_heading_x'] 
    """

    rospy.init_node('VT_node',anonymous=True,disable_signals=True)

    timer = Timer(300)
    while not timer.check():
        clf();xlim(-0.5,0.5)
        #print P['header1']
        plot(na(NET['encoders'][0]).astype(float)/-1000./90.,range(10),'ro-')
        plot(na(NET['encoders'][1]).astype(float)/-1000./90.,range(10),'bo-')
        plot(na(NET['encoders'][2]).astype(float)/-1000./90.,range(10),'go-')
        print(CAR['motor'],CAR['gyro_heading_x'],CAR['encoder'])
        
        spause()
    raw_enter()
#
##############################################################
#
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
    xys = zeros((1+len(headings),4))
    for i in range(0,len(headings)):
        xys[i+1,:2] = xys[i,:2] + vec(headings[i],encoders[i],motors[i],P['net sample frequency'])
        xys[i+1,-2:] = (NET['ts']-t0,direction_code)
    return xys
#
#############################################################################

xys = zeros([2,4])

Direction_codes = {'left':0,'direct':1,'right':2}
Direction_colors = {0:[255,0,0],1:[0,0,255],2:[0,255,0]}

hz = Timer(10)

Img = CV2Plot(height_in_pixels=300,width_in_pixels=300,pixels_per_unit=40,
    x_origin_in_pixels=150,y_origin_in_pixels=200)

use_GPU = False



for i in range(1000,len(U['ts'])-100):
    
    callback1(i)
    hz.freq(d2s())
    for direction in ['left','right','direct']:

        callback2(i,direction)
        d_heading = CAR['gyro_heading_x'] - CAR['gyro_heading_x_prev']
        velocity = CAR['encoder'] * P['vel-encoding coeficient']
        trajectory_vector_magnitude = velocity / CAR['sample_frequency']
        if use_GPU:
            xys[:,:2] = rotatePolygon_cuda(xys[:,:2],-d_heading)
        else:
            xys[:,:2] = rotatePolygon(xys[:,:2],-d_heading) # rotate existing points away from heading
        xys = na(xys)
        xys[:,1] -= trajectory_vector_magnitude # move points down so origin is new starting point
        new_xys = get_latest_network_2D_trajectory_predictions(
            NET['headings'],NET['encoders'],NET['motors'],Direction_codes[direction])
        xys = np.concatenate((xys,new_xys),0)  # concatenate these to other points

    if len(xys) > 3*310:
        xys = xys[-3*300:,:]
    
    if True:#np.mod(100,i)==0:
        Img['clear']()
        Img['pts_plot'](xys[:,:2]) 
        for xy in xys:
            Img['plot point (xy_version)'](xy[0],xy[1],Direction_colors[xy[3]])
        Img['show'](title='2d points',scale=2.0,delay=33)

        mci(O['left_image']['vals'][i],title='left',scale=4)
        """
        clf()
        pts_plot(xys[:,:2])
        pts_plot(new_xys[:,:2],color='k')
        plt_square()
        xylim(-4,4,-8,7)
        spause()
        """


#
##########################################################





"""

xys = xys[-900:,:]
    use_GPU = True (39 percent speed increase)
        elapsed time =   frequency = 847.87 Hz
        elapsed time =   frequency = 848.46 Hz
        elapsed time =   frequency = 849.55 Hz
        elapsed time =   frequency = 851.6 Hz
        elapsed time =   frequency = 854.11 Hz

    use_GPU = False
        elapsed time =   frequency = 595.96 Hz
        elapsed time =   frequency = 613.3 Hz
        elapsed time =   frequency = 608.2 Hz
        elapsed time =   frequency = 612.81 Hz
        elapsed time =   frequency = 617.6 Hz
        elapsed time =   frequency = 618.58 Hz



xys = xys[-300:,:]

        use_GPU = True (9 percent speed increase)
                        frequency = 1306.09 Hz
                        frequency = 1290.58 Hz
                        frequency = 1313.18 Hz

    use_GPU = False
        elapsed time =   frequency = 1183.09 Hz
        elapsed time =   frequency = 1186.33 Hz
        elapsed time =   frequency = 1195.02 Hz




xys = xys[-10000:,:]
    use_GPU = True (100 percent speed increase)
                         frequency = 181.58 Hz
                         frequency = 138.53 Hz
                         frequency = 145.97 Hz
                         frequency = 145.54 Hz
                         frequency = 145.96 Hz
                         frequency = 145.32 Hz

    use_GPU = False
                         frequency = 116.53 Hz
                         frequency = 72.21 Hz
                         frequency = 71.67 Hz
                         frequency = 72.01 Hz
                         frequency = 71.91 Hz
                         frequency = 71.92 Hz


xys = xys[-4400:,:]
bdd2+GPU
 88 Hz

bdd2
 54 Hz

TX1+GPU
 11.5 Hz

TX1
 9.5 Hz


xys = xys[-300:,:]
bdd2+GPU
  338 Hz

bdd2
  410 Hz

TX1+GPU
  48 Hz

TX1
   91 Hz

"""













#EOF