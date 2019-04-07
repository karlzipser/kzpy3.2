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

def project(p, mat):
    #print mat
    x = mat[0][0] * p.x + mat[0][1] * p.y + mat[0][2] * p.z + mat[0][3] * 1
    y = mat[1][0] * p.x + mat[1][1] * p.y + mat[1][2] * p.z + mat[1][3] * 1
    w = mat[3][0] * p.x + mat[3][1] * p.y + mat[3][2] * p.z + mat[3][3] * 1
    return Point2(168 * (x / w + 1) / 2., 94 - 94 * (y / w + 1) / 2.)

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
    










        
#EOF