##############################################################
####################### IMPORT ################################
############
from kzpy3.vis3 import *
from scipy.optimize import curve_fit
import kzpy3.Menu_app.menu2 as menu2
import default_values
from subscribe_no_ros import S,step
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

load_parameters(_)
#_['index'] = _['initial index']
##
##############################################################
##############################################################

save_timer = Timer(30)


if __name__ == '__main__':

    Prediction2D_plot = CV2Plot(height_in_pixels=141,width_in_pixels=62,pixels_per_unit=7,y_origin_in_pixels=41)

    Prediction2D_plot['verbose'] = False

    pts2D_multi_step = []

    headings,encoders,motors = {},{},{}

    
    mov = Timer(_['99 mov timer time'])

    while not _['ABORT']:

        first = True
        
        step()

        if first:
            headings['left'] =      S['headings_left']
            headings['direct'] =    S['headings_direct']
            headings['right'] =     S['headings_right']
            first = False

        mt_prev = _['99 mov timer time']
        load_parameters(_)
        if mt_prev !=  _['99 mov timer time']:
            cg('*** new 99 mov timer time, t =',_['99 mov timer time'],'***')
        

        camera_heading = (S['cmd/camera']-49) * _['cmd_camera_to_camera_heading_cooeficient']

        if np.abs(S['delta cmd/camera']) > 3:
            cb(np.abs(S['delta cmd/camera']))
            mov.time_s = _['99 mov timer time'] * S['delta cmd/camera']/99. + 3/30.
            mov.reset()

        if not mov.check():
            cg("mov.time() =",intr(1000*mov.time()),"ms")
            pass

        else:
            headings['left'] =      S['headings_left'] + camera_heading
            headings['direct'] =    S['headings_direct'] + camera_heading
            headings['right'] =     S['headings_right'] + camera_heading
        
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


        #pts2D_multi_step = prediction_images.get__pts2D_multi_step_2(d_heading,encoder,S['steer'],sample_frequency,headings,encoders,motors,pts2D_multi_step,S,_)

        if True:
            Prediction2D_plot,left_camera_3D_img,metadata_3D_img = \
                prediction_images.prepare_2D_and_3D_images(
                    Prediction2D_plot,
                    pts2D_multi_step,
                    d_heading,
                    encoder,
                    S['steer'],
                    sample_frequency,
                    headings,
                    encoders,
                    motors,
                    S['left_image'],
                    S,
                    _)
            prediction_images.show_maybe_save_images(Prediction2D_plot,left_camera_3D_img,metadata_3D_img,_)

        if save_timer.check2():
            soD(pts2D_multi_step,'pts2D_multi_step')




##############################################################
##############################################################



#EOF