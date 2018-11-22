from kzpy3.vis3 import *

import pandas as pd
import numpy as np

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




for i in xrange(100000):
    mat,est = approximate(mat, 1)
    if np.mod(i,50) == 0:
        print mat
        print est



if False:
    mat = [ [1.103618771460224, 0, -0.0701799535550891, -0.010607765731461827],
            [-0.013683406981532142, 1, -0.043465873204453276, -0.42658901116635217],
            [0, 0, 1, 0],
            [0.021482728110305827, 0, 1.1158981482417645, 0.784109020955855]
    ]
"""

"""

"""
33.5 cm 

107,81
55,80
66,68
97,67


y = 80,68
x = 58 -- 110

(58,80)
(110,80) 
(66,68)
(98,68)
"""







        
#EOF