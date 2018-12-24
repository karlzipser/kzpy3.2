####################### IMPORT ################################
#
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
cg("To start menu:\n\tpython kzpy3/Menu_app/menu2.py path",project_path,"dic P")

import fit3d
exec(identify_file_str)
_ = default_values._
#
##############################################################

assert 'run' in Arguments




########################################################################################
########################################################################################
########################################################################################
####
def CV2Plot(height_in_pixels,width_in_pixels,pixels_per_unit,x_origin_in_pixels=None,y_origin_in_pixels=None):
    if x_origin_in_pixels == None:
        x_origin_in_pixels = intr(width_in_pixels/2.0)
    if y_origin_in_pixels == None:
        y_origin_in_pixels = intr(height_in_pixels/2.0)
    D = {}
    D['verbose'] = True
    if D['verbose']:
        cy(x_origin_in_pixels,y_origin_in_pixels)
    D['image'] = zeros((height_in_pixels,width_in_pixels,3),np.uint8)
    def function_show(autocontrast=True):
        
        img = D['image']
        if autocontrast:
            img = z2_255_by_channel(img)
            #cg(img.min(),img.max())
        mci(img,scale=4.0,delay=1)
    def function_safe(px,py):
        if px >= 0:
            if py >= 0:
                if py < height_in_pixels:
                    if px < width_in_pixels:
                        return True
        if D['verbose']:
            cr('not safe')
        return False
    def function_get_pixel(x,y):
        px = intr(x * pixels_per_unit)
        py = intr(-y * pixels_per_unit)
        px += x_origin_in_pixels
        py += y_origin_in_pixels
        if D['verbose']:
            cb(x,y,"->",px,py)
        return px,py
    def function_plot_point_xy_version(x,y,c=[255,255,255],add_mode=False):
        px,py = D['get pixel'](x,y)
        if D['safe?'](px,py):
            if not add_mode:
                D['image'][py,px,:] = c
            else:
                D['image'][py,px,:] += na(c,np.uint8)
    def function_pts_plot(xys,c=[255,255,255],add_mode=False):
        if type(c) == str:
            if add_mode:
                n = 1
            else:
                n = 255
            if c == 'r':
                c = [n,0,0]
            elif c == 'g':
                c = [0,n,0]
            elif c == 'b':
                c = [0,0,n]  
            else:
                cr('warning, unknown color:',c)
                c = [255,255,255]
        for i in rlen(xys):
            D['plot point (xy_version)'](xys[i,0],xys[i,1],c,add_mode)
    def function_clear():
        D['image'] *= 0
    D['show'] = function_show
    D['safe?'] = function_safe
    D['plot point (xy_version)'] = function_plot_point_xy_version
    D['get pixel'] = function_get_pixel
    D['pts_plot'] = function_pts_plot
    D['clear'] = function_clear
    return D
####
########################################################################################
########################################################################################
########################################################################################

Cv2Plot = CV2Plot(height_in_pixels=23,width_in_pixels=41,pixels_per_unit=7,y_origin_in_pixels=23)
Cv2Plot['verbose'] = False

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
# 
##############################################################

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

runs = lo(opjD('Data/Network_Predictions_13Dec2018/runs.pkl'))
Runs = {}
for r in runs:
    Runs[fname(r)] = r
run_path = Runs[Arguments['run']]


U = lo(opjD('Data/Network_Predictions',fname(run_path)+'.net_predictions.pkl'))
O = h5r(opj(run_path,'original_timestamp_data.h5py' ))
L = h5r(opj(run_path,'left_timestamp_metadata_right_ts.h5py'))

_['headings'] = L['gyro_heading_x'][:]
_['encoders'] = L['encoder'][:]
_['motors'] = L['motor'][:]

Left_timestamps_to_left_indicies = {}
t0 = L['ts'][0]
for i in rlen(L['ts']):
    t = (1000.0*(L['ts'][i] - t0)).astype(int)
    Left_timestamps_to_left_indicies[t] = i

Colors = {'direct':'b','left':'r','right':'g'}

def get_r_points(behavioral_mode,headings,encoders,motors):
    xy = array([0.0,0.0])
    xys = []

    for i in range(len(headings)):
        v = vec(headings[i],encoders[i],motors[i],_['vec sample frequency']) #3.33)
        xy += v # take into consideration reverse driving
        xys.append(xy.copy())

    points_to_fit = na(xys[:3])
    x = points_to_fit[:,0]
    y = points_to_fit[:,1]
    m,b = curve_fit(f,x,y)[0]
    ang = np.degrees(angle_between([0,1],[1,m]))

    rpoints = na(xys)
    return rpoints

if True:#_['metadata_version']:
    metadata_version_list_dic = {}
    metadata_version_list_dic['index'] = []
    for i in range(_['num timesteps']):
        metadata_version_list_dic[d2n('i',i)] = []

RGBs = {'direct':(0,0,255),'right':(0,255,0),'left':(255,0,0)}
Color_index = {'direct':2,'right':1,'left':0}
blank_meta = np.zeros((23,41,3),np.uint8)


def show3d(Rpoints_list,left_index,delay=33,metadata_version=False):
    rmax = 7
    img = O['left_image']['vals'][left_index].copy()

    metadata_version_list = None
    if metadata_version:
        img1 = cv2.resize(img,(41,23))
        metadata_version_list = []
        img2 = 0*img1.astype(np.float)
    for q in range(len(Rpoints_list)-1,-1,-1):
        Rpoints = Rpoints_list[q]
        if metadata_version:
            pass#img2 = 0*img
        for behavioral_mode in Rpoints.keys():
            rpoints = Rpoints[behavioral_mode]
            for i in rlen(rpoints):
                a = rpoints[i,:]
                if a[1]<0:
                    continue
                try:
                    r = int(5.0/np.sqrt(a[0]**2+(a[1])**2))
                except:
                    r = 1
        
                b = fit3d.Point3(a[0], 0, a[1]-_['backup parameter'])
                c = fit3d.project(b, fit3d.mat)

                try:
                    if True:#not metadata_version:
                        good = True
                        if c.x < 0 or c.x >= 168:
                            good = False
                        elif c.y < 0 or c.y >= 94:
                            good = False
                        if good:               
                            if r < rmax:
                                cv2.circle(img,(int(c.x),int(c.y)),r,RGBs[behavioral_mode])
                    if metadata_version:
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

        if metadata_version:       
            metadata_version_list.append(img2)
            
                
    
    img = cv2.resize(img,(168*2,94*2))
    if _['use center line']:
        img[:,168,:] = int((127+255)/2)
    mci(img,scale=2.0,delay=delay,title='left camera w/ points')

    if metadata_version:
        for y in range(11,23):
            for c in range(3):
                if img2[y,:,c].max() > 0:
                    img2[y,:,c] = z2o(img2[y,:,c])
        #cr(img2.min(),img2.max())
        mci((255*img2).astype(np.uint8),scale=1,delay=1,title='metadata')
        #mi(img2);spause()
    if metadata_version:
        return metadata_version_list
    else:
        return None




if __name__ == '__main__':

    sample_frequency = 30.0

    Pts = []

    while _['index'] < len(U['ts']):
        if _['ABORT'] == True:
            break

        try:
            left_index = Left_timestamps_to_left_indicies[(1000.0*(U['ts'][_['index']] - t0)).astype(int)]
            Rpoints = {}

            for behavioral_mode in  _['behavioral_mode_list']:
                headings = U[behavioral_mode][_['index']]['heading']
                encoders = U[behavioral_mode][_['index']]['encoder']
                rpoints = get_r_points(behavioral_mode,headings,encoders,_['motors'])

                Rpoints[behavioral_mode] = rpoints

            if _['plt/show 2D']:
                if False:
                    clf(); plt_square(); xysqlim(_['plot_range'])
                Cv2Plot['clear']()
            Pts.append({})

            for behavioral_mode in _['behavioral_mode_list']:
                
                if len(Pts) > _['num timesteps']:
                    Pts = Pts[-_['num timesteps']:]
                Pts[-1][behavioral_mode] = []
                if True:#try:
                    rpoints = Rpoints[behavioral_mode]
                    indx = _['index']

                    Pts[-1][behavioral_mode] = list(rpoints)

            d_heading = _['headings'][indx]-_['headings'][indx-1]
            encoder = _['encoders'][indx]
            velocity = encoder * _['vel-encoding coeficient']
            a = na([0,1]) * velocity / sample_frequency

            for behavioral_mode in _['behavioral_mode_list']:        
                for i in rlen(Pts):
                    if behavioral_mode in Pts[i]:
                        Pts[i][behavioral_mode] = rotatePolygon(Pts[i][behavioral_mode],-d_heading)
                    else:
                        cr('A')
                if behavioral_mode in Pts[i]:
                    Pts[-1][behavioral_mode].append(a)
                else:
                    cr('C')
                for i in rlen(Pts):
                    if behavioral_mode in Pts[i] and behavioral_mode in Pts[-1]:
                        Pts[i][behavioral_mode] = Pts[i][behavioral_mode]-Pts[-1][behavioral_mode][-1]
                        if _['plt/show 2D']:
                            if False:
                                pts_plot(na(Pts[i][behavioral_mode]),Colors[behavioral_mode])
                            Cv2Plot['pts_plot'](na(Pts[i][behavioral_mode]),Colors[behavioral_mode],add_mode=True)
                    else:
                        cr('B')                    
                if _['plt/show 2D']:
                    if False:
                        plot(0,0,'ko');plot(0,0,'kx')

                    

                if False:#except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    CS_('Exception!',emphasis=True)
                    CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)

                if _['plt/show 2D']:
                    if False:
                        spause()
            Cv2Plot['show']()

            if _['show 3D']:
                metadata_version_list = show3d(Pts,left_index,_['cv2 delay'],_['metadata_version'])
                if metadata_version_list != None:
                    """
                    for i in range(_['num timesteps']):
                        ky = d2n('i',i)
                        if ky not in metadata_version_list_dic:
                            metadata_version_list_dic[ky] = []
                        if i >= len(metadata_version_list):
                            img = 0*metadata_version_list[0]
                        else:
                            img = metadata_version_list[i]
                        metadata_version_list_dic[ky].append(img)
                    metadata_version_list_dic['index'].append(_['index'])
                    first = True
                    for k in metadata_version_list_dic.keys():
                        if first:
                            l = len(metadata_version_list_dic[k])
                            first = False
                        else:
                            assert len(metadata_version_list_dic[k]) == l
                    """
                    pass
        except Exception as e:
            if _['metadata_version']:
                for k in metadata_version_list_dic.keys():
                    print k
                    if len(metadata_version_list_dic[k]) < _['index']+1:
                        if k == 'index':
                            cr(1)
                            metadata_version_list_dic[k].append(_['index'])
                        else:
                            metadata_version_list_dic[k].append(blank_meta)
                            cr(2)

            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)  
            
        load_parameters(_)
        if _['cmd/an impulse (click)']:
            _['cmd/an impulse (click)'] = False
            cr('hi')

        _['index'] += _['step_size']

        _['timer'].freq(d2s("_['index'] =",_['index'], int(100*_['index']/(1.0*len(U['ts']))),'%'))





#EOF
