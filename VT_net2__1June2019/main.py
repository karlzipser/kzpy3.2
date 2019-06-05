##############################################################
####################### SETUP ################################
############
from kzpy3.vis3 import *
import kzpy3.Menu_app.menu2 as menu2
import default_values
from subscribe import S
import prediction_images
import kzpy3.Array.Array
import kzpy3.Array.test_Array
from sensor_msgs.msg import Image
import cv_bridge
exec(identify_file_str)
P = default_values.P

rospy.init_node('main',anonymous=True)

project_path = pname(__file__).replace(opjh(),'')
if project_path[0] == '/':
    project_path = project_path[1:]
sys_str = d2s('mkdir -p',opj(project_path,'__local__'))
cg(sys_str)
os.system(sys_str)
cg("To start menu:\n\tpython kzpy3/Menu_app/menu2.py path",project_path,"dic P")

##
#############################################################
#############################################################

if False:
    def test(A={
        'a':1,
        'b':[1,2,3],
    }):
        B = {
        'a':A['b'],
        'b':A['a'],
        }
        return B

#############################################################
####################### MENU ################################
##
if P['start menu automatically'] and using_linux():
    dic_name = "P"
    sys_str = d2n("gnome-terminal --geometry 40x30+100+200 -x python kzpy3/Menu_app/menu2.py path ",project_path," dic ",dic_name)
    cr(sys_str)
    os.system(sys_str)

parameter_file_load_timer = Timer(P['load_timer_time'])

def load_parameters(P,customer='VT menu'):
    if parameter_file_load_timer.check():
        Topics = menu2.load_Topics(project_path,first_load=False,customer=customer)
        if type(Topics) == dict:
            for t in Topics['To Expose'][customer]:
                if t in Arguments:
                    topic_warning(t)
                if '!' in t:
                    pass
                else:
                    P[t] = Topics[t]
        parameter_file_load_timer.reset()

##
##############################################################
##############################################################


Path_pts2D = kzpy3.Array.Array.Array(P['num Array pts'],2)
Path_pts2D['setup_plot'](
    height_in_pixels=200,
    width_in_pixels=200,
    pixels_per_unit=P['pixels_per_unit'],
)

Path_pts3D = kzpy3.Array.Array.Array(P['num Array pts'],2)
height_in_pixels=94
width_in_pixels=168
x_origin_in_pixels=0
y_origin_in_pixels=height_in_pixels
pixels_per_unit=1
Path_pts3D['setup_plot'](
    height_in_pixels=height_in_pixels,
    width_in_pixels=width_in_pixels,
    x_origin_in_pixels=x_origin_in_pixels,
    y_origin_in_pixels=y_origin_in_pixels,
    pixels_per_unit=pixels_per_unit,
)

Barrier_pts3D = kzpy3.Array.Array.Array(P['num Array pts'],2)
height_in_pixels=94
width_in_pixels=168
x_origin_in_pixels=0
y_origin_in_pixels=height_in_pixels
pixels_per_unit=1
Barrier_pts3D['setup_plot'](
    height_in_pixels=height_in_pixels,
    width_in_pixels=width_in_pixels,
    x_origin_in_pixels=x_origin_in_pixels,
    y_origin_in_pixels=y_origin_in_pixels,
    pixels_per_unit=pixels_per_unit,
)


Pub = {}
Pub['ldr_img'] = rospy.Publisher("/ldr_img"+P['topic_suffix'],Image,queue_size=1)

if False:
    A = kzpy3.Array_.Array.Array(30,2)
    kzpy3.Array_.test_Array.test_Array()

if __name__ == '__main__':

    graphics_timer = Timer(P['graphics_timer time'])
    delay_timer = Timer(1/10.)
    err_timer = Timer(5)
    ts = time.time()
    gyro_heading_x = 0
    
    Prediction2D_plot = CV2Plot(height_in_pixels=141,width_in_pixels=62,pixels_per_unit=7,y_origin_in_pixels=41)

    Prediction2D_plot['verbose'] = False

    pts2D_multi_step = []

    path_pts2D = []

    
    while not P['ABORT']:

        if delay_timer.check():
            delay_timer.reset()
        else:
            time.sleep(0.01)
            load_parameters(P)
            continue
        try:
            try:
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
            except:
                err_timer.message(d2s('No net predictions coming in,',time.time()))
            
            gyro_heading_x_prev =   gyro_heading_x
            gyro_heading_x =        S['gyro_heading_x']
            encoder =               S['encoder']
            if 'behavioral_mode' not in S:
                motor = S['motor']
            elif S['behavioral_mode'] not in ['left','direct','right'] or S['human_agent']:
                motor = S['motor']
            else:
                motor = S['cmd/motor']
            direction = 1.
            if motor < 49:
                direction = -1.

            ts_prev = ts
            ts = time.time()
            dts = ts - ts_prev
            sample_frequency = 1.0 / dts
            d_heading = gyro_heading_x - gyro_heading_x_prev

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)    
            print "fail",time.time()
            continue


        if True: #try:

            if encoder < 0.1: #direction < 0 or encoder < 0.1:
                value = 0
            elif direction > 0:
                value = 1
            else:
                value = -1
            pop = False #True
            if value == 0:
                pop = False
            prediction_images.get__path_pts2D(
                d_heading,
                encoder,
                sample_frequency,
                direction,
                value,
                Path_pts2D,
                P,
                pop=pop,
            )

            if graphics_timer.check():
                graphics_timer.time_s = P['graphics_timer time']
                graphics_timer.reset()

                Path_pts2D['check_ts'](P['point_lifetime'])
                Path_pts2D['show'](
                    use_CV2_plot=True,
                    use_maplotlib=False,
                    do_print=False,
                    clear=True,
                    color=(255,255,0),
                    code=1,
                    show=False,
                    grid=False,
                    scale=1.0,
                )
                Path_pts2D['show'](
                    use_CV2_plot=True,
                    use_maplotlib=False,
                    do_print=False,
                    clear=False,
                    color=(255,0,0),
                    code=-1,
                    show=False,
                    grid=False,
                    scale=1.0,
                )
                Path_pts2D['show'](
                    use_CV2_plot=True,
                    use_maplotlib=False,
                    do_print=False,
                    clear=False,
                    color=(255,255,255),
                    code=0,
                    show=True,
                    grid=True,
                    scale=1.0,
                )

                Path_pts3D['to_3D'](Path_pts2D,P['backup parameter'])
                Path_pts3D['show'](
                    do_print=False,
                    use_maplotlib=False,
                    grid=False,
                    scale=1.0,
                    clear=True,
                    code=1,
                    color=(0,255,0), #(0,127,255),
                    show=False,
                    background_image=S['left_image'],
                )
                Path_pts3D['show'](
                    do_print=False,
                    use_maplotlib=False,
                    grid=False,
                    scale=1.0,
                    clear=False,
                    code=-1,
                    color=(255,0,0), #(0,127,255),
                    show=False,
                    #background_image=S['left_image'],
                )
                Path_pts3D['show'](
                    do_print=False,
                    use_maplotlib=False,
                    use_CV2_circles=False,
                    grid=True,
                    scale=1.0,
                    clear=False,
                    code=0,
                    color=(255,255,255), #(0,127,255),
                    show=True,
                    #background_image=S['left_image'],
                )

                Barrier_pts3D['to_3D'](
                    Path_pts2D,
                    P['backup parameter'],
                    min_dist=0.5,
                    codes=[-1],
                )
                Barrier_pts3D['check_ts'](P['circle_lifetime'])
                Barrier_pts3D['show'](
                    do_print=False,
                    use_maplotlib=False,
                    use_CV2_circles=True,
                    grid=True,
                    scale=1.0,
                    clear=True,
                    code=-1 ,
                    color=(255,0,0), #(0,127,255),
                    show=True,
                    background_image=S['left_image'],
                )

                #cg(dp(P['distance']),dp(P['velocity']))

            if len(motors.keys()) > 0:
                (
                    Prediction2D_plot,
                    left_camera_3D_img,
                    metadata_3D_img,
                ) = \
                prediction_images.prepare_2D_and_3D_images(
                        Prediction2D_plot,
                        pts2D_multi_step,
                        d_heading,
                        encoder,
                        sample_frequency,
                        headings,
                        encoders,
                        motors,
                        S['left_image'],
                        P,
                )


                prediction_images.show_maybe_save_images(
                    Prediction2D_plot,
                    left_camera_3D_img,
                    metadata_3D_img,
                    P,
                )

                Pub['ldr_img'].publish(
                    cv_bridge.CvBridge().cv2_to_imgmsg(
                        metadata_3D_img,
                        'rgb8',
                    )
                )

        else:
        #except KeyboardInterrupt:
            cr('*** KeyboardInterrupt ***')
            sys.exit()
        #except Exception as e:
            cr('*** index',P['index'],'failed ***')
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
            time.sleep(1)  
        
      

    
##############################################################
##############################################################

cg('\n\nDone.\n')

#EOF