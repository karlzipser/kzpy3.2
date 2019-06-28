##############################################################
####################### IMPORT ################################
############
"""




#18April2019
roscore
python kzpy3/VT_net2__29April2019/publish.py  pub_predictions 1 step 0
python kzpy3/VT_net2__29April2019/publish.py  pub_predictions 9 step 0
python kzpy3/VT_net2__29April2019/main.py # _['topic_suffix'] = ''
python kzpy3/VT_net2__29April2019/main.py # _['topic_suffix'] = '_'
python kzpy3/scripts/plot_topics.py topics headings_left_,headings_right_,headings_direct_ colors red,green,blue falloff 0.7
python kzpy3/scripts/plot_topics.py topics headings_left,headings_right,headings_direct colors red,green,blue falloff 0.7
python kzpy3/Menu_app/menu2.py path kzpy3/Cars/a2Apr19/nodes dic P
python kzpy3/Cars/a2Apr19/nodes/network_node.py desktop_mode 1
rosplay_menu.py


"""

from kzpy3.vis3 import *
from scipy.optimize import curve_fit
import kzpy3.Menu_app.menu2 as menu2
import default_values
from subscribe import S
import prediction_images
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




from sensor_msgs.msg import Image
import cv_bridge
rospy.init_node('main',anonymous=True)
Pub = {}
Pub['ldr_img'] = rospy.Publisher("/ldr_img"+_['topic_suffix'],Image,queue_size=1)
Path_pts2D = prediction_images.Array(300,2)
if __name__ == '__main__':

    
    Prediction2D_plot = CV2Plot(height_in_pixels=141,width_in_pixels=62,pixels_per_unit=7,y_origin_in_pixels=41)

    Prediction2D_plot['verbose'] = False

    pts2D_multi_step = []

    path_pts2D = []

    while not _['ABORT']:
        time.sleep(0.001)
        if True:
        #try:
            load_parameters(_)

            headings,encoders,motors = {},{},{}
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
            if 'behavioral_mode' not in S:
                motor = S['motor']
            elif S['behavioral_mode'] not in ['left','direct','right'] or S['human_agent']:
                motor = S['motor']
            else:
                motor = S['cmd/motor']
            direction = 1.
            if motor < 49:
                direction = -1.
            #print direction,dp(encoder,1),motor,S['cmd/motor'],S['motor']

            Prediction2D_plot,left_camera_3D_img,metadata_3D_img = \
                prediction_images.prepare_2D_and_3D_images(Prediction2D_plot,pts2D_multi_step,d_heading,encoder,sample_frequency,headings,encoders,motors,S['left_image'],_)


            prediction_images.get__path_pts2D(d_heading,encoder,sample_frequency,direction,Path_pts2D,_)

            if False:
                clf()
                plt_square()
                xyliml(_['plot xylims'])
                pts_plot(Path_pts2D['array'],sym=',')#_['pts sym'])
                d = Path_pts2D['data']
                e = d[d[:,2]<0]
                pts_plot(e,color='b',sym=_['pts sym'])
                spause()



            """
            path_pts2D = prediction_images.get__path_pts2D(d_heading,encoder,sample_frequency,direction,path_pts2D,_)

            path_pts2D = path_pts2D[-min(len(path_pts2D),300):]

            clf();plt_square();xyliml(_['plot xylims']);pts_plot(na(path_pts2D),sym=_['pts sym']);spause();
            """


            prediction_images.show_maybe_save_images(Prediction2D_plot,left_camera_3D_img,metadata_3D_img,_)

            Pub['ldr_img'].publish(cv_bridge.CvBridge().cv2_to_imgmsg(metadata_3D_img,'rgb8'))

        else:
        #except KeyboardInterrupt:
            cr('*** KeyboardInterrupt ***')
            sys.exit()
        #except Exception as e:
            cr('*** index',_['index'],'failed ***')
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
            time.sleep(1)  
        
      

    
##############################################################
##############################################################

cg('\n\nDone.\n')

#EOF