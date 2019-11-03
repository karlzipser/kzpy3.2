#######################################################
## python kzpy3/scripts/ros/publish_preprocessed_data.py --step 0
############
from kzpy3.vis3 import *
import std_msgs.msg
import geometry_msgs.msg
from std_msgs.msg import Int32MultiArray
from sensor_msgs.msg import Image
import cv_bridge
exec(identify_file_str)


"""

roscore
python kzpy3/scripts/ros/publish_preprocessed_data.py  --pub_predictions 1 --step 0
python kzpy3/scripts/ros/publish_preprocessed_data.py  --pub_predictions 9 --step 0
python kzpy3/scripts/ros/publish_preprocessed_data.py  --pub_predictions 1 --step 0 --initial_index 10000
python kzpy3/VT_net2__5April2019_2__18April2019_for_speed/main.py
python kzpy3/VT_net2__5April2019_2__18April2019_for_speed/main.py # _['topic_suffix'] = '_'
python kzpy3/scripts/ros/plot_topics.py topics headings_left_,headings_right_,headings_direct_ colors red,green,blue falloff 0.7
python kzpy3/scripts/ros/plot_topics.py topics headings_left,headings_right,headings_direct colors red,green,blue falloff 0.7
python kzpy3/Menu_app/menu2.py path kzpy3/Cars/a2Apr19/nodes dic P
python kzpy3/Cars/a2Apr19/nodes/network_node.py desktop_mode 1
rosplay_menu.py

"""


Defaults = {
    'pub_predictions':1,
    'step':False,
    'run_name':'tegra-ubuntu_29Oct18_13h28m05s',
    'run_path':opjD('Data/1_TB_Samsung_n1/left_direct_stop__29to30Oct2018/locations/local/left_direct_stop/h5py'),
    'initial_index':0,
}
setup_Default_Arguments(Defaults)


_ = {}
_['ABORT'] = False
_['save metadata'] = False
_['step_size'] = 1
_['3d image scale'] = 1.0
_['U_heading_gain'] = 2.0
_['index'] = Arguments['initial_index']
_['cmd_camera_to_camera_heading_cooeficient'] = 0.75
_['dst path'] = opjD('Data/Network_Predictions_projected_gain_2')
_['behavioral_mode_list'] = ['left','direct','right']
_['timer'] = Timer(5)
_['Depth_data'] = None

runs_with_Depth_images = fnamenes(sggo(opjD('Data','Depth_images','*')))

    
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
Pub['depth_image'] = rospy.Publisher("/os1_node/image",Image,queue_size=1)

rospy.init_node('publish_node',anonymous=True,disable_signals=True)
##
##############################################################
##############################################################


##############################################################
##############################################################
##
cm(0,5)
U = lo(opjD('Data/Network_Predictions',Arguments['run_name']+'.net_predictions.pkl'))
cm(1,5)
L,O,___ = open_run(run_name=Arguments['run_name'],h5py_path=Arguments['run_path'],want_list=['L','O'])
cm(2,5)
_['headings'] = L['gyro_heading_x'][:]
_['encoders'] = L['encoder'][:]
cm(3,5)
#CA();plot(_['encoders'],_['headings'],'.');spause()

Left_timestamps_to_left_indicies = {}
t0 = L['ts'][0]
cm(4,5)
blank_meta = np.zeros((23,41,3),np.uint8)
for i in rlen(L['ts']):
    t = (1000.0*(L['ts'][i] - t0)).astype(int)
    Left_timestamps_to_left_indicies[t] = i
if Arguments['run_name'] in runs_with_Depth_images:
    _['Depth_data'] = h5r(opjD('Data','Depth_images',Arguments['run_name']+'.Depth_image.with_left_ts.rgb_v1.h5py'))
cm(5,5)
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
    try:
        for behavioral_mode in _['behavioral_mode_list']:
            
            #print(len(headings))
            #print(_['U_heading_gain'])
            #print(len(U[behavioral_mode]))
            #print(U[behavioral_mode][_['index']])
            #print(U[behavioral_mode][_['index']].keys())
            
            headings[behavioral_mode] = _['U_heading_gain'] * U[behavioral_mode][_['index']]['heading']

            encoders[behavioral_mode] = U[behavioral_mode][_['index']]['encoder']

            motors[behavioral_mode] = L['motor'][_['index']:_['index']+len(headings[behavioral_mode])]

        left_index = Left_timestamps_to_left_indicies[(1000.0*(U['ts'][_['index']] - t0)).astype(int)]

        left_image = O['left_image']['vals'][left_index].copy()
        right_image = O['right_image']['vals'][left_index].copy()

        depth_image = None
        if _['Depth_data'] != None:
            depth_index = _['Depth_data']['left_to_lidar_index'][indx]
            depth_image = _['Depth_data']['rgb_v1_normal'][depth_index]
            #clp(indx,depth_index)
            #mci(depth_image)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        CS_('Exception!',emphasis=True)
        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)            
        return None,None,None,None,None,None,None,None,None,None
    return d_heading,sample_frequency,left_image,right_image,gyro_heading_x,encoder,headings,encoders,motors,depth_image
##
##############################################################
##############################################################



##############################################################
##############################################################
##############################################################
###

rate_timer = Timer(1/30.)

if __name__ == '__main__':
    
    
    while _['index'] < len(U['ts']) and not _['ABORT']:
        if True:#try:
            
            
            if rate_timer.check():
                rate_timer.reset()
                clp(_['index'],'`g-r',len(U['ts']),_['ABORT'],'`by')
                Data = {}

                d_heading,sample_frequency,left_image,right_image,gyro_heading_x,encoder,Data['headings'],Data['encoders'],Data['motors'],depth_image = get_data(_)

                if d_heading == None:
                    _['index'] += _['step_size']
                    continue
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

                Pub['depth_image'].publish(cv_bridge.CvBridge().cv2_to_imgmsg(depth_image,'rgb8'))
                
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
    
        #except KeyboardInterrupt:
        #    cr('\n\n*** KeyboardInterrupt ***\n')
        #    sys.exit()
        else:#except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno,'\t',time.time()),emphasis=False)
            _['index'] += _['step_size']
            time.sleep(.1)
    
try_to_close([O,L,U,_['Depth_data']])
###
##############################################################
##############################################################
##############################################################

cg('\n\nDone.\n')

#EOF

#EOF
