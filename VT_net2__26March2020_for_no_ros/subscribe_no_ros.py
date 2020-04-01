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
S['steer'] = 49
S['motor'] = 49

def MODALITY_SIDE_callback(data,modality,side):
    S[modality+'_'+side] = na(data).astype(float)/1000.

def encoder_callback(data):
    S['encoder'] = data

def steer_callback(data):
    S['steer'] = data

def motor_callback(data):
    S['motor'] = data


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

assert 'run_name' in Arguments
run_name = Arguments['run_name']

Defaults = {
    'pub_predictions':True,
    'step':False,
    #'run':'tegra-ubuntu_29Oct18_13h28m05s', # 'tegra-ubuntu_31Oct18_16h06m32s'
}
for k in Defaults:
    if k not in Arguments:
        Arguments[k] = Defaults[k]

save_path = opjD('Data','pts2D_multi_step','pkl',run_name+'.pkl')
os.system('mkdir -p '+opj(pname(save_path)))

if len(sggo(save_path)) > 0:
    clp(save_path,'exists!!!','`wrb')
    exit()

os.system(d2s('touch',save_path))
##############################################################
##############################################################
##

U = lo(opjD('Data','Network_Predictions',run_name+'.net_predictions.pkl'))
for i in rlen(U['left']):
    if U['left'][i] is not None and len(U['left'][i]) > 0:
        break
    else:
        P['index'] += 1
clp('first valid index =',P['index'],'; initial index=',P['initial index'])



#h5py_path = find_h5py_path(run_name)

#L,O,___ = open_run(run_name=run_name,h5py_path=h5py_path,want_list=['L','O'],verbose=True)
L,O,___ = open_run2(run_name=run_name,want_list=['L','O'],verbose=True)

P['headings'] = L['gyro_heading_x'][:]
P['encoders'] = L['encoder'][:]
P['steers'] = L['steer'][:]
P['motors'] = L['motor'][:]

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

    steer = P['steers'][indx]
    motor = P['motors'][indx]

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

    return d_heading,sample_frequency,left_image,right_image,gyro_heading_x,encoder,steer,motor,headings,encoders,motors
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

        d_heading,sample_frequency,left_image,right_image,gyro_heading_x,encoder,steer,motor,Data['headings'],Data['encoders'],Data['motors'] = get_data(P)

        if Arguments['pub_predictions']:
            for modality in ['headings','encoders','motors']:
                for behavioral_mode in P['behavioral_mode_list']:
                    MODALITY_SIDE_callback( 1000*Data[modality][behavioral_mode], modality, behavioral_mode )

        gyro_heading_x_callback( gyro_heading_x )

        encoder_callback( encoder )

        steer_callback( steer )

        motor_callback( motor )

        left_callback( left_image )

        if Arguments['step']:
            cg("P['index'] =",P['index'],ra=1)
        S['index'] = P['index']
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

