##############################################################
####################### IMPORT ################################
## python kzpy3/VT_net2__5April2019/main.py run tegra-ubuntu_29Oct18_13h28m05s
############
from kzpy3.vis3 import *
import default_values
import fit3d#_torch as fit3d
import std_msgs.msg
import geometry_msgs.msg
from std_msgs.msg import Int32MultiArray
from sensor_msgs.msg import Image
import cv_bridge
#bridge = cv_bridge.CvBridge()
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
bcs = '/bair_car/'
Pub = {}
extra = ''
if Arguments['pub_predictions'] == 9:
    extra = '_'
for modality in ['headings','encoders','motors']:
    Pub[modality] = {}
    for behavioral_mode in _['behavioral_mode_list']:
        Pub[modality][behavioral_mode] = rospy.Publisher(modality+'_'+behavioral_mode+extra,Int32MultiArray,queue_size = 1)
Pub['gyro_heading'] = rospy.Publisher(bcs+'gyro_heading', geometry_msgs.msg.Vector3, queue_size=1)
Pub['encoder'] = rospy.Publisher(bcs+'encoder',std_msgs.msg.Float32,queue_size=1)
Pub['human_agent'] = rospy.Publisher(bcs+'human_agent',std_msgs.msg.Int32,queue_size=1)
Pub['behavioral_mode'] = rospy.Publisher(bcs+'behavioral_mode',std_msgs.msg.String,queue_size=1)
Pub['drive_mode'] = rospy.Publisher(bcs+'drive_mode',std_msgs.msg.Int32,queue_size=1)
Pub['left_image'] = rospy.Publisher("/bair_car/zed/left/image_rect_color",Image,queue_size=1)
Pub['right_image'] = rospy.Publisher("/bair_car/zed/right/image_rect_color",Image,queue_size=1)

rospy.init_node('publish_node',anonymous=True,disable_signals=True)
##
##############################################################
##############################################################


##############################################################
##############################################################
##

runs = lo(opjD('Data/Network_Predictions/runs.pkl'))
Runs = {}

for r in runs:
    Runs[fname(r)] = r
run_path = Runs[Arguments['run']]
run_path = run_path.replace('/media/karlzipser','/home/karlzipser/Desktop/Data')
cm(0)
U = lo(opjD('Data/Network_Predictions',fname(run_path)+'.net_predictions.pkl'))

L,O,___ = open_run(run_name=Arguments['run'],h5py_path=pname(run_path),want_list=['L','O'])
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

if __name__ == '__main__':
    
    try:
        while _['index'] < len(U['ts']) and not _['ABORT']:

            if rate_timer.check():
                rate_timer.reset()
                Data = {}

                d_heading,sample_frequency,left_image,right_image,gyro_heading_x,encoder,Data['headings'],Data['encoders'],Data['motors'] = get_data(_)

                if Arguments['pub_predictions']:
                    for modality in ['headings','encoders','motors']:
                        for behavioral_mode in _['behavioral_mode_list']:
                            Pub[modality][behavioral_mode].publish(data=1000*Data[modality][behavioral_mode])

                Pub['gyro_heading'].publish(geometry_msgs.msg.Vector3(*[gyro_heading_x,0,0]))

                Pub['encoder'].publish(data=encoder)

                Pub['human_agent'].publish(data=0)
                Pub['behavioral_mode'].publish(data='direct')
                Pub['drive_mode'].publish(data=1)


                Pub['left_image'].publish(cv_bridge.CvBridge().cv2_to_imgmsg(left_image,'rgb8'))

                Pub['right_image'].publish(cv_bridge.CvBridge().cv2_to_imgmsg(right_image,'rgb8'))
                
                if Arguments['step']:
                    cg("_['index'] =",_['index'],ra=1)
                _['index'] += _['step_size']
                _['timer'].freq(d2s("_['index'] =",_['index'], int(100*_['index']/(1.0*len(U['ts']))),'%'))
                #,"S['sample_frequency'] =",dp(S['sample_frequency'],1),"S['d_heading'] =",dp(S['d_heading'])))

                

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

            else:
                time.sleep(2/1000.)

    except KeyboardInterrupt:
        cr('\n\n*** KeyboardInterrupt ***\n')
        sys.exit()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        CS_('Exception!',emphasis=True)
        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno,'\t',time.time()),emphasis=False)
        time.sleep(1)

###
##############################################################
##############################################################
##############################################################

cg('\n\nDone.\n')

#EOF

#EOF
