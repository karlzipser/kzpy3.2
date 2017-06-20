from kzpy3.vis import *
import math







from kzpy3.teg9.data.markers_clockwise import markers_clockwise
Origin = int(1000/300.*300)
Mult = 1000/300.*50
pfield = zeros((2*Origin,2*Origin))
marker_ids_all = []
marker_angles_dic = {}
marker_angles = 2*np.pi*np.arange(len(markers_clockwise))/(1.0*len(markers_clockwise))
marker_xys = {}
for r in [4.0,4.2,4.4]:
    marker_xys[r] = []
    for i in range(len(markers_clockwise)):
        a = marker_angles[i]
        marker_angles_dic[markers_clockwise[i]] = a
        x = r*107/100.*np.sin(a)
        y = r*107/100.*np.cos(a)
        marker_xys[r].append([x,y])


pfield *= 0
gm = makeGaussian(3*Mult,1*Mult)
gc = makeGaussian(6*Mult,1.6*Mult)
gs = makeGaussian(0.8*Mult,0.24*Mult)
gcar = makeGaussian(4*Mult,4/3.*Mult)
for j in range(len(markers_clockwise)):
    m = markers_clockwise[j]
    xy = marker_xys[4.0][j]
    markers_xy_dic[m] = xy
    xp,yp = meters_to_pixels(xy[0],xy[1])
    iadd(gm,pfield,(xp,yp))
    iadd(5*gs,pfield,(xp,yp))

    #iadd(5*gs,pfield,(xp,yp))
for j in range(len(markers_clockwise)):
    m = markers_clockwise[j]
    xy = marker_xys[4.0][j]
    markers_xy_dic[m] = xy
    xp,yp = meters_to_pixels(0.75*xy[0],0.75*xy[1])
    isub(gm,pfield,(xp,yp))
iadd(4*gc,pfield,(Origin,Origin))


pfield -= pfield.min()
pfield /= pfield.max()


for x in range(2*Origin):
    for y in range(2*Origin):
        if sqrt((x - Origin)**2+(y - Origin)**2) > 720:
            pfield[x,y] = 1

mi(pfield,'pfield')
figure(3);plot(pfield[:,Origin])







N = lo(opjD('N.pkl'))
traj = N['Mr_Black']['direct_rewrite_test_28Apr17_17h23m15s_Mr_Black']['self_trajectory']

def rotatePoint(centerPoint,point,angle):
    """http://stackoverflow.com/questions/20023209/function-for-rotating-2d-objects
    Rotates a point around another centerPoint. Angle is in degrees.
    Rotation is counter-clockwise"""
    angle = math.radians(angle)
    temp_point = point[0]-centerPoint[0] , point[1]-centerPoint[1]
    temp_point = ( temp_point[0]*math.cos(angle)-temp_point[1]*math.sin(angle) , temp_point[0]*math.sin(angle)+temp_point[1]*math.cos(angle))
    temp_point = temp_point[0]+centerPoint[0] , temp_point[1]+centerPoint[1]
    return temp_point








def sample_gradient(xy,xy_prev,angles,pfield):

    sample_points = []
    potential_values = []

    delta_xy = xy - array(xy_prev)

    xy = array(xy)
    xy_forward = xy + delta_xy

    for angle in angles:
        pt = rotatePoint(xy,xy_forward,angle)
        sample_points.append(pt)

    for sp in sample_points:
        pix = meters_to_pixels(sp[0],sp[1])
        potential_values.append(pfield[pix[0],pix[1]])

    return sample_points,potential_values



from scipy.optimize import curve_fit

def f(x,A,B):
    return A*x+B



def xylim(a,b,c,d):
    xlim(a,b)
    ylim(c,d)
"""
def sqfig(a,b):
    figure(1,figsize=b)
    xylim(0,a,0,a)
"""

def normalized(a, axis=-1, order=2):
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2==0] = 1
    return a / np.expand_dims(l2, axis)


def normalized_vector_from_pts(pts):
    x = pts[:,0]
    y = pts[:,1]
    m,b = curve_fit(f,x,y)[0]
    heading = normalized([1,m])[0]
    return heading




Pts = zeros( (len(traj['left']['x']),2) )
Pts[:,0] = traj['left']['x']
Pts[:,1] = traj['left']['y']

pts = Pts.copy()

def get_sample_points(pts,angles,n=3):

    sample_points = []
    potential_values = []

    heading = normalized_vector_from_pts(pts[-n:,:])
    heading *= 0.5 # 50 cm, about the length of the car
    if pts[-n,0] > pts[-1,0]:
        heading *= -1
    #if pts[-3,1] > pts[-1,1]:
    #    heading *= -1

    for a in angles:

        sample_points.append( rotatePoint([0,0],heading,a) )
    #figure(3)
    #pts_plot(pts)
    for k in range(len(sample_points)):
        f = sample_points[k]
        #plot([pts[-1,0],pts[-1,0]+f[0]],[pts[-1,1],pts[-1,1]+f[1]])
    #figure(1)
    for sp in sample_points:
        pix = meters_to_pixels(sp[0]+pts[-1,0],sp[1]+pts[-1,1])
        #plot(pix[0],pix[1],'kx')
        potential_values.append(pfield[pix[0],pix[1]])

    return sample_points,potential_values





angles = range(-30,31,10)
angles = -1*array(angles)
pix_prev = [Origin,Origin]
mi(pfield,1)
xylim(-4,4,-4,4)
figure(2)
clf()
#xylim(0,7,1.5,1.57)
ctr = 0
for i in range(5000,len(pts),3):
    if traj['left']['t_vel'][i] > 0.4:
        pt = pts[i]
        pix = meters_to_pixels(pt[0],pt[1])
        sample_points,potential_values = get_sample_points(pts[i:i+6],angles,6)
        sp = sample_points[0]
        sp_pix = meters_to_pixels(sp[0]+pt[0],sp[1]+pt[1])
        if ctr ==0 or ctr > 5:
            figure(1)
            mi(pfield,img_title=d2s(i))
            if ctr > 0:
                isub(gcar,pfield,(pix_prev[0],pix_prev[1]))
            iadd(gcar,pfield,(pix[0],pix[1]))
            pix_prev = array(pix).copy()
            figure(2)
            clf()
            xylim(-0.1,6.1,-0.1,1.1)
            ctr = 0
        figure(1)
        plot(pix[0],pix[1],'r.')
        plot(sp_pix[0],sp_pix[1],'g.')
        figure(2)
        plot(potential_values,'r.-')
        ctr += 1
        
        pause(0.1)
        #raw_input("dafds")#pause(0.03)

