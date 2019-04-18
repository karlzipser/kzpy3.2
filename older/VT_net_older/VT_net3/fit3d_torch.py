from kzpy3.vis3 import *
exec(identify_file_str)
"""
https://stackoverflow.com/questions/76134/how-do-i-reverse-project-2d-points-into-3d
http://pyopengl.sourceforge.net/documentation/installation.html
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


def project(p, mat):
    x = mat[0][0] * p.x + mat[0][1] * p.y + mat[0][2] * p.z + mat[0][3] * 1
    y = mat[1][0] * p.x + mat[1][1] * p.y + mat[1][2] * p.z + mat[1][3] * 1
    w = mat[3][0] * p.x + mat[3][1] * p.y + mat[3][2] * p.z + mat[3][3] * 1
    return Point2(168 * (x / w + 1) / 2., 94 - 94 * (y / w + 1) / 2.)

mat4 = [[1.1038363893132925, 0, -0.06913056289047548, -0.011453007708049912],
     [-0.0015083235462127753, 1, -0.04276381228842596, -0.4265748298235925],
     [0, 0, 1, 0],
     [0.002382129088680296, 0, 1.114622282258332, 0.7840441986828541]]
    
mat = [
    [1.1038363893132925, 0, -0.06913056289047548, -0.011453007708049912],
    [-0.0015083235462127753, 1, -0.04276381228842596, -0.4265748298235925],
    [0.002382129088680296, 0, 1.114622282258332, 0.7840441986828541]]
 









        
#EOF