###start
from kzpy3.vis3 import *
import kzpy3.Menu_app.menu2 as menu2
import kzpy3.scratch.VT.default_values as default_values

P = default_values.P

os.system(d2n("gnome-terminal -x python kzpy3/Menu_app/menu2.py path ","kzpy3/scratch/Vis_Traj"," dic P"))




"""
https://stackoverflow.com/questions/76134/how-do-i-reverse-project-2d-points-into-3d
http://pyopengl.sourceforge.net/documentation/installation.html
"""

if 'encoders' not in P:
    run_folder = '/media/karlzipser/preprocessed_5Oct2018_500GB/model_car_data_July2018_lrc/locations/local/left_right_center/h5py/Mr_Black_25Jul18_19h55m13s'
    cs("Loading L and O...")
    L = h5r(opjD(run_folder,"left_timestamp_metadata_right_ts.h5py"))
    P['O'] = h5r(opjD(run_folder,"original_timestamp_data.h5py"))
    P['headings'] = L['gyro_heading_x'][:]
    P['encoders'] = L['encoder'][:]


parameter_file_load_timer = Timer(2)

def parameter_thread(P):
    while not P['ABORT']:
        time.sleep(0.1)
        load_parameters(P)

def load_parameters(P):      
        if parameter_file_load_timer.check():
            Topics = menu2.load_Topics(opjk("scratch/Vis_Traj"),first_load=False,customer='customer0')
            if type(Topics) == dict:
                for t in Topics['To Expose']['customer0']:
                    if t in Arguments:
                        topic_warning(t)
                    if '!' in t:
                        pass
                    else:
                        P[t] = Topics[t]
            parameter_file_load_timer.reset()

#threading.Thread(target=parameter_thread,args=[P]).start()



def vec(heading,encoder):
	velocity = encoder/2.3 # rough guess
	a = [0,1]
	a = array(rotatePoint([0,0],a,heading))
	a *= velocity/30.0
	return array(a)

from scipy.optimize import curve_fit

def f(x,A,B):
    return A*x + B

#A,B = curve_fit(f,x,y)[0]






figure(P['fig'])
clf()
plt_square()


CA()
timer = Timer(5)





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

        mci(P['O']['left_image']['vals'][D['index']-P['future_steps']],scale=2,delay=1,title='left camera')

        clf();plt_square();xylim(-P['l']/2,P['l']/2,-0.1,P['l'])

        pts_plot(D['rpoints'][:P['past_steps'],:],'k',sym=',')
        pts_plot(D['rpoints'][P['past_steps']:,:],'k',sym='x')

        spause()

        timer.freq()


    D['step'] = _step
    D['get'] = _get
    D['show2d'] = _show2d
    return D
#
################################################################################################







    



Raw_to_trajectory = Raw_to_Trajectory(P)

while P['ABORT'] != True:
    if not Raw_to_trajectory['get']():
        continue
    Raw_to_trajectory['show2d']()
    if not Raw_to_trajectory['step']():
        break
    load_parameters(P)

raw_enter()







#EOF
