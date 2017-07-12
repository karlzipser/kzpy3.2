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

        sample_points,potential_values = sample_gradient(xy,xy_prev,angles,pfield,_)
        
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


CA()
figure('pfield')
mi(pfield)

def length(xy):
    return sqrt(xy[0]**2+xy[1]**2)

xy = np.random.rand(2)*3
xy_prev = [xy[0],xy[1]-0.1]
xy_start = array(xy).copy()
xy_start_prev = array(xy_prev).copy()
angles = (array([-2,-1,0,1,2])+0.0)*2.5
num_points = 10 #3
rand_proportion = 0.1

pts2 = []
for k in range(300):
    pts2.append(xy)

    if mod(k,2) == 0:
        pts = get_trajectory(num_points,xy,xy_prev,angles,pfield,rand_proportion)
        #pts_plot(pts_meters_to_pixels(pts))
        #pause(0.000001)

    v0 = xy-xy_prev
    v1 = (pts[-1]-xy)/length(pts[-1]-xy)*length(v0)
    xy_new = xy + (3*v0+7*v1)/10.0

    xy_prev = xy
    xy = xy_new
    
pts_plot(pts_meters_to_pixels(pts2),'b')