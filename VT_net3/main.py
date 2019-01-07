
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

Img = CV2Plot(300,300,50,150,250)
hz = Timer(10)







use_GPU = False
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



bdd2+GPU
 frequency = 64.49 Hz
 frequency = 88.94 Hz
 frequency = 88.12 Hz
 frequency = 88.98 Hz

TX1+GPU
11.5 Hz
"""

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


    if len(xys) > 4600:
        xys = xys[-4400:,:]
    """
    if len(xys) > 910:
        xys = xys[-900:,:]
    """
    if False:#np.mod(100,i)==0:
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



















#EOF
