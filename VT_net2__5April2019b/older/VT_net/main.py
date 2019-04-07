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
import fit3d
exec(identify_file_str)
P = default_values.P

#
##############################################################

assert 'run' in Arguments

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

runs = lo(opjD('Data/Network_Predictions_13Dec2018/runs.pkl'))
Runs = {}
for r in runs:
    Runs[fname(r)] = r
run_path = Runs[Arguments['run']]


U = lo(opjD('Data/Network_Predictions_13Dec2018',fname(run_path)+'.net_predictions.pkl'))
#U = lo(opjD('Data/Network_Predictions',fname(run_path)+'.net_predictions.pkl'))
O = h5r(opj(run_path,'original_timestamp_data.h5py' ))
L = h5r(opj(run_path,'left_timestamp_metadata_right_ts.h5py'))

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

if P['metadata_version']:
    metadata_version_list_dic = {}
    metadata_version_list_dic['index'] = []
    for i in range(P['num timesteps']):
        metadata_version_list_dic[d2n('i',i)] = []

RGBs = {'direct':(0,0,255),'right':(0,255,0),'left':(255,0,0)}
Color_index = {'direct':2,'right':1,'left':0}
blank_meta = np.zeros((23,41,3),np.uint8)


def show3d(Rpoints_list,left_index,delay=33,metadata_version=False):
    rmax = 7
    img = O['left_image']['vals'][left_index].copy()

    metadata_version_list = None
    if metadata_version:
        img = cv2.resize(img,(41,23))
        metadata_version_list = []

    for q in range(len(Rpoints_list)-1,-1,-1):
        Rpoints = Rpoints_list[q]
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
        pass
        #mci(img,scale=6.0,delay=delay,title='left camera w/ points, metadata_version')
        #mci(img2,scale=6.0,delay=delay,title='left camera w/ points, metadata_version2')

    

    if metadata_version:
        return metadata_version_list
    else:
        return None




if __name__ == '__main__':

    sample_frequency = 30.0

    Pts = []

    while P['index'] < len(U['ts']):
        if P['ABORT'] == True:
            break

        try:
            left_index = Left_timestamps_to_left_indicies[(1000.0*(U['ts'][P['index']] - t0)).astype(int)]
            Rpoints = {}

            for behavioral_mode in  ['left','direct','right']:
                headings = U[behavioral_mode][P['index']]['heading']
                encoders = U[behavioral_mode][P['index']]['encoder']
                rpoints = get_r_points(behavioral_mode,headings,encoders)


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

            d_heading = P['headings'][indx]-P['headings'][indx-1]
            encoder = P['encoders'][indx]
            velocity = encoder * P['vel-encoding coeficient'] # rough guess
            a = na([0,1]) * velocity / sample_frequency

            for behavioral_mode in ['left','direct','right']:        
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
                        if P['show 2D']:
                            pts_plot(na(Pts[i][behavioral_mode]),Colors[behavioral_mode])
                    else:
                        cr('B')                    
                if P['show 2D']:
                    plot(0,0,'ko');plot(0,0,'kx')

                    

                if False:#except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    CS_('Exception!',emphasis=True)
                    CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)

                if P['show 2D']:
                    spause()

            if P['show 3D']:
                metadata_version_list = show3d(Pts,left_index,P['cv2 delay'],P['metadata_version'])
                if metadata_version_list != None:
                    for i in range(P['num timesteps']):
                        ky = d2n('i',i)
                        if ky not in metadata_version_list_dic:
                            metadata_version_list_dic[ky] = []
                        if i >= len(metadata_version_list):
                            img = 0*metadata_version_list[0]
                        else:
                            img = metadata_version_list[i]
                            #mci(metadata_version_list[i],scale=6.0,delay=P['cv2 delay'],title=d2s('metadata_version',i))
                        metadata_version_list_dic[ky].append(img)
                    metadata_version_list_dic['index'].append(P['index'])
                    first = True
                    for k in metadata_version_list_dic.keys():
                        if first:
                            l = len(metadata_version_list_dic[k])
                            first = False
                        else:
                            assert len(metadata_version_list_dic[k]) == l
        except Exception as e:
            if P['metadata_version']:
                for k in metadata_version_list_dic.keys():
                    print k
                    if len(metadata_version_list_dic[k]) < P['index']+1:
                        if k == 'index':
                            cr(1)
                            metadata_version_list_dic[k].append(P['index'])
                        else:
                            metadata_version_list_dic[k].append(blank_meta)
                            cr(2)

            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)  
            
        load_parameters(P)

        P['index'] += P['step_size']

        P['timer'].freq(d2s("P['index'] =",P['index'], int(100*P['index']/(1.0*len(U['ts']))),'%'))


        #if len(metadata_version_list_dic['i0']) > 100:
        #    break
    





    #print('here!')
    #CA()
    print len(metadata_version_list_dic['i8'])

    first = True
    for k in metadata_version_list_dic.keys():
        if first:
            l = len(metadata_version_list_dic[k])
            first = False
        else:
            assert len(metadata_version_list_dic[k]) == l
    """
    raw_enter()
    for i in rlen(metadata_version_list_dic['i8']):
        cg(i)
        mci(metadata_version_list_dic['i8'][i],scale=6.0,delay=66,title=d2s('metadata_version_list_dic'))
    raw_enter()
    """
    file_paths = [opjD('Data/Network_Predictions_projected',fname(run_path)+'.net_projections.h5py'),\
        opjD('Data/Network_Predictions_projected',fname(run_path)+'.net_projections.flip.h5py')]

    for file_path in file_paths:
        os.system(d2s('mkdir -p',pname(file_path)))
        F = h5w(file_path)
        pd2s('Topics:')
        D = metadata_version_list_dic
        for topic in D.keys():
            pd2s('\t',topic,len(D[topic]))
            if 'flip' in file_path:
                for i in rlen(D[topic]):
                    if topic != 'index':
                        D[topic][i] = cv2.flip(D[topic][i],1)
            F.create_dataset(topic,data=D[topic])
            cs( type(D[topic]),shape(D[topic]))      
        F.close()




#EOF
