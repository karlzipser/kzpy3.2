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



if 'encoders' not in P:
    cs("Loading L and O...")
    L = h5r(opj(P['run_folder'],"left_timestamp_metadata_right_ts.h5py"))
    P['O'] = h5r(opj(P['run_folder'],"original_timestamp_data.h5py"))
    P['headings'] = L['gyro_heading_x'][:]
    P['encoders'] = L['encoder'][:]
    P['motors'] = L['motor'][:]
    L.close()



####################### MENU ################################
#
if P['start menu automatically'] and using_linux():
    sys_str = d2n("gnome-terminal -x python kzpy3/Menu_app/menu2.py path ",project_path," dic P")
    cr(sys_str)
    os.system(sys_str)

parameter_file_load_timer = Timer(P['load_timer_time'])

def parameter_thread(P):
    while not P['ABORT']:
        time.sleep(0.1)
        load_parameters(P)

def load_parameters(P):
    if parameter_file_load_timer.check():
        #print project_path
        Topics = menu2.load_Topics(project_path,first_load=False,customer='customer0')
        if type(Topics) == dict:
            for t in Topics['To Expose']['customer0']:
                if t in Arguments:
                    topic_warning(t)
                if '!' in t:
                    pass
                else:
                    P[t] = Topics[t]
        parameter_file_load_timer.reset()


# threading.Thread(target=parameter_thread,args=[P]).start()
##############################################################



def vec(heading,encoder,sample_frequency=30.0):
    velocity = encoder * P['vel-encoding coeficient'] # rough guess
    a = [0,1]
    a = array(rotatePoint([0,0],a,heading))
    a *= velocity/sample_frequency
    return array(a)

def equation_of_a_line(x,A,B):
    return A*x + B




################################################################################################
#
def Raw_to_Trajectory(P):

    D = {}
    D['xy'] = array([0.0,0.0])
    D['xys'] = []
    D['index'] = P['good_starts'][P['start_index_choice']][1]
    
    D['max_index'] = len(P['headings']) - (P['future_steps']+P['past_steps'])

    def _step():
        D['index'] += P['step_size']
        if D['index'] < D['max_index']:
            P['index_timer!'].message(d2s("D['index'] =", D['index']))
            return True
        return False

    def _get():
        
        heading = P['headings'][D['index']]
        encoder = P['encoders'][D['index']]
        motor = P['motors'][D['index']]
        if motor < 49:
            encoder *= -1
        v = vec(heading,encoder)
        D['xy'] += v
        D['xys'].append(array(D['xy']))

        if len(D['xys']) < P['future_steps']+P['past_steps']:
            return False

        points = na(D['xys'])[-(P['future_steps']+P['past_steps']):]
        points -= points[P['past_steps'],:]
        points_to_fit = points[P['past_steps']-P['offset']:P['past_steps']+P['offset'],:]
        x = points_to_fit[:,0]
        y = points_to_fit[:,1]
        m,b = curve_fit(equation_of_a_line,x,y)[0]
        ang = np.degrees(angle_between([0,1],[1,m]))
        P['angs'].append(ang)
        rpoints = na(rotatePolygon(points,ang))
        rpoints *= -1
        D['rpoints'] = rpoints
        return True

    def _show2d():
        clf();plt_square();xylim(-P['l']/2,P['l']/2,-P['l']/2,P['l'])
        pts_plot(D['rpoints'][:P['past_steps'],:],'r',sym='.')
        pts_plot(D['rpoints'][P['past_steps']:,:],'b',sym='x')
        spause()
        P['timer'].freq()


    def _show3d():
        img = P['O']['left_image']['vals'][D['index']-P['future_steps']].copy()

        for i in range(P['past_steps'],len(D['rpoints']),P['step_skip']):

            a = D['rpoints'][i,:]

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
                    cv2.circle(img,(int(c.x),int(c.y)),r,(255,0,0))
            except:
                cr(r)
                pass
        mci(img,scale=P['cv2 scale'],delay=P['cv2 delay'],title='left camera w/ points')

    D['step'] = _step
    D['get'] = _get
    D['show2d'] = _show2d
    D['show3d'] = _show3d
    return D





#
################################################################################################




#pts = list(np.random.randn(600,2)*30)
#indx = 12000
pts = [na([.2,.2])]

if __name__ == '__main__':

    CA()

    Raw_to_trajectory = Raw_to_Trajectory(P)
    ctr = 0
    sample_frequency = 30.0
    while P['ABORT'] != True:
        if not Raw_to_trajectory['get']():
            continue
        if P['show 2D']:
            Raw_to_trajectory['show2d']()
        if P['show 3D']:
            Raw_to_trajectory['show3d']()

        if True:

            try:
                indx = Raw_to_trajectory['index'] - (P['future_steps'])#+P['past_steps'])
                img = P['O']['left_image']['vals'][indx]
                mci(img,scale=P['cv2 scale'],delay=P['cv2 delay'],title='d_heading')
                d_heading = P['headings'][indx]-P['headings'][indx-1]
                encoder = P['encoders'][indx]
                velocity = encoder * P['vel-encoding coeficient'] # rough guess
                a = na([0,1]) * velocity / sample_frequency
                cb(dp(encoder),dp(d_heading))
                
                pts = rotatePolygon(pts,d_heading)
                pts.append(a)
                pts = list(na(pts)-pts[-1])
                indx += 1
                clf();pts_plot(na(pts));plt_square();xysqlim(20)
                plot(0,0,'b.')
                #plot(indx,d_heading,'r.')
                spause()
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                CS_('Exception!',emphasis=True)
                CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)




        if not Raw_to_trajectory['step']():
            break
        load_parameters(P)
        """
        try:
            if ctr > 10:
                #figure('ang');clf();plot(P['angs'][:],'b.')
                spause()
                pass
                ctr = 0
            else:
                ctr += 1
        except:
            print len(P['angs'])
            pass
        """
    #raw_enter()







#EOF
