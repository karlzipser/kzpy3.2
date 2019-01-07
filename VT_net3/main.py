from kzpy3.vis3 import *
#import VT_net3.default_values as default_values
import default_values
P = default_values.P

sample_frequency = 30.0

U=lo('/home/karlzipser/Desktop/Data/Network_Predictions/Mr_Black_27Jul18_18h46m35s.net_predictions.pkl') 
runs = lo(opjD('Data/Network_Predictions/runs.pkl'))                                            
Runs = {}                  
for r in runs:        
    Runs[fname(r)] = r
L,__,___=open_run(U['run_name'],Runs_dic=Runs)   

NET = {}
NET['ts'] = 0
CAR = {}
CAR['encoder'] = 0
CAR['gyro_heading_x'] = 0
CAR['sample_frequency'] = 30.

def callback(i,direction):
    NET['ts previous'] = NET['ts']
    NET['ts'] =         U['ts'][i]
    CAR['sample_frequency'] = 1.0/(NET['ts']-NET['ts previous'])
    cb(CAR['sample_frequency'])
    assert(NET['ts previous'] < NET['ts'])
    NET['headings'] =   U[direction][i]['heading']
    NET['encoders'] =   U[direction][i]['encoder']
    NET['motors'] =     U[direction][i]['motor']
    CAR['encoder_prev'] = CAR['encoder']
    CAR['encoder'] =        L['encoder'][i]
    CAR['gyro_heading_x_prev'] = CAR['gyro_heading_x']
    CAR['gyro_heading_x'] = L['gyro_heading_x'][i]

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

def get_latest_network_2D_trajectory_predictions(headings,encoders,motors):
    assert len(headings) == len(encoders)
    assert len(headings) == len(motors) # this means motor predictions
    xys = zeros((1+len(headings),2))
    for i in range(0,len(headings)):
        xys[i+1,:] = xys[i,:] + vec(headings[i],encoders[i],motors[i],P['net sample frequency'])
    return xys
#
#############################################################################

xys = zeros([2,2])

for i in range(8000,20000):

    if np.mod(i,1):
        print i
        continue
    callback(i,'right')


    d_heading = CAR['gyro_heading_x'] - CAR['gyro_heading_x_prev']

    velocity = CAR['encoder'] * P['vel-encoding coeficient']
    trajectory_vector_magnitude = velocity / CAR['sample_frequency']
    xys = rotatePolygon(xys,-d_heading) # rotate existing points away from heading
    xys = na(xys)
    xys[:,1] -= trajectory_vector_magnitude # move points down so origin is new starting point

    new_xys = get_latest_network_2D_trajectory_predictions(NET['headings'],NET['encoders'],NET['motors'])

    xys = np.concatenate((xys,new_xys),0)  # concatenate these to other points

    if len(xys) > 930:
        xys = xys[-900:,:]
    
    clf()
    pts_plot(xys)
    pts_plot(new_xys,color='k')
    plt_square()
    xylim(-4,4,-8,7)
    spause()
    


#
##########################################################



















#EOF
