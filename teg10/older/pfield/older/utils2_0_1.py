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
    sense_points = []
    sample_points = []
    potential_values = []
    xy = array(xy)
    delta_xy = xy - array(xy_prev)
    xy_sense_forward = xy + 2*delta_xy
    xy_forward = xy + delta_xy
    #xy_forward = 2*xy - xy_prev

    for angle in angles:
        pt = rotatePoint(xy,xy_forward,angle)
        sense_pt = rotatePoint(xy,xy_sense_forward,10*angle)
        sample_points.append(pt)
        sense_points.append(sense_pt)

    for sp in sense_points:
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
        a = 1
        b = 0
        xy = a*array(xy) + b*array(sample_points[len(sample_points)/2])
        pix = meters_to_pixels(xy[0],xy[1])
        #figure('pfield')
        plot(pix[0],pix[1],'r.')
        pause(0.000001)
        if length(xy) > 4.5:
            return
        pts.append(xy)

    return pts

            

def pt_plot(xy):
    plot(xy[0],xy[1],'r.')

def pts_plot(xys):
    for xy in xys:
        pt_plot(xy)



CA()
figure('pfield')
mi(pfield)



angles = array([-2,-1,0,1,2])*3.0
num_points = 200
rand_proportion = 0.2






for tr in range(10):
    xy = np.random.rand(2)*4-2.0
    xy_prev = [xy[0],xy[1]-0.1]
    xy_start = array(xy).copy()
    xy_start_prev = array(xy_prev).copy()

    pts = get_trajectory(num_points,xy,xy_prev,angles,pfield,rand_proportion)

"""
dsteer max = ~ 25 control units
max turn in 0.5s ~= 28 degrees
"""