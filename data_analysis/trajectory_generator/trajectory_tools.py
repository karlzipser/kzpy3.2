'''
Created on May 8, 2017

@author: Sascha Hornauer
'''

import numpy as np
from operator import mul, div, sub,mod, add
import cv2
import angles
import sys
try:
    from angles import normalize as normalize_angle # Adjust for different angles packages
except ImportError:
    from angles import normalize_angle #  Adjust for different angles packages

def get_heading(seq_xy):
    '''
    Give an average heading over all positions. Two different positions are 
    the minimum, more will return a smoothed angle
    '''

    diffsX = []
    diffsY = []

    # calculate the angle:
    for i in range(0,len(seq_xy)-1):
        diffsX.append(seq_xy[i+1][0]-seq_xy[i][0])
        diffsY.append(seq_xy[i+1][1]-seq_xy[i][1])
    
    myAngle = np.arctan2(diffsY, diffsX)
    
    return np.mean(myAngle)


def project_pos(xy,current_heading, distance=2):
    '''
    Take the position as xy and the current heading and returns future
    xy in a distance of distance
    '''
    
    x,y = cv2.polarToCart(distance,current_heading)
    
    return [x[0][0]+xy[0],y[0][0]+xy[1]]


def get_velocities(xy_positions,framerate):
    '''
    Returns the diffs in between two x,y positions divided by the
    framerate aka velocity in m/s since the distance in time between two
    positions is exactly that framerate
    '''
    
    velocities = []
    # First add 0 as a start
    velocities.append([0.0,0.0])
    
    for i in range(1,len(xy_positions)):
        x = xy_positions[i-1][0]
        y = xy_positions[i-1][1]
        x_t1 = xy_positions[i][0]
        y_t1 = xy_positions[i][1]
    
        sx = x_t1 - x
        sy = y_t1 - y
        
        vx = sx / framerate
        vy = sy / framerate
        velocities.append([vx,vy])
        
    
    return velocities

def distance_2d(point_a,point_b):
    return np.hypot(point_a[0]-point_b[0],point_a[1]-point_b[1])

def get_pos_diff(xy_positions):
    
    
    diffs = []
    # First add 0 as a start
    #diffs.append([0.0,0.0])
    
    for i in range(1,len(xy_positions)):
        x = xy_positions[i-1][0]
        y = xy_positions[i-1][1]
        x_t1 = xy_positions[i][0]
        y_t1 = xy_positions[i][1]
    
        sx = x_t1 - x
        sy = y_t1 - y
        
        vx = sx 
        vy = sy
        diffs.append([vx,vy])
        
    
    return diffs


def convert_delta_to_steer(delta_values):
    
    # delta values are assumed to be in +pi/2,-pi/2
    
    max_left_command = 100
    max_right_command = 0
    
    range = max_left_command-max_right_command
    
    steering_values=[]
    
    for values in delta_values:
        
        norm_values = map(div,values,[np.pi]*np.ones(len(values)))
        norm_values = map(add,norm_values,[0.5]*np.ones(len(values)))
        norm_values = map(mul,norm_values,[range]*np.ones(len(values)))
        norm_values = map(add,norm_values,[max_right_command]*np.ones(len(values)))
        
        
#         for value in values:
#             value = normalize_angle(value)
#             
#             range = max_left_command-max_right_command
#             value = normalize_angle(np.pi - value)/np.pi
#             value = value*range + max_right_command
#             norm_values.append(value)
#         
        steering_values.append(norm_values) 
        
    return steering_values

### Approach by Martin Thoma https://martin-thoma.com/author/martin-thoma/
class Point:
    """Represents a two dimensional point."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __get__(self, obj, cls=None):
        return obj

    def __repr__(self):
        return "P(%.2lf|%.2lf)" % (self.x, self.y)

    def __str__(self):
        return repr(self)
    
def to_point(xy):
    # Convenience method to convert an arbitrary tuple/array to a point
    return Point(xy[0],xy[1])

def distance_of_points(point_a, point_b):
    return distance_2d((point_a.x,point_a.y), (point_b.x,point_b.y))

def points_to_list(points):
    return_points = []
    
    if isinstance(points, list):
        for point in points:
            return_points.append((point.x,point.y))
    else:
        return_points = (points.x,points.y)
    return return_points

class Triangle:
    """Represents a triangle in R^2."""

    epsilon = 0.001

    def __init__(self, a, b, c):
        assert isinstance(a, Point)
        assert isinstance(b, Point)
        assert isinstance(c, Point)
        self.a = a
        self.b = b
        self.c = c

    def getArea(self):
        """Get area of this triangle.
           >>> Triangle(Point(0.,0.), Point(10.,0.), Point(10.,10.)).getArea()
           50.0
           >>> Triangle(Point(-10.,0.), Point(10.,0.), Point(10.,10.)).getArea()
           100.0
        """
        a, b, c = self.a, self.b, self.c
        return abs(a.x*(b.y-c.y)+b.x*(c.y-a.y)+c.x*(a.y-b.y))/2

    def isInside(self, p):
        """Check if p is inside this triangle."""
        assert isinstance(p, Point)
        currentArea = self.getArea()
        pab = Triangle(p,self.a, self.b)
        pac = Triangle(p,self.a, self.c)
        pbc = Triangle(p,self.b, self.c)
        newArea = pab.getArea()+pac.getArea()+pbc.getArea()
        return (abs(currentArea - newArea) < Triangle.epsilon)

if __name__ == '__main__':
    convert_delta_to_steer([ np.pi,  -1.41117611e-02,  -4.86447727e-02,
        -1.15039945e-01,  -1.91160306e-01,  -2.64138424e-01,
        -3.10457172e-01,  -3.1,  -4.04860318e-01,
        -3.88877490e-01,  -3.39034880e-01,  -2.62556928e-01,
        -1.86203485e-01,  -1.17426627e-01,  -8.51071829e-02,
        -5.16039439e-02,  -2.17969835e-02,   3.32755536e-15,
         5.53455382e-15,   1.62135104e-14])