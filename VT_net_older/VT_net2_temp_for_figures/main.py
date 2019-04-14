####################### IMPORT ################################
# python kzpy3/VT_net2_/main.py run tegra-ubuntu_29Oct18_13h28m05s
from kzpy3.vis3 import *
from scipy.optimize import curve_fit
import kzpy3.Menu_app.menu2 as menu2
import default_values
cr(__file__)
cr(pname(__file__))
project_path = pname(__file__).replace(opjh(),'')
if project_path[0] == '/':
    project_path = project_path[1:]
sys_str = d2s('mkdir -p',opj(project_path,'__local__'))
cg(sys_str)
os.system(sys_str)
cg("To start menu:\n\tpython kzpy3/Menu_app/menu2.py path",project_path,"dic _")
output_images = []
import fit3d#_torch as fit3d
exec(identify_file_str)
_ = default_values._
#
##############################################################

####################### MENU ################################
#
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
            for t in Topics['To Expose']['VT menu']:
                if t in Arguments:
                    topic_warning(t)
                if '!' in t:
                    pass
                else:
                    _[t] = Topics[t]
        parameter_file_load_timer.reset()


start_signal = True
if _['wait for start signal']:
    cr('Wait for impulse click from menu...')
    start_signal = False
while start_signal == False:
    if _['ABORT'] == True:
        sys.exit()
    load_parameters(_)
    if _['cmd/an impulse (click)']:
        _['cmd/an impulse (click)'] = False
        cr('An impulse, test of click. Continue work...')
        start_signal = True

#
##############################################################

##############################################################
#
assert 'run' in Arguments
runs = lo(opjD('Data/Network_Predictions/runs.pkl'))
Runs = {}
for r in runs:
    Runs[fname(r)] = r
run_path = Runs[Arguments['run']]
U = lo(opjD('Data/Network_Predictions',fname(run_path)+'.net_predictions.pkl'))

L,O,___ = open_run(run_name=Arguments['run'],h5py_path=pname(run_path),want_list=['L','O'])

_['headings'] = L['gyro_heading_x'][:]
_['encoders'] = L['encoder'][:]
_['motors'] = L['motor'][:]

Left_timestamps_to_left_indicies = {}
t0 = L['ts'][0]

if _['save metadata']:
    metadata_img_list = []
blank_meta = np.zeros((23,41,3),np.uint8)
for i in rlen(L['ts']):
    t = (1000.0*(L['ts'][i] - t0)).astype(int)
    Left_timestamps_to_left_indicies[t] = i
    if _['save metadata']:
        metadata_img_list.append(blank_meta)

#############################################################################

#############################################################################

Colors = {'direct':'b','left':'r','right':'g'}
RGBs = {'direct':(0,0,255),'right':(0,255,0),'left':(255,0,0)}
Color_index = {'direct':2,'right':1,'left':0}
#
##############################################################

##############################################################
#
def vec(heading,encoder,motor,sample_frequency=30.0):
    velocity = encoder * _['vel-encoding coeficient'] # rough guess
    if motor < 49:
        velocity *= -1.0
    a = [0,1]
    a = array(rotatePoint([0,0],a,heading))
    a *= velocity/sample_frequency
    return array(a)

def f(x,A,B):
    return A*x + B

def get_predictions2D(behavioral_mode,headings,encoders,motors):
    xy = array([0.0,0.0])
    xys = []

    for i in range(len(headings)):
        v = vec(headings[i],encoders[i],motors[i],_['vec sample frequency']) #3.33)
        xy += v
        xys.append(xy.copy())

    points_to_fit = na(xys[:3])
    x = points_to_fit[:,0]
    y = points_to_fit[:,1]
    m,b = curve_fit(f,x,y)[0]
    ang = np.degrees(angle_between([0,1],[1,m]))

    pts2D_1step = na(xys)
    return pts2D_1step


def get_prediction_images_3D(pts2D_1step_list,left_index):
    rmax = 7
    img = O['left_image']['vals'][left_index].copy()
    metadata_version_list = None
    img1 = cv2.resize(img,(41,23))
    metadata_version_list = []
    img2 = 0*img1.astype(np.float)
    for q in range(len(pts2D_1step_list)-1,-1,-1):
        Pts2D_1step = pts2D_1step_list[q]

        for behavioral_mode in Pts2D_1step.keys():
            pts2D_1step = Pts2D_1step[behavioral_mode]
            for i in rlen(pts2D_1step):
                a = pts2D_1step[i,:]
                if a[1]<0:
                    continue
                try:
                    r = int(5.0/np.sqrt(a[0]**2+(a[1])**2))
                except:
                    r = 1
        
                b = fit3d.Point3(a[0], 0, a[1]-_['backup parameter'])
                c = fit3d.project(b, fit3d.mat)

                try:
                    if True:
                        good = True
                        if c.x < 0 or c.x >= 168:
                            good = False
                        elif c.y < 0 or c.y >= 94:
                            good = False
                        if good:             
                            if r < rmax:
                                cv2.circle(img,(int(c.x),int(c.y)),r,RGBs[behavioral_mode],thickness=_['thickness'])
                    good = True
                    cx = intr(c.x * 0.245)
                    cy = intr(c.y * 0.245)
                    if cx < 0 or cx >= 41:
                        good = False
                    elif cy < 0 or cy >= 23:
                        good = False
                    if good:               
                        img1[cy,cx,:] = RGBs[behavioral_mode]
                        img2[cy,cx,Color_index[behavioral_mode]] += 1

                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    CS_('Exception!',emphasis=True)
                    CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
                    cr(r)


    img = cv2.resize(img,(168*2,94*2))
    if _['use center line']:
        img[:,168,:] = int((127+255)/2)
    left_camera_3D_img = img


    for y in range(11,23):
        for c in range(3):
            if img2[y,:,c].max() > 0:
                img2[y,:,c] = z2o(img2[y,:,c])
    metadata_3D_img = (255*img2).astype(np.uint8)

    return left_camera_3D_img,metadata_3D_img




if __name__ == '__main__':


    Prediction2D_plot = CV2Plot(height_in_pixels=23,width_in_pixels=41,pixels_per_unit=7,y_origin_in_pixels=23) ###########
    Prediction2D_plot['verbose'] = False ###########

    sample_frequency = 30.0

    pts2D_multi_step = []

    while _['index'] < len(U['ts']):

        ##########################################################
        #
        load_parameters(_)
        if _['cmd/an impulse (click)']:
            _['cmd/an impulse (click)'] = False
            cr('An impulse, test of click.')
        #
        ##########################################################

        if _['ABORT'] == True:
            so(_['output_file'],output_images)
            break

        Pts2D_1step = {}

        ##########################################################
        #
        try:

            for behavioral_mode in _['behavioral_mode_list']:
                headings = _['U_heading_gain'] * U[behavioral_mode][_['index']]['heading']
                encoders = U[behavioral_mode][_['index']]['encoder']
                pts2D_1step = get_predictions2D(behavioral_mode,headings,encoders,_['motors'])
                Pts2D_1step[behavioral_mode] = pts2D_1step
            #################
            #
            Prediction2D_plot['clear']()
            #
            #################
            pts2D_multi_step.append({})

            for behavioral_mode in _['behavioral_mode_list']:
                
                if len(pts2D_multi_step) > _['num timesteps']:
                    pts2D_multi_step = pts2D_multi_step[-_['num timesteps']:]
                pts2D_multi_step[-1][behavioral_mode] = list(Pts2D_1step[behavioral_mode])

            indx = _['index']
            d_heading = _['headings'][indx]-_['headings'][indx-1]
            encoder = _['encoders'][indx]
            velocity = encoder * _['vel-encoding coeficient']
            trajectory_vector = na([0,1]) * velocity / sample_frequency

            for behavioral_mode in _['behavioral_mode_list']:        
                for i in rlen(pts2D_multi_step):
                    pts2D_multi_step[i][behavioral_mode] = rotatePolygon(pts2D_multi_step[i][behavioral_mode],-d_heading)
                pts2D_multi_step[-1][behavioral_mode].append(trajectory_vector)
                for i in rlen(pts2D_multi_step):
                    pts2D_multi_step[i][behavioral_mode] = pts2D_multi_step[i][behavioral_mode] - pts2D_multi_step[-1][behavioral_mode][-1]
                    ###################
                    #
                    Prediction2D_plot['pts_plot'](na(pts2D_multi_step[i][behavioral_mode]),Colors[behavioral_mode],add_mode=True)
                    #
                    ###################

            left_index = Left_timestamps_to_left_indicies[(1000.0*(U['ts'][_['index']] - t0)).astype(int)]
            left_camera_3D_img,metadata_3D_img = get_prediction_images_3D(pts2D_multi_step,left_index)
            if _['save metadata']:
                metadata_img_list[left_index] = metadata_3D_img

      
            #cv2.waitKey(1)
            if _['show timer'].check():
                
                #################
                # 
                Prediction2D_plot['show']()
                mci(left_camera_3D_img,title='left_camera_3D_img',delay=_['cv2 delay'],scale=_['3d image scale'])
                output_images.append(left_camera_3D_img)
                #mi(left_camera_3D_img);spause();raw_enter()
                mci(metadata_3D_img,title='metadata_3D_img',delay=_['cv2 delay'])
                output_images.append(left_camera_3D_img)
                #
                #################
                _['show timer'] = Timer(_['show timer time']) 


        except Exception as e:
            cr('*** index',_['index'],'failed ***')
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)  
        #
        ##########################################################


        _['index'] += _['step_size']
        _['timer'].freq(d2s("_['index'] =",_['index'], int(100*_['index']/(1.0*len(U['ts']))),'%'))


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

cg('\n\nDone.\n')
#EOF
