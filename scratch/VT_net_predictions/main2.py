###start
from kzpy3.vis3 import *
from scipy.optimize import curve_fit
import kzpy3.Menu_app.menu2 as menu2
import kzpy3.scratch.VT_net_predictions.default_values as default_values
import kzpy3.scratch.VT_net_predictions.fit3d as fit3d
P = default_values.P
Point3 = fit3d.Point3
project = fit3d.project

if P['start menu automatically']:
    os.system(d2n("gnome-terminal -x python kzpy3/Menu_app/menu2.py path ","kzpy3/scratch/VT_net_predictions"," dic P"))




"""
https://stackoverflow.com/questions/76134/how-do-i-reverse-project-2d-points-into-3d
http://pyopengl.sourceforge.net/documentation/installation.html
"""



parameter_file_load_timer = Timer(P['load_timer_time'])



def load_parameters(P):
    if parameter_file_load_timer.check():
        Topics = menu2.load_Topics(opjk("scratch/VT_net_predictions"),first_load=False,customer='customer0')
        if type(Topics) == dict:
            for t in Topics['To Expose']['customer0']:
                if t in Arguments:
                    topic_warning(t)
                if '!' in t:
                    pass
                else:
                    P[t] = Topics[t]
        parameter_file_load_timer.reset()



def vec(heading,encoder,sample_frequency=30.0):
	velocity = encoder * P['vel-encoding coeficient'] # rough guess
	a = [0,1]
	a = array(rotatePoint([0,0],a,heading))
	a *= velocity/sample_frequency
	return array(a)


def f(x,A,B):
    return A*x + B


U = lo( opjD('16Nov2018_held_out_data/net_predictions.tegra-ubuntu_16Nov18_17h44m50s.pkl' ))
O = h5r(opjD('16Nov2018_held_out_data/h5py/tegra-ubuntu_16Nov18_17h44m50s/original_timestamp_data.h5py' ))




Colors = {'direct':'k','left':'b','right':'r'}

def get_r_points(index,behavioral_mode,headings,encoders):
    xy = array([0.0,0.0])
    xys = []

    for i in range(len(headings)):
        v = vec(headings[i],encoders[i],10.0)
        xy += v # take into consideration reverse driving
        #cr(xy)
        xys.append(xy.copy())

    points_to_fit = na(xys[:3])
    x = points_to_fit[:,0]
    y = points_to_fit[:,1]
    m,b = curve_fit(f,x,y)[0]
    ang = np.degrees(angle_between([0,1],[1,m]))

    rpoints = na(xys)#na(rotatePolygon(xys,ang))

    #rpoints *= -1
    return rpoints




def show2d(rpoints,color):

    #mci(O['left_image']['vals'][],scale=P['cv2 scale'],delay=P['cv2 delay'],title='left camera')

    

    pts_plot(rpoints,color=color,sym='.')

    

    P['timer'].freq()




for index in range(15000,16000):
    clf();plt_square();xylim(-P['l']/2,P['l']/2,-P['l']/2,P['l']/2)
    for behavioral_mode in ['left','direct','right']:
        headings = U[behavioral_mode][index]['heading']
        encoders = U[behavioral_mode][index]['encoder']
        rpoints = get_r_points(index,behavioral_mode,headings,encoders)
        show2d(rpoints,Colors[behavioral_mode])
    spause()









###################################

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
