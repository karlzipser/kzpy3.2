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

def load_parameters(P,customer='VT menu'):
    if parameter_file_load_timer.check():
        Topics = menu2.load_Topics(project_path,first_load=False,customer=customer)
        if type(Topics) == dict:
            for t in Topics['To Expose']['VT menu']:
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
#U = lo('/home/karlzipser/Desktop/net_predictions.tegra-ubuntu_11Dec18_16h05m42s.pkl')
O = h5r(opjD(\
    'Data/16Nov2018_held_out_data/h5py/tegra-ubuntu_16Nov18_17h59m10s/original_timestamp_data.h5py' ))
L = h5r(opjD(\
    'Data/16Nov2018_held_out_data/h5py/tegra-ubuntu_16Nov18_17h59m10s/left_timestamp_metadata_right_ts.h5py'))
#O = h5r('/home/karlzipser/Desktop/Data/locations/local/left_right_center/h5py/tegra-ubuntu_11Dec18_16h05m42s/original_timestamp_data.h5py')
#L = h5r('/home/karlzipser/Desktop/Data/locations/local/left_right_center/h5py/tegra-ubuntu_11Dec18_16h05m42s/left_timestamp_metadata_right_ts.h5py')
#U = lo('/home/karlzipser/Desktop/Data/Network_Predictions/tegra-ubuntu_18Oct18_16h15m46s.net_predictions.pkl')
#O = h5r('/media/karlzipser/1_TB_Samsung_n1/tu_18to19Oct2018/locations/local/left_right_center/h5py/tegra-ubuntu_18Oct18_16h15m46s/original_timestamp_data.h5py')
#L = h5r('/media/karlzipser/1_TB_Samsung_n1/tu_18to19Oct2018/locations/local/left_right_center/h5py/tegra-ubuntu_18Oct18_16h15m46s/left_timestamp_metadata_right_ts.h5py')

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

metadata_version_list_dic = {}
for i in range(P['num timesteps']):
    metadata_version_list_dic[d2n('i',i)] = []

RGBs = {'direct':(0,0,255),'right':(0,255,0),'left':(255,0,0)}
Color_index = {'direct':2,'right':1,'left':0}

def show3d(Rpoints_list,left_index,delay=33,metadata_version=False):
    rmax = 7
    img = O['left_image']['vals'][left_index].copy()

    if metadata_version:
        img = cv2.resize(img,(41,23))
        metadata_version_list = []
    for Rpoints in Rpoints_list:
        if metadata_version:
            img2 = 0*img
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
        
                b = fit3d.Point3(a[0], 0, a[1]-P['backup parameter'])
                c = fit3d.project(b, fit3d.mat)

                try:
                    if not metadata_version:
                        good = True
                        if c.x < 0 or c.x >= 168:
                            good = False
                        elif c.y < 0 or c.y >= 94:
                            good = False
                        if good:               
                            if r < rmax:
                                cv2.circle(img,(int(c.x),int(c.y)),r,RGBs[behavioral_mode])
                    else:
                        good = True
                        cx = intr(c.x * 0.245)
                        cy = intr(c.y * 0.245)
                        if cx < 0 or cx >= 41:
                            good = False
                        elif cy < 0 or cy >= 23:
                            good = False
                        if good:               
                            img[cy,cx,:] = RGBs[behavioral_mode]
                            img2[cy,cx,Color_index[behavioral_mode]] = 255
                    """    
                    if not metadata_version:
                        good = True
                        if c.x < 0 or c.x >= 168:
                            good = False
                        elif c.y < 0 or c.y >= 94:
                            good = False
                        if good:                    
                            if r < rmax:
                                cv2.circle(img,(int(c.x),int(c.y)),r,RGBs[behavioral_mode])
                    else:
                        good = True
                        cx = intr(c.x * 0.245)
                        cy = intr(c.y * 0.245)
                        if cx < 0 or cx >= 41:
                            good = False
                        elif cy < 0 or cy >= 23:
                            good = False
                        if good:                    
                            img[cy,cx,:] = RGBs[behavioral_mode]
                    """ 

                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    CS_('Exception!',emphasis=True)
                    CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
                    cr(r)

        if metadata_version:       
            metadata_version_list.append(img2)
                
    if not metadata_version:
        mci(cv2.resize(img,(168*2,94*2)),scale=2.0,delay=delay,title='left camera w/ points')
    else:
        mci(img,scale=6.0,delay=delay,title='left camera w/ points, metadata_version')
        mci(img2,scale=6.0,delay=delay,title='left camera w/ points, metadata_version2')

    P['timer'].freq(d2s("P['index'] =",P['index']))

    if metadata_version:
        return metadata_version_list
    else:
        return None




if __name__ == '__main__':

    sample_frequency = 30.0
    #pts = :[na([.2,.2])]
    #Pts = {'left':[na([.2,.2])],'direct':[na([.2,.2])],'right':[na([.2,.2])]}
    Pts = []

    while P['index'] < len(U['ts']):
        if P['ABORT'] == True:
            break
        left_index = Left_timestamps_to_left_indicies[(1000.0*(U['ts'][P['index']] - t0)).astype(int)]
        Rpoints = {}
        #if P['show 2D']:
        #    clf();plt_square();xylim(-2.5,2.5,0,5)
        for behavioral_mode in  ['left','direct','right']:
            headings = U[behavioral_mode][P['index']]['heading']
            encoders = U[behavioral_mode][P['index']]['encoder']
            rpoints = get_r_points(behavioral_mode,headings,encoders)

            #if P['show 2D']:
            #    show2d(rpoints,left_index,Colors[behavioral_mode],True)
            Rpoints[behavioral_mode] = rpoints









        if P['show 2D']:

            clf(); plt_square(); xysqlim(P['plot_range'])

            Pts.append({})

            for behavioral_mode in ['left','direct','right']:
                
                if len(Pts) > P['num timesteps']:
                    Pts = Pts[-P['num timesteps']:]
                Pts[-1][behavioral_mode] = []
                if True:#try:
                    rpoints = Rpoints[behavioral_mode]
                    indx = P['index']

                    Pts[-1][behavioral_mode] = list(rpoints)

            #pprint(Pts)
            #cr(len(Pts))
            #raw_enter()

            d_heading = P['headings'][indx]-P['headings'][indx-1]
            encoder = P['encoders'][indx]
            velocity = encoder * P['vel-encoding coeficient'] # rough guess
            a = na([0,1]) * velocity / sample_frequency

            for behavioral_mode in ['left','direct','right']:        
                for i in rlen(Pts):
                    if behavioral_mode in Pts[i]:
                        Pts[i][behavioral_mode] = rotatePolygon(Pts[i][behavioral_mode],d_heading)
                    else:
                        cr('A')
                if behavioral_mode in Pts[i]:
                    Pts[-1][behavioral_mode].append(a)
                else:
                    cr('C')
                for i in rlen(Pts):
                    if behavioral_mode in Pts[i] and behavioral_mode in Pts[-1]:
                        Pts[i][behavioral_mode] = Pts[i][behavioral_mode]-Pts[-1][behavioral_mode][-1]
                        pts_plot(na(Pts[i][behavioral_mode]),Colors[behavioral_mode])
                    else:
                        cr('B')                    
                plot(0,0,'ko');plot(0,0,'kx')

                    

                if False:#except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    CS_('Exception!',emphasis=True)
                    CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)

            spause()

        if P['show 3D']:
            metadata_version_list = show3d(Pts,left_index,P['cv2 delay'],P['metadata_version'])
        if metadata_version_list != None:
            for i in rlen(metadata_version_list):
                print i
                metadata_version_list_dic[d2n('i',i)].append(metadata_version_list[i])
                mci(metadata_version_list[i],scale=6.0,delay=P['cv2 delay'],title=d2s('metadata_version',i))
        load_parameters(P)

 



        P['index'] += P['step_size']
        #if len(metadata_version_list_dic['i0']) > 100:
        #    break
    """
    print('here!')
    CA()
    print len(metadata_version_list_dic['i8'])
    raw_enter()
    for i in rlen(metadata_version_list_dic['i8']):
        cg(i)
        mci(metadata_version_list_dic['i8'][i],scale=6.0,delay=P['cv2 delay'],title=d2s('metadata_version_list_dic',i))
        raw_enter()
    """





#EOF
