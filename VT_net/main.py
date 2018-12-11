####################### IMPORT ################################
#
from kzpy3.vis3 import *
from scipy.optimize import curve_fit
import kzpy3.Menu_app.menu2 as menu2
project_path = pname(__file__).replace(opjh(),'')
project_import_prefix = project_path__to__project_import_prefix(project_path)
module_names = ['default_values','fit3d']
for m in module_names:
    exec_str = d2s('import',project_import_prefix+'.'+m,'as',m)
    cr(exec_str)
    exec(exec_str)

P = default_values.P
#
##############################################################


####################### MENU ################################
#
if P['start menu automatically'] and using_linux():
    dic_name = "P"
    sys_str = d2n("gnome-terminal -x python kzpy3/Menu_app/menu2.py path ",project_path," dic ",dic_name)
    cr(sys_str)
    os.system(sys_str)

parameter_file_load_timer = Timer(P['load_timer_time'])

def load_parameters(P,customer='customer0'):
    if parameter_file_load_timer.check():
        Topics = menu2.load_Topics(project_path,first_load=False,customer=customer)
        if type(Topics) == dict:
            for t in Topics['To Expose']['customer0']:
                if t in Arguments:
                    topic_warning(t)
                if '!' in t:
                    pass
                else:
                    P[t] = Topics[t]
        parameter_file_load_timer.reset()
# 
##############################################################

def vec(heading,encoder,sample_frequency=30.0):
	velocity = encoder * P['vel-encoding coeficient'] # rough guess
	a = [0,1]
	a = array(rotatePoint([0,0],a,heading))
	a *= velocity/sample_frequency
	return array(a)


def f(x,A,B):
    return A*x + B

U = lo( opjD(\
    'Data/16Nov2018_held_out_data/net_predictions.tegra-ubuntu_16Nov18_17h59m10s.pkl' ))
O = h5r(opjD(\
    'Data/16Nov2018_held_out_data/h5py/tegra-ubuntu_16Nov18_17h59m10s/original_timestamp_data.h5py' ))
L = h5r(opjD(\
    'Data/16Nov2018_held_out_data/h5py/tegra-ubuntu_16Nov18_17h59m10s/left_timestamp_metadata_right_ts.h5py'))
P['headings'] = L['gyro_heading_x'][:]
P['encoders'] = L['encoder'][:]
P['motors'] = L['motor'][:]

Left_timestamps_to_left_indicies = {}
t0 = L['ts'][0]
for i in rlen(L['ts']):
    t = (1000.0*(L['ts'][i] - t0)).astype(int)
    Left_timestamps_to_left_indicies[t] = i

Colors = {'direct':'b','left':'r','right':'g'}

def get_r_points(behavioral_mode,headings,encoders):
    xy = array([0.0,0.0])
    xys = []

    for i in range(len(headings)):
        v = vec(headings[i],encoders[i],P['vec sample frequency']) #3.33)
        xy += v # take into consideration reverse driving
        xys.append(xy.copy())

    points_to_fit = na(xys[:3])
    x = points_to_fit[:,0]
    y = points_to_fit[:,1]
    m,b = curve_fit(f,x,y)[0]
    ang = np.degrees(angle_between([0,1],[1,m]))

    rpoints = na(xys)
    return rpoints



RGBs = {'direct':(0,0,255),'right':(0,255,0),'left':(255,0,0)}

def show2d(rpoints,left_index,color='b',show_image=False):
    if show_image:
        mci(P['O']['left_image']['vals'][D[P['index']]-P['future_steps']],\
            scale=P['cv2 scale'],delay=P['cv2 delay'],title='left camera')
    pts_plot(rpoints,color=color,sym='.')
    P['timer'].freq()

def show3d(Rpoints,left_index):
    rmax = 7
    img = O['left_image']['vals'][left_index].copy()
    for behavioral_mode in Rpoints.keys():
        rpoints = Rpoints[behavioral_mode]
        for i in rlen(rpoints):
            a = rpoints[i,:]
            try:
                r = int(5.0/np.sqrt(a[0]**2+(a[1])**2))
            except:
                r = 1
    
            b = fit3d.Point3(a[0], 0, a[1]-P['backup parameter'])
            c = fit3d.project(b, fit3d.mat)
            try:
                good = True
                if c.x < 0 or c.x >= 168:
                    good = False
                elif c.y < 0 or c.y >= 94:
                    good = False
                if good:
                    if r < rmax:
                        cv2.circle(img,(int(c.x),int(c.y)),r,RGBs[behavioral_mode])
            except:
                cr(r)
                pass
    mci(cv2.resize(img,(168*2,94*2)),scale=2.0,delay=20,title='left camera w/ points')
    P['timer'].freq(d2s("P['index'] =",P['index']))




if __name__ == '__main__':

    sample_frequency = 30.0
    #pts = :[na([.2,.2])]
    Pts = {'left':[na([.2,.2])],'direct':[na([.2,.2])],'right':[na([.2,.2])]}

    while P['index'] < len(U['ts']):
        if P['ABORT'] == True:
            break
        left_index = Left_timestamps_to_left_indicies[(1000.0*(U['ts'][P['index']] - t0)).astype(int)]
        Rpoints = {}
        if P['show 2D']:
            clf();plt_square();xylim(-2.5,2.5,0,5)
        for behavioral_mode in  ['left','direct','right']:
            headings = U[behavioral_mode][P['index']]['heading']
            encoders = U[behavioral_mode][P['index']]['encoder']
            rpoints = get_r_points(behavioral_mode,headings,encoders)

            if P['show 2D']:
                show2d(rpoints,left_index,Colors[behavioral_mode],True)
            Rpoints[behavioral_mode] = rpoints
        if P['show 3D']:
            show3d(Rpoints,left_index)
        spause()
        load_parameters(P)








        if True:

            clf(); plt_square(); xysqlim(P['l'])

            for behavioral_mode in Pts.keys():
                
                try:
                    rpoints = Rpoints[behavioral_mode]
                    indx = P['index']

                    d_heading = P['headings'][indx]-P['headings'][indx-1]
                    encoder = P['encoders'][indx]
                    velocity = encoder * P['vel-encoding coeficient'] # rough guess
                    a = na([0,1]) * velocity / sample_frequency
                    #cb(dp(encoder),dp(d_heading))

                    Pts[behavioral_mode] += list(rpoints)
                    if len(Pts[behavioral_mode])>P['num points']:
                        Pts[behavioral_mode] = Pts[behavioral_mode][-P['num points']:]
                    Pts[behavioral_mode] = rotatePolygon(Pts[behavioral_mode],d_heading)
                    Pts[behavioral_mode].append(a)
                    Pts[behavioral_mode] = list(na(Pts[behavioral_mode])-Pts[behavioral_mode][-1])
                    indx += 1
                    pts_plot(na(Pts[behavioral_mode]),Colors[behavioral_mode])
                    plot(0,0,'b.')

                    

                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    CS_('Exception!',emphasis=True)
                    CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)

            spause()




















        P['index'] += P['step_size']
   # raw_enter("Done. ")





#EOF
