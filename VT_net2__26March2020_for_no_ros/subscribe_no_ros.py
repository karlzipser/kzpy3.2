##############################################################
########################    SUBSCRIBE no ros #######################
###
from kzpy3.vis3 import *
import default_values
#import publish_no_ros

S = {}
S['ts'] = 0
S['ts_prev'] = 0
S['sample_frequency'] = 0
S['gyro_heading_x'] = 0
S['gyro_heading_x_prev'] = 0
S['d_heading'] = 0
S['encoder'] = 0
S['left_image'] = False
S['delta cmd/camera'] = 0
S['cmd/camera'] = 49

def MODALITY_SIDE_callback(data,modality,side):
    S[modality+'_'+side] = na(data).astype(float)/1000.

def encoder_callback(data):
    S['encoder'] = data


def gyro_heading_x_callback(data):
    S['gyro_heading_x_prev'] = S['gyro_heading_x']
    S['gyro_heading_x'] = data
    S['d_heading'] = 2*(S['gyro_heading_x']-S['gyro_heading_x_prev'])
    S['ts_prev'] = S['ts']
    S['ts'] = time.time()
    S['sample_frequency'] = 30.
    #S['sample_frequency'] = 1.0 / (S['ts']-S['ts_prev'])



def cmd_camera_callback(msg):
    S['delta cmd/camera'] = msg - S['cmd/camera']
    S['cmd/camera'] = msg



def left_callback(data):
    S['left_image'] = data


###
#####################################################
#####################################################



##############################################################
####################### IMPORT no ros ################################
## python kzpy3/VT_net2__5April2019/main.py run tegra-ubuntu_29Oct18_13h28m05s
############
from kzpy3.vis3 import *
import default_values
import fit3d

exec(identify_file_str)
P = default_values.P

Defaults = {
    'pub_predictions':True,
    'step':False,
    'run':'tegra-ubuntu_29Oct18_13h28m05s',
}
for k in Defaults:
    if k not in Arguments:
        Arguments[k] = Defaults[k]


##############################################################
##############################################################
##

if False:
    runs = lo(opjD('Data/Network_Predictions/runs.pkl'))
    Runs = {}

    for r in runs:
        Runs[fname(r)] = r
    run_path = Runs[Arguments['run']]
    run_path = run_path.replace('/media/karlzipser','/home/karlzipser/Desktop/Data')



if False:
    U = lo(opjD('Data/Network_Predictions',fname(run_path)+'.net_predictions.pkl'))
U = lo(opjD('tegra-ubuntu_31Oct18_16h06m32s.net_predictions.pkl'))
for i in rlen(U['left']):
    if U['left'][i] is not None and len(U['left'][i]) > 0:
        break
    else:
        P['index'] += 1
clp('first valid index =',P['index'],'; initial index=',P['initial index'])

if False:
    L,O,___ = open_run(run_name=Arguments['run'],h5py_path=pname(run_path),want_list=['L','O'])
L,O,___ = open_run(run_name='tegra-ubuntu_31Oct18_16h06m32s',h5py_path=pname(opjD()),want_list=['L','O'])
P['headings'] = L['gyro_heading_x'][:]
P['encoders'] = L['encoder'][:]

Left_timestamps_to_left_indicies = {}
t0 = L['ts'][0]

blank_meta = np.zeros((23,41,3),np.uint8)
for i in rlen(L['ts']):
    t = (1000.0*(L['ts'][i] - t0)).astype(int)
    Left_timestamps_to_left_indicies[t] = i

##
##############################################################
##############################################################


##############################################################
##############################################################
##
def get_data(P):

    headings,encoders,motors = {},{},{}

    indx = P['index']

    d_heading = P['headings'][indx]-P['headings'][indx-1]

    gyro_heading_x = P['headings'][indx]

    encoder = P['encoders'][indx]

    if False:#P['index'] > 0:
        sample_frequency = 1.0 / (L['left_timestamp_index'][P['index']]-L['left_timestamp_index'][P['index']-1])
    else:
        sample_frequency = 30.0

    for behavioral_mode in P['behavioral_mode_list']:

        headings[behavioral_mode] = P['U_heading_gain'] * U[behavioral_mode][P['index']]['heading']

        encoders[behavioral_mode] = U[behavioral_mode][P['index']]['encoder']

        motors[behavioral_mode] = L['motor'][P['index']:P['index']+len(headings[behavioral_mode])]

    left_index = Left_timestamps_to_left_indicies[(1000.0*(U['ts'][P['index']] - t0)).astype(int)]

    left_image = O['left_image']['vals'][left_index].copy()
    right_image = O['right_image']['vals'][left_index].copy()

    return d_heading,sample_frequency,left_image,right_image,gyro_heading_x,encoder,headings,encoders,motors
##
##############################################################
##############################################################



##############################################################
##############################################################
##############################################################
###

#rate_timer = Timer(1/30.)

def step(index=-1):
    
    if index > 0:
        P['index'] = index

    if True:#try:
        assert( P['index'] < len(U['ts']) and not P['ABORT'] )

        #if rate_timer.check():
        #    rate_timer.reset()
        Data = {}

        d_heading,sample_frequency,left_image,right_image,gyro_heading_x,encoder,Data['headings'],Data['encoders'],Data['motors'] = get_data(P)

        if Arguments['pub_predictions']:
            for modality in ['headings','encoders','motors']:
                for behavioral_mode in P['behavioral_mode_list']:
                    MODALITY_SIDE_callback( 1000*Data[modality][behavioral_mode], modality, behavioral_mode )

        gyro_heading_x_callback( gyro_heading_x )

        encoder_callback( encoder )

        left_callback( left_image )

        if Arguments['step']:
            cg("P['index'] =",P['index'],ra=1)
        P['index'] += P['step_size']
        P['timer'].freq(d2s("P['index'] =",P['index'], int(100*P['index']/(1.0*len(U['ts']))),'%'))


    """
    except KeyboardInterrupt:
        cr('\n\n*** KeyboardInterrupt ***\n')
        sys.exit()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        CS_('Exception!',emphasis=True)
        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno,'\t',time.time()),emphasis=False)
        time.sleep(1)
    """
    

###
##############################################################
##############################################################
##############################################################


#EOF

