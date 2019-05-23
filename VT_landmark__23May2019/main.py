##############################################################
####################### SETUP ################################
############
from kzpy3.vis3 import *
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


Path_pts2D = prediction_images.Array(_['num Array pts'],2)

rospy.init_node('main',anonymous=True)

gyro_heading_x = 0

if __name__ == '__main__':

    graphics_timer = Timer(_['graphics_timer time'])
    ts = time.time()

    while not _['ABORT']:
        time.sleep(0.001)
        #if True:
        try:
            load_parameters(_)
            gyro_heading_x_prev = gyro_heading_x
            gyro_heading_x =        S['gyro_heading_x']
            #cy(S['gyro_heading_x'])
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

            #
            #cm(direction,dp(encoder,1),motor,S['cmd/motor'],S['motor'])

            
            ts_prev = ts
            ts = time.time()
            dts = ts - ts_prev
            sample_frequency = 1.0 / dts
            d_heading = gyro_heading_x - gyro_heading_x_prev

        except:
            print "fail",time.time()
            continue

        if True:

            if encoder < 0.1:#direction < 0 or encoder < 0.1:
                value = -1
            else:
                value = 1

            prediction_images.get__path_pts2D(
                d_heading,
                encoder,
                sample_frequency,
                direction,
                value,
                Path_pts2D,
                _
            )

            if graphics_timer.check():
                graphics_timer.time_s = _['graphics_timer time']
                graphics_timer.reset()

                if False:
                    clf()
                    plt_square()
                    #xyliml(_['plot xylims'])
                    #print Path_pts2D['array']
                    pts_plot(Path_pts2D['array'],sym=_['pts sym'])#_['pts sym'])
                    d = Path_pts2D['data']
                    e = d[d[:,2]<0]
                    pts_plot(e,color='b',sym=_['pts sym'])
                    spause()

                Path_pts2D['show'](
                    height_in_pixels=200,
                    width_in_pixels=200,
                    pixels_per_unit=6.,
                    x_origin_in_pixels=None,
                    y_origin_in_pixels=None,
                    use_CV2_plot=True,
                    use_maplotlib=False,
                    do_print=False,
                    clear=True
                )

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