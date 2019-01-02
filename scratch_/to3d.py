"""
https://stackoverflow.com/questions/76134/how-do-i-reverse-project-2d-points-into-3d
"""


class Point2:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Point3:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

# Known 2D coordinates of our rectangle
i0 = Point2(318, 247)
i1 = Point2(326, 312)
i2 = Point2(418, 241)
i3 = Point2(452, 303)

# 3D coordinates corresponding to i0, i1, i2, i3
r0 = Point3(0, 0, 0)
r1 = Point3(0, 0, 1)
r2 = Point3(1, 0, 0)
r3 = Point3(1, 0, 1)

mat = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
]

def project(p, mat):
    x = mat[0][0] * p.x + mat[0][1] * p.y + mat[0][2] * p.z + mat[0][3] * 1
    y = mat[1][0] * p.x + mat[1][1] * p.y + mat[1][2] * p.z + mat[1][3] * 1
    w = mat[3][0] * p.x + mat[3][1] * p.y + mat[3][2] * p.z + mat[3][3] * 1
    return Point(720 * (x / w + 1) / 2., 576 - 576 * (y / w + 1) / 2.)


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

def perturb(amount):
    from copy import deepcopy
    from random import randrange, uniform
    mat2 = deepcopy(mat)
    mat2[randrange(4)][randrange(4)] += uniform(-amount, amount)


def approximate(mat, amount, n=100000):
    est = evaluate(mat)

    for i in xrange(n):
        mat2 = perturb(mat, amount)
        est2 = evaluate(mat2)
        if est2 < est:
            mat = mat2
            est = est2

    return mat, est


for i in xrange(100):
    mat = approximate(mat, 1)
    mat = approximate(mat, .1)




    [1.0836000765696232,  0,  0.16272110011060575, -0.44811064935115597],
    [0.09339193527789781, 1, -0.7990570384334473,   0.539087345090207  ],
    [0,                   0,  1,                    0                  ],
    [0.06700844759602216, 0, -0.8333379578853196,   3.875290562060915  ],
]


