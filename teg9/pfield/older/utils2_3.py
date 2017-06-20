from kzpy3.vis import *
import math


def rotatePoint(centerPoint,point,angle):
    """http://stackoverflow.com/questions/20023209/function-for-rotating-2d-objects
    Rotates a point around another centerPoint. Angle is in degrees.
    Rotation is counter-clockwise"""
    angle = math.radians(angle)
    temp_point = point[0]-centerPoint[0] , point[1]-centerPoint[1]
    temp_point = ( temp_point[0]*math.cos(angle)-temp_point[1]*math.sin(angle) , temp_point[0]*math.sin(angle)+temp_point[1]*math.cos(angle))
    temp_point = temp_point[0]+centerPoint[0] , temp_point[1]+centerPoint[1]
    return temp_point


import math
def rotatePolygon(polygon,theta):
    """http://stackoverflow.com/questions/20023209/function-for-rotating-2d-objects
    Rotates the given polygon which consists of corners represented as (x,y),
    around the ORIGIN, clock-wise, theta degrees"""
    theta = math.radians(theta)
    rotatedPolygon = []
    for corner in polygon :
        rotatedPolygon.append(( corner[0]*math.cos(theta)-corner[1]*math.sin(theta) , corner[0]*math.sin(theta)+corner[1]*math.cos(theta)) )
    return rotatedPolygon


def makeGaussian(size, fwhm = 3, center=None):
    """ Make a square gaussian kernel.

    size is the length of a side of the square
    fwhm is full-width-half-maximum, which
    can be thought of as an effective radius.
    http://stackoverflow.com/questions/7687679/how-to-generate-2d-gaussian-with-python

    """

    x = np.arange(0, size, 1, float)
    y = x[:,np.newaxis]

    if center is None:
        x0 = y0 = size // 2
    else:
        x0 = center[0]
        y0 = center[1]

    return np.exp(-4*np.log(2) * ((x-x0)**2 + (y-y0)**2) / fwhm**2)




def iadd(src,dst,xy,neg=False):
    src_size = []
    upper_corner = []
    lower_corner = []
    for i in [0,1]:
        src_size.append(shape(src)[i])
        upper_corner.append(int(xy[i]-src_size[i]/2.0))
        lower_corner.append(int(xy[i]+src_size[i]/2.0))
    if neg:
        dst[upper_corner[0]:lower_corner[0],upper_corner[1]:lower_corner[1]] -= src
    else:
        dst[upper_corner[0]:lower_corner[0],upper_corner[1]:lower_corner[1]] += src
    
def isub(src,dst,xy):
    iadd(src,dst,xy,neg=True)


from kzpy3.teg9.data.markers_clockwise import markers_clockwise
Origin = int(1000/300.*300)
Mult = 1000/300.*50
pfield = zeros((2*Origin,2*Origin))
marker_ids_all = []
marker_angles_dic = {}
marker_angles = 2*np.pi*np.arange(len(markers_clockwise))/(1.0*len(markers_clockwise))
marker_xys = []
for i in range(len(markers_clockwise)):
    a = marker_angles[i]
    marker_angles_dic[markers_clockwise[i]] = a
    x = 4*107/100.*np.sin(a)
    y = 4*107/100.*np.cos(a)
    marker_xys.append([x,y])
markers_xy_dic = {}
assert(len(markers_clockwise) == len(marker_xys))

def meters_to_pixels(x,y):
    return (int(-Mult*x)+Origin),(int(Mult*y)+Origin)

def meters_to_pixels(x,y):
    return (int(-Mult*x)+Origin),(int(Mult*y)+Origin)

pfield *= 0
gm = makeGaussian(3*Mult,1*Mult)
gc = makeGaussian(6*Mult,1.6*Mult)
gs = makeGaussian(0.8*Mult,0.24*Mult)
for j in range(len(markers_clockwise)):
    m = markers_clockwise[j]
    xy = marker_xys[j]
    markers_xy_dic[m] = xy
    xp,yp = meters_to_pixels(xy[0],xy[1])
    #print((xp,yp))
    iadd(gm,pfield,(xp,yp))
    iadd(5*gs,pfield,(xp,yp))
"""
for j in range(len(markers_clockwise)):
    m = markers_clockwise[j]
    xy = marker_xys[j]
    markers_xy_dic[m] = xy
    xp,yp = meters_to_pixels(0.8*xy[0],0.8*xy[1])
    isub(gm,pfield,(xp,yp))
    isub(5*gs,pfield,(xp,yp))
"""
for j in range(len(markers_clockwise)):
    m = markers_clockwise[j]
    xy = marker_xys[j]
    markers_xy_dic[m] = xy
    xp,yp = meters_to_pixels(0.75*xy[0],0.75*xy[1])
    #print((xp,yp))
    isub(gm,pfield,(xp,yp))
    #if j>31 and j<45:
    #    iadd(100*gs,pfield,(xp,yp))
    #else:
    #    isub(5*gs,pfield,(xp,yp))
iadd(2*gc,pfield,(Origin,Origin))
mi(pfield,'pfield')




def rotatePoint(centerPoint,point,angle):
    """http://stackoverflow.com/questions/20023209/function-for-rotating-2d-objects
    Rotates a point around another centerPoint. Angle is in degrees.
    Rotation is counter-clockwise"""
    angle = math.radians(angle)
    temp_point = point[0]-centerPoint[0] , point[1]-centerPoint[1]
    temp_point = ( temp_point[0]*math.cos(angle)-temp_point[1]*math.sin(angle) , temp_point[0]*math.sin(angle)+temp_point[1]*math.cos(angle))
    temp_point = temp_point[0]+centerPoint[0] , temp_point[1]+centerPoint[1]
    return temp_point







def sample_gradient(xy,xy_prev,angles,pfield,_):
    sample_points = []
    potential_values = []

    xy = array(xy)
    xy_forward = 2*xy - xy_prev

    for angle in angles:
        pt = rotatePoint(xy,xy_forward,angle)
        sample_points.append(pt)

    for sp in sample_points:
        pix = meters_to_pixels(sp[0],sp[1])
        potential_values.append(pfield[pix[0],pix[1]])

    return sample_points,potential_values






def get_trajectory(num_points,start_xy,xy_prev,angles,pfield,rand_proportion):

    pts = []

    xy = start_xy

    for i in range(num_points):

        sample_points,potential_values = sample_gradient(xy,xy_prev,angles,pfield,None)
        
        xy_prev = xy

        min_potential_index = potential_values.index(min(potential_values))

        
        if np.random.random() > rand_proportion:
            xy = sample_points[min_potential_index]
        else:
            xy = (array(sample_points[min_potential_index])+array(random.choice(sample_points)))/2.0
       # pt_plot(xy)

        pix = meters_to_pixels(xy[0],xy[1])
        #figure('pfield')


        pts.append(xy)

    return pts

            

def pt_plot(xy,color='r'):
    plot(xy[0],xy[1],color+'.')

def pts_plot(xys,color='r'):
    for xy in xys:
        pt_plot(xy,color)

def pts_meters_to_pixels(pts):
    pixs = []
    for xy in pts:
        pixs.append([int(-Mult*xy[0])+Origin,int(Mult*xy[1])+Origin])
    return pixs



figure('pfield')
clf()
mi(pfield)

def length(xy):
    return sqrt(xy[0]**2+xy[1]**2)

xy = np.random.rand(2)*3
xy_prev = [xy[0],xy[1]-0.1]
xy_start = array(xy).copy()
xy_start_prev = array(xy_prev).copy()
angles = (array([-2,-1,0,1,2])+0.0)*2.2
num_points = 10 #3
rand_proportion = 0.1

pts2 = []
for k in range(200):
    pts2.append(xy)
    #if mod(k,30) == 0:
    #    xy += 0.2*np.random.rand(2)-0.1
    if mod(k,2) == 0:
        pts = get_trajectory(num_points,xy,xy_prev,angles,pfield,rand_proportion)
        #pts_plot(pts_meters_to_pixels(pts))
        #pause(0.000001)

    v0 = xy-xy_prev
    v1 = (pts[-1]-xy)/length(pts[-1]-xy)*length(v0)
    xy_new = xy + (1*v0+9*v1)/10.0

    xy_prev = xy
    xy = xy_new
    
pts_plot(pts_meters_to_pixels(pts2),'b')

raw_input('enter to quit')

figure(2)
pts_plot(pts2,'b')
pt_plot(pts2[0],'r')

figure(1)
N = 10
M = 3
for i in range(0,len(pts2)-N,1):
    A = array(pts2[i:(i+N)])
    A = A - A[0]
    angs = []
    for j in range(1,M+1):
        angs.append(angle_between([0,1],A[j]))
    avg_ang = np.degrees(array(angs).mean())
    print (A[1],dp(avg_ang,2))
    if A[1][0] > 0:
        avg_ang *= -1.0
    B = rotatePolygon(A,-avg_ang)
    clf()
    pts_plot(B)
    xlim(-1,1);ylim(-1,1)
    pause(0.033)#raw_input('---')




"""
A = pts.copy()

pts_plot(A,'k');pause(0.1)

A = pts.copy()-pts[0]

C = A-A[-1]



np.degrees(angle_between([0,1],C[-2]))
139.90389468908447

D=rotatePolygon(C,140)

pts_plot(D);pause(1)

np.degrees(angle_between([0,1],C[-3]))


E=rotatePolygon(C,(139.9+142.1)/2.0)

pts_plot(E,'b');pause(1)

"""

None



