##############################################################
####################### IMPORT no ros ################################
## python kzpy3/VT_net2__5April2019/main.py run tegra-ubuntu_29Oct18_13h28m05s
############
from kzpy3.vis3 import *
import default_values
import fit3d#_torch as fit3d

exec(identify_file_str)
_ = default_values._

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
U = lo(opjD('Data','tegra-ubuntu_31Oct18_16h06m32s.net_predictions.pkl'))


if False:
    L,O,___ = open_run(run_name=Arguments['run'],h5py_path=pname(run_path),want_list=['L','O'])
L,O,___ = open_run(run_name='tegra-ubuntu_31Oct18_16h06m32s',h5py_path=pname(opjD()),want_list=['L','O'])
_['headings'] = L['gyro_heading_x'][:]
_['encoders'] = L['encoder'][:]

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
def get_data(_):

    headings,encoders,motors = {},{},{}

    indx = _['index']

    d_heading = _['headings'][indx]-_['headings'][indx-1]

    gyro_heading_x = _['headings'][indx]

    encoder = _['encoders'][indx]

    if False:#_['index'] > 0:
        sample_frequency = 1.0 / (L['left_timestamp_index'][_['index']]-L['left_timestamp_index'][_['index']-1])
    else:
        sample_frequency = 30.0
        #cr('sample_frequency = 30.0')

    for behavioral_mode in _['behavioral_mode_list']:

        headings[behavioral_mode] = _['U_heading_gain'] * U[behavioral_mode][_['index']]['heading']

        encoders[behavioral_mode] = U[behavioral_mode][_['index']]['encoder']

        motors[behavioral_mode] = L['motor'][_['index']:_['index']+len(headings[behavioral_mode])]

    left_index = Left_timestamps_to_left_indicies[(1000.0*(U['ts'][_['index']] - t0)).astype(int)]

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

rate_timer = Timer(1/30.)

def step():
    
    #try:
    asssert( _['index'] < len(U['ts']) and not _['ABORT'] )

    if rate_timer.check():
        rate_timer.reset()
        Data = {}

        d_heading,sample_frequency,left_image,right_image,gyro_heading_x,encoder,Data['headings'],Data['encoders'],Data['motors'] = get_data(_)

        if Arguments['pub_predictions']:
            for modality in ['headings','encoders','motors']:
                for behavioral_mode in _['behavioral_mode_list']:
                    MODALITY_SIDE_callback( 1000*Data[modality][behavioral_mode], modality, behavioral_mode )

        gyro_heading_x_callback( gyro_heading_x )

        encoder_callback( encoder )

        #Pub['human_agent'].publish(data=0)
        #Pub['behavioral_mode'].publish(data='direct')
        #Pub['drive_mode'].publish(data=1)

        left_callback( left_image )

        if Arguments['step']:
            cg("_['index'] =",_['index'],ra=1)
        _['index'] += _['step_size']
        _['timer'].freq(d2s("_['index'] =",_['index'], int(100*_['index']/(1.0*len(U['ts']))),'%'))
        #,"S['sample_frequency'] =",dp(S['sample_frequency'],1),"S['d_heading'] =",dp(S['d_heading'])))

    time.sleep(2/1000.)

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

cg('\n\nDone.\n')

#EOF

#EOF
