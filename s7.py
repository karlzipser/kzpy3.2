###start
from kzpy3.vis3 import *
"""
https://stackoverflow.com/questions/76134/how-do-i-reverse-project-2d-points-into-3d
http://pyopengl.sourceforge.net/documentation/installation.html
"""

try:
    print len(encoders)
except:
    run_folder = '/media/karlzipser/preprocessed_5Oct2018_500GB/model_car_data_July2018_lrc/locations/local/left_right_center/h5py/Mr_Black_25Jul18_19h55m13s'
    cs("Loading L and O...")
    L = h5r(opjD(run_folder,"left_timestamp_metadata_right_ts.h5py"))
    O = h5r(opjD(run_folder,"original_timestamp_data.h5py"))
    headings = L['gyro_heading_x'][:]
    encoders = L['encoder'][:]








def vec(heading,encoder):
	velocity = encoder/2.3 # rough guess
	a = [0,1]
	a = array(rotatePoint([0,0],a,heading))
	a *= velocity/30.0
	return array(a)

from scipy.optimize import curve_fit

def f(x,A,B):
    return A*x + B

A,B = curve_fit(f,x,y)[0]




ang_prev = 0
fig1 = 99
figure(fig1)
clf()
plt_square()
l = 5.0
xy = array([0.0,0.0])
xys=[]
CA()
hz_timer = Timer(5)

cool_run_by_metal_bridge = 22000

if Truecool_run_by_metal_bridge    for i in range(22000,len(headings),1):
        heading = headings[i]
        encoder = encoders[i]
        v = vec(heading,encoder)
        xy += v # taken into consideration reverse driving
        xys.append(array(xy))
        graphics = False
        if np.mod(i,1) == 0:
            if len(xys) > 90+30:
                graphics = True
        if graphics:
            points = na(xys)[-120:]
            points -= points[30,:]
            points_to_fit = points[15:45,:]#na(xys)[-95:-90]
            x = points_to_fit[:,0]
            y = points_to_fit[:,1]
            m,b = curve_fit(f,x,y)[0]
            ang = np.degrees(angle_between([0,1],[1,m]))

            #print(int(ang))
            mci(O['left_image']['vals'][i-90],scale=2,delay=1,title='left camera')
            clf();plt_square();xylim(-l,l,-l,l)
            plot(0,1,'r.')
            plot(1,m,'r.')
            pts_plot(points[:30,:],'r',sym=',')
            pts_plot(points[30:,:],'r',sym=',')

            rpoints = na(rotatePolygon(points,ang))

            rpoints *= -1
            pts_plot(rpoints[:30,:],'k',sym=',')
            pts_plot(rpoints[30:,:],'k',sym='o')
            
            """
            points_to_fit = rpoints[30:45,:]#na(xys)[-95:-90]
            x = points_to_fit[:,0]
            y = points_to_fit[:,1]
            m,b = curve_fit(f,x,y)[0]
            ang2 = np.degrees(angle_between([0,1],[m,1]))
            
            rpoints2 = na(rotatePolygon(rpoints,-ang2/2))

            pts_plot(rpoints2[:30,:],'b',sym='.')
            pts_plot(rpoints2[30:,:],'b',sym='+')
            """
            d_ang = ang-ang_prev
            print(dp(ang),dp(d_ang),dp(ang2))
            #if np.abs(d_ang) > 1.5:
            #    raw_enter()
            ang_prev = ang
            spause()
        hz_timer.freq()














            """
            theta_ = angle_clockwise((0,1), (R[aruco_heading_x][vals][-1],R[aruco_heading_y][vals][-1]))
            xy_ = na([x_,y_])
            pts_pov_ = na(rotatePolygon(pts_-xy_,theta_))
            """

"""
use:

    grep -lr rotate * | xargs grep -lr heading

check out:

    ~/_kzpy3_older/kzpy_8Sept2018/Localization_app/localizer_listener.py

https://stackoverflow.com/questions/973473/getting-a-list-of-all-subdirectories-in-the-current-directory
"""


###stop







#EOF