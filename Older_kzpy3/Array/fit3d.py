from kzpy3.vis3 import *
exec(identify_file_str)
"""
https://stackoverflow.com/questions/76134/how-do-i-reverse-project-2d-points-into-3d
http://pyopengl.sourceforge.net/documentation/installation.html
"""

#import pandas as pd
#import numpy as np

class Point2:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Point3:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

if False:
    # Known 2D coordinates of our rectangle
    i0 = Point2(318, 247)
    i1 = Point2(326, 312)
    i2 = Point2(418, 241)
    i3 = Point2(452, 303)

i0 = Point2(58,80)
i1 = Point2(66,68)
i2 = Point2(98,68)
i3 = Point2(110,80)


# 33.5 cm

half = 33.5/100.0/2.0

# 3D coordinates corresponding to i0, i1, i2, i3
r0 = Point3(-half, 0, -half)
r1 = Point3(-half, 0, half)
r2 = Point3(half, 0, half)
r3 = Point3(half, 0, -half)

mat = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
]

def project(
    p,
    mat,
    height_in_pixels=94,
    width_in_pixels=168,
):
    #print mat
    x = mat[0][0] * p.x + mat[0][1] * p.y + mat[0][2] * p.z + mat[0][3] * 1
    y = mat[1][0] * p.x + mat[1][1] * p.y + mat[1][2] * p.z + mat[1][3] * 1
    w = mat[3][0] * p.x + mat[3][1] * p.y + mat[3][2] * p.z + mat[3][3] * 1
    return Point2(width_in_pixels * (x / w + 1) / 2., height_in_pixels - height_in_pixels * (y / w + 1) / 2.)

# The squared distance between two points a and b
def norm2(a, b):
    dx = b.x - a.x
    dy = b.y - a.y
    return dx * dx + dy * dy

def evaluate(mat): 
    c0 = project(r0, mat)
    c1 = project(r1, mat)
    c2 = project(r2, mat)
    c3 = project(r3, mat)
    return norm2(i0, c0) + norm2(i1, c1) + norm2(i2, c2) + norm2(i3, c3)    

def perturb(mat, amount):
    from copy import deepcopy
    from random import randrange, uniform
    mat2 = deepcopy(mat)
    mat2[randrange(4)][randrange(4)] += uniform(-amount, amount)
    return mat2

def approximate(mat, amount, n=1000):
    est = evaluate(mat)
    for i in xrange(n):
        mat2 = perturb(mat, amount)
        est2 = evaluate(mat2)
        if est2 < est:
            mat = mat2
            est = est2

    return mat, est


if __name__ == '__main__':

    for i in xrange(100000):
        mat,est = approximate(mat, 1)
        if np.mod(i,50) == 0:
            print mat
            print est

else:
    mat = [[1.1038363893132925, 0, -0.06913056289047548, -0.011453007708049912],
         [-0.0015083235462127753, 1, -0.04276381228842596, -0.4265748298235925],
         [0, 0, 1, 0],
         [0.002382129088680296, 0, 1.114622282258332, 0.7840441986828541]]
    





def pt_in_2D_to_image(x_meters,y_meters):
    b = Point3(x_meters,0,y_meters)
    c = project(b, mat)
    return c.x,c.y

def pt_in_2D_to_image_with_disparity(
    x_meters,
    y_meters,
    m_disparity=0.47885706 ,# from Mr. Blue
    b_disparity=-21.76993126
):
    b_ = Point3(x_meters,0,y_meters)
    c = project(b_, mat)
    disparity = max(0,c.y*m_disparity+b_disparity)
    return c.x,c.y,disparity

def width_at_y(
    w,
    y,
    m_width = 4.97,
    b_width = -242.
):
    return max(0.,w*(m_width*y + b_width))

def pt_in_2D_to_image_with_disparity_and_width(
    x_meters,
    y_meters,
    width_meters,
    backup_parameter=1.
):
    x,y,disparity = pt_in_2D_to_image_with_disparity(x_meters,y_meters-backup_parameter)
    width = width_at_y(width_meters,y)
    return x,y,disparity,width


def point_in_3D_to_point_in_2D(
    a,
    backup_parameter=1.0,
    height_in_pixels=94,
    width_in_pixels=168,
):
    if a[1]<0:
        return False,False

    b = Point3(a[0], 0, a[1] - backup_parameter)
    c = project(b,mat,height_in_pixels,width_in_pixels)

    if c.x < 0 or c.x >= width_in_pixels:
        return False,False

    elif c.y < 0 or c.y >= height_in_pixels:
        return False,False

    return c.x,c.y





        
#EOF