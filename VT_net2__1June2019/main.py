##############################################################
####################### SETUP ################################
############
from kzpy3.vis3 import *
import kzpy3.Menu_app.menu2 as menu2
import default_values
from subscribe import S
import prediction_images
import kzpy3.VT_net2__1June2019.rectangles as rectangles
import kzpy3.Array.Array
import std_msgs.msg
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
    #cm(0)
    if parameter_file_load_timer.check():
        parameter_file_load_timer.reset()
        Topics = menu2.load_Topics(project_path,first_load=False,customer=customer)
        if type(Topics) == dict:
            for t in Topics['To Expose'][customer]:
                if t in Arguments:
                    topic_warning(t)
                if '!' in t:
                    pass
                else:
                    P[t] = Topics[t]
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

Barrier_pts3D = kzpy3.Array.Array.Array(P['num barrier pts'],2)
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
Pub['rectangles_xys'] = rospy.Publisher(
    'rectangles_xys',
    std_msgs.msg.Float32MultiArray,
    queue_size = 1,
)

num_rectangle_patterns = 4
Rectangles = rectangles.Random_black_white_rectangle_collection(
    num_rectangle_patterns=num_rectangle_patterns,
)

rate = Timer(5)
P['just_stopped_from_forward_detected'] = Timer(10**9)

if __name__ == '__main__':

    graphics_timer = Timer(P['graphics_timer time'])
    ts = time.time()
    gyro_heading_x = 0
    camera_heading = 0

    while not P['ABORT']:
        
        try:
            load_parameters(P)            
            gyro_heading_x_prev =   gyro_heading_x
            gyro_heading_x =        S['gyro_heading_x']
            encoder =               S['encoder']
            camera_heading_prev = camera_heading
            if S['button_number'] == 4:
                #T['parameters']['the_motor'] = S['motor']
                camera = S['steer']
            else:
                #T['parameters']['the_motor'] = S['cmd/motor']
                camera = S['cmd/camera']

            ts_prev = ts
            ts = time.time()
            dts = ts - ts_prev
            sample_frequency = 1.0 / dts
            d_heading = gyro_heading_x - gyro_heading_x_prev
            camera_heading = (camera-49) * P['cmd_camera_to_camera_heading_cooeficient']

            d_camera_heading = camera_heading - camera_heading_prev
            #cm(d_camera_heading)

        except KeyboardInterrupt:
            cr('*** KeyboardInterrupt ***')
            sys.exit()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)    
            print "fail",time.time()
            continue
        direction = S['drive_direction']
        
        pop = False #True
        a = 0
        #cm(0,a,S['just_stopped_from_forward'])
        if P['just_stopped_from_forward_detected'].check() and direction == 0:
            P['just_stopped_from_forward_detected'].time_s = 10**9
            P['just_stopped_from_forward_detected'].reset()
            a = 1
            pop = False
            #cm(1,a)
        if S['just_stopped_from_forward'] == 1:
            pop = False
            P['just_stopped_from_forward_detected'].time_s = P['just_stopped_from_forward_detected_time']
            P['just_stopped_from_forward_detected'].reset()
            #cm(2,a)
        prediction_images.get__path_pts2D(
            d_heading + d_camera_heading,
            encoder,
            sample_frequency,
            direction,
            a,
            Path_pts2D,
            P,
            pop=pop,
        )
        #print S['just_stopped_from_forward'],a

        if graphics_timer.check():
            rate.freq()
            graphics_timer.time_s = P['graphics_timer time']
            graphics_timer.reset()

            Path_pts2D['check_ts'](
                P['point_lifetime'],
            )
                
            pts_3d = Barrier_pts3D['to_3D'](
                Path_pts2D,
                P['backup parameter'],
                min_dist=0.5,
                codes=[1],
            )

            Barrier_pts3D['check_ts'](
                P['circle_lifetime'],
            )
        
            xys = na(pts_3d)
            #print xys

            #if len(xys) > 0:
            xys4 = []
            for i in rlen(xys):
                x_ = xys[i,0]
                y_ = xys[i,1] #+ 1/3. ##### TEMP #########
                if y_ > -1:
                    xys4.append([x_,y_,np.sqrt(x_**2+y_**2),np.mod(i,num_rectangle_patterns)])
            xys4 = na(xys4)
            try:
                xys4 = xys4[ (-xys4[:,2] ).argsort() ]
            except:
                pass#print xys4
            Pub['rectangles_xys'].publish(data=xys4.reshape(4*len(xys4)))


 
        
      

    
##############################################################
##############################################################

cg('\n\nDone.\n')

#EOF
