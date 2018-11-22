###start
from kzpy3.vis3 import *
from scipy.optimize import curve_fit
import kzpy3.Menu_app.menu2 as menu2
import kzpy3.scratch.VT.default_values as default_values
import kzpy3.scratch.VT.fit3d as fit3d
P = default_values.P
Point3 = fit3d.Point3
project = fit3d.project

if P['start menu automatically']:
    os.system(d2n("gnome-terminal -x python kzpy3/Menu_app/menu2.py path ","kzpy3/scratch/VT"," dic P"))




"""
https://stackoverflow.com/questions/76134/how-do-i-reverse-project-2d-points-into-3d
http://pyopengl.sourceforge.net/documentation/installation.html
"""

if 'encoders' not in P:
    cs("Loading L and O...")
    L = h5r(opjD(P['run_folder'],"left_timestamp_metadata_right_ts.h5py"))
    P['O'] = h5r(opjD(P['run_folder'],"original_timestamp_data.h5py"))
    P['headings'] = L['gyro_heading_x'][:]
    P['encoders'] = L['encoder'][:]
    L.close()

cr(P['hide this!'])

parameter_file_load_timer = Timer(P['load_timer_time'])

def parameter_thread(P):
    while not P['ABORT']:
        time.sleep(0.1)
        load_parameters(P)

def load_parameters(P):
    if parameter_file_load_timer.check():
        Topics = menu2.load_Topics(opjk("scratch/VT"),first_load=False,customer='customer0')
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



def vec(heading,encoder):
	velocity = encoder * P['vel-encoding coeficient'] # rough guess
	a = [0,1]
	a = array(rotatePoint([0,0],a,heading))
	a *= velocity/30.0
	return array(a)



def f(x,A,B):
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
        v = vec(heading,encoder)
        D['xy'] += v # take into consideration reverse driving
        D['xys'].append(array(D['xy']))

        if len(D['xys']) < P['future_steps']+P['past_steps']:
            return False

        points = na(D['xys'])[-(P['future_steps']+P['past_steps']):]
        points -= points[P['past_steps'],:]
        points_to_fit = points[P['past_steps']-P['offset']:P['past_steps']+P['offset'],:]
        x = points_to_fit[:,0]
        y = points_to_fit[:,1]
        m,b = curve_fit(f,x,y)[0]
        ang = np.degrees(angle_between([0,1],[1,m]))

        rpoints = na(rotatePolygon(points,ang))

        rpoints *= -1

        D['rpoints'] = rpoints

        return True





    def _show2d():

        mci(P['O']['left_image']['vals'][D['index']-P['future_steps']],scale=P['cv2 scale'],delay=P['cv2 delay'],title='left camera')

        clf();plt_square();xylim(-P['l']/2,P['l']/2,-0.1,P['l'])

        pts_plot(D['rpoints'][:P['past_steps'],:],'k',sym=',')
        pts_plot(D['rpoints'][P['past_steps']:,:],'k',sym='x')

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

            b = Point3(a[0], 0, a[1]-P['backup parameter'])

            c = project(b, fit3d.mat)

            try:
                good = True
                if c.x < 0 or c.x >= 168:
                    good = False
                elif c.y < 0 or c.y >= 94:
                    good = False
                if good:
                    cv2.circle(img,(int(c.x),int(c.y)),r,(255,0,0))#int(np.max(1,5.0/np.sqrt(c.x**2+c.y**2))),255)
                    #cg(r)
                    #img[int(c.y),int(c.x),:] = na([255,0,0])
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







if __name__ == '__main__':

    CA()

    Raw_to_trajectory = Raw_to_Trajectory(P)

    while P['ABORT'] != True:
        if not Raw_to_trajectory['get']():
            continue
        if P['show 2D']:
            Raw_to_trajectory['show2d']()
        if P['show 3D']:
            Raw_to_trajectory['show3d']()
        if not Raw_to_trajectory['step']():
            break
        load_parameters(P)

    raw_enter()







#EOF
