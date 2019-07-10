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
import kzpy3.Array.test_Array
from sensor_msgs.msg import Image
import std_msgs.msg
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

Barrier_pts3D = kzpy3.Array.Array.Array(5,2)#P['num Array pts'],2)
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

stop_timer = Timer(P['stop_timer_time'])
slow_encoder = 0
slow_motor = 49
os.system('mkdir -p '+opjm('rosbags/imgs'))
rate = Timer(5)
move_timer = Timer(0.1)
avg_motor_val_prev = 49
avg_motor_val = 49
avg_encoder_val_prev = 0
avg_encoder_val = 0
first_slowdown = False

if __name__ == '__main__':

    graphics_timer = Timer(P['graphics_timer time'])
    delay_timer = Timer(1/30.)
    err_timer = Timer(5)
    ts = time.time()
    gyro_heading_x = 0
    camera_heading = 0
    direction2 = 1

    while not P['ABORT']:
        
        try:
            load_parameters(P)            
            gyro_heading_x_prev =   gyro_heading_x
            gyro_heading_x =        S['gyro_heading_x']
            encoder =               S['encoder']
            if 'behavioral_mode' not in S:
                motor = S['motor']
            elif S['behavioral_mode'] not in ['left','direct','right'] or S['human_agent']:
                motor = S['motor']
            else:
                motor = S['cmd/motor']

            ts_prev = ts
            ts = time.time()
            dts = ts - ts_prev
            sample_frequency = 1.0 / dts
            d_heading = gyro_heading_x - gyro_heading_x_prev

            camera_heading_prev = camera_heading

            camera_heading = (S['cmd/camera']-49) * P['cmd_camera_to_camera_heading_cooeficient']

            d_camera_heading = camera_heading - camera_heading_prev

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

        #try:
        if True:
            if encoder < 0.01 and not first_slowdown:
                first_slowdown = True
                avg_motor_val_prev = avg_motor_val
                avg_encoder_val_prev = avg_encoder_val
                sum_encoder_val = 0.
                sum_encoder_ctr = 0.
                sum_motor_val = 0.
                sum_motor_ctr = 0.
            else:
                first_slowdown = False
                sum_encoder_val += encoder
                sum_encoder_ctr += 1.
                sum_motor_val += motor
                sum_motor_ctr += 1.
            avg_motor_val = sum_motor_val/(max(sum_motor_ctr,1.0))
            avg_encoder_val = sum_encoder_val/(max(sum_encoder_ctr,1.0))
            msg = d2s(
                dp(avg_encoder_val),dp(avg_motor_val),
                dp(avg_encoder_val_prev),dp(avg_motor_val_prev)
            )
            #cr(encoder)
            #cg(msg)
            #move_timer.message(msg)





            s = P['slow_encoder_s']
            slow_encoder = s*slow_encoder + (1-s)*encoder
            slow_motor = s*slow_motor + (1-s)*motor

            direction = 1.
            if slow_motor < 45:
                direction = -1.

            if slow_encoder > 0.1:
                if slow_motor < 45:
                    direction2 = -1
                elif slow_motor > 54:
                    direction2 = 1
            
            if slow_encoder < 0.01 and direction2 == 1 and stop_timer.check(): #direction < 0 or encoder < 0.1:
                stop_timer.time_s = P['stop_timer_time']
                stop_timer.reset()
                value = 0
            elif direction2 > 0:
                value = 1
            else:
                value = -1

            #cg(dp(slow_encoder,2),dp(slow_motor,2),direction,direction2)
            
            pop = False #True
            if value == 0:
                pop = False
            prediction_images.get__path_pts2D(
                d_heading + d_camera_heading,
                encoder,
                sample_frequency,
                direction,
                value,
                Path_pts2D,
                P,
                pop=pop,
            )

            if graphics_timer.check():
                rate.freq()
                graphics_timer.time_s = P['graphics_timer time']
                graphics_timer.reset()

                Path_pts2D['check_ts'](P['point_lifetime'])
                if False:
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
                if False:
                    Path_pts3D['show'](
                        do_print=False,
                        use_maplotlib=False,
                        grid=False,
                        scale=1.0,
                        clear=True,
                        code=1,
                        color=(0,255,0), #(0,127,255),
                        show=False,
                        #background_image=S['left_image'],
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
                        background_image=S['left_image'],
                    )
                    
                pts_3d = Barrier_pts3D['to_3D'](
                    Path_pts2D,
                    P['backup parameter'],
                    min_dist=0.5,
                    codes=[0],
                )
                Barrier_pts3D['check_ts'](P['circle_lifetime'])
                if False:
                    Barrier_pts3D['show'](
                        do_print=False,
                        use_maplotlib=False,
                        use_CV2_circles=True,
                        grid=False,
                        scale=1.0,
                        clear=True,
                        code=0,
                        color=(255,0,0), #(0,127,255),
                        show=True,
                        background_image=S['left_image'],
                    )
                    

                xys = na(pts_3d)
                #cy(xys)
                if len(xys) > 0:
                    xys4 = []
                    for i in rlen(xys):
                        x_ = xys[i,0]
                        y_ = xys[i,1] + 1/3. ##### TEMP #########
                        xys4.append([x_,y_,np.sqrt(x_**2+y_**2),np.mod(i,num_rectangle_patterns)])

                    xys4 = na(xys4)
                    Pub['rectangles_xys'].publish(data=xys4.reshape(4*len(xys4)))

                    if False:
                        try:
                            xys4 = S['rectangles_xys'].reshape(len(S['rectangles_xys'])/4,4)
                            xys4_prev = xys4.copy()
                            #cg(xys4)
                            #cb(xys4_prev)
                            xys4_prev[:,1] += 0.0375
                            Xys = {
                                'now':  xys4,
                                'prev': xys4_prev,
                            }
                            temp = S['left_image'].copy()
                            I = {
                                'now':{
                                    'R':temp,
                                    'L':S['left_image'],
                                },
                                'prev':{
                                    'R':temp,
                                    'L':temp,
                                },
                            }
                            for when in ['now']:#,'prev']:
                                rectangles.paste_rectangles_into_drive_images(
                                    Xys[when],
                                    I[when],
                                    Rectangles,
                                    P['backup parameter'],
                                )
                            #mci(I['now']['L'],title="left")
                            #mci(S['left_image'],title='left.')
                            #imsave(opjm('rosbags/imgs/'+d2n(img_ctr,'.png')),I_L)#S['left_image'])#Barrier_pts3D['plot']['image'])
                        except Exception as e:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                            CS_('Exception!',emphasis=True)
                            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)        



            

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
