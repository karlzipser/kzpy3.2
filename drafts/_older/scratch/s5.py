from kzpy3.vis3 import *
"""
https://stackoverflow.com/questions/76134/how-do-i-reverse-project-2d-points-into-3d
http://pyopengl.sourceforge.net/documentation/installation.html
"""

L = h5r(opjD("model_car_data_July2018_lrc/locations/local/left_right_center/h5py/Mr_Black_25Jul18_19h55m13s/left_timestamp_metadata_right_ts.h5py"))
O = h5r(opjD("model_car_data_July2018_lrc/locations/local/left_right_center/h5py/Mr_Black_25Jul18_19h55m13s/original_timestamp_data.h5py"))

headings = L['gyro_heading_x'][:]

encoders = L['encoder'][:]






def angle_between(v1, v2):
    """http://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python
    Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))



def rotatePoint(centerPoint,point,angle):
    """http://stackoverflow.com/questions/20023209/function-for-rotating-2d-objects
    Rotates a point around another centerPoint. Angle is in degrees.
    Rotation is counter-clockwise"""
    angle = math.radians(angle)
    temp_point = point[0]-centerPoint[0] , point[1]-centerPoint[1]
    temp_point = ( temp_point[0]*math.cos(angle)-temp_point[1]*math.sin(angle) , temp_point[0]*math.sin(angle)+temp_point[1]*math.cos(angle))
    temp_point = temp_point[0]+centerPoint[0] , temp_point[1]+centerPoint[1]
    return temp_point



def rotatePolygon(polygon,theta):
    """http://stackoverflow.com/questions/20023209/function-for-rotating-2d-objects
    Rotates the given polygon which consists of corners represented as (x,y),
    around the ORIGIN, clock-wise, theta degrees"""
    theta = math.radians(theta)
    rotatedPolygon = []
    for corner in polygon :
        rotatedPolygon.append(( corner[0]*math.cos(theta)-corner[1]*math.sin(theta) , corner[0]*math.sin(theta)+corner[1]*math.cos(theta)) )
    return rotatedPolygon



def vec(heading,encoder):
	velocity = encoder/2.3 # rough guess
	a = [0,1]
	a = array(rotatePoint([0,0],a,heading))
	a *= velocity/30.0
	return array(a)
###start
figure(99);clf()
plt_square();
l = 1
xylim(-l,l,-l,l)
xy = array([0.0,0.0])
xys=[]
CA()
if True:
	for i in range(9000,len(headings),4):
		#plot(xy[0],xy[1],'r.')
		heading = headings[i]#data['gyro_heading'][i][0]
		encoder = encoders[i]#data['encoder'][i]
		v = vec(heading,encoder)
		xy += v
		xys.append(array(xy))
		#print i#(heading,encoder,v)
		#pause(0.0001)
		if len(xys) >99:
			#mag = np.sqrt(xys[-28][0]**2+xys[-28][0]**2)
			alpha = angle_between(na((0,1)),na(xys[-28])-na(xys[-30]))
			xl = xys[-30][0];yl = xys[-30][1]
			figure(99);clf();xylim(-l+xl,l+xl,-l+yl,l+yl);plt_square();
			xys_rot = rotatePolygon(xys[-30:]-xys[-30],alpha)
			pts_plot(array(xys_rot[-30:]),sym=',')
			pt_plot(array(xys_rot[-30]),color='b')
			mci(O['left_image']['vals'][i-30],scale=2,delay=1)#,'left camera')
			spause()
			print i
###stop


if False:
    for i in range(100):
        clear_screen()
        teams_list = ["Man Utd", "Man City", "T Hotspur"]
        data = np.random.rand(3,3)

        row_format ="{:>15}" * (len(teams_list) + 1)
        print row_format.format("", *teams_list)

        for team, row in zip(teams_list, data):
            print row_format.format(team, *row)
        time.sleep(.1)


    for i in range(100):
        unix("cd /anaconda/bin/; play  -n synth 60 brownnoise vol 1 &")

    CA()
    random_steer = 49
    random_steer_lst = []
    for i in range(10000):
        random_steer = np.random.randint(20,80)#-5)
        random_steer = bound_value(random_steer,0,99)
        random_steer_lst.append(random_steer)
    from kzpy3.vis3 import *
    hist(random_steer_lst)

import pyaudio
BITRATE = 16000     #number of frames per second/frameset.      

FREQUENCY = 500     #Hz, waves per second, 261.63=C4-note.
LENGTH = 0.1     #seconds to play sound

if FREQUENCY > BITRATE:
    BITRATE = FREQUENCY+100

NUMBEROFFRAMES = int(BITRATE * LENGTH)
RESTFRAMES = NUMBEROFFRAMES % BITRATE
WAVEDATA = ''    

#generating wawes
for x in xrange(NUMBEROFFRAMES):
 WAVEDATA = WAVEDATA+chr(int(math.sin(x/((BITRATE/FREQUENCY)/math.pi))*127+128))    

#for x in xrange(RESTFRAMES): 
# WAVEDATA = WAVEDATA+chr(128)

p = pyaudio.PyAudio()
stream = p.open(format = p.get_format_from_width(1), 
                channels = 1, 
                rate = BITRATE, 
                output = True)
for i in range(100):
    stream.write(WAVEDATA)
    #time.sleep(1)
    stream.write(WAVEDATA)
stream.stop_stream()
stream.close()
p.terminate()









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
    return Point2(720 * (x / w + 1) / 2., 576 - 576 * (y / w + 1) / 2.)

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





mat2 = [[0.15163146912369507, 0, 0.022787948887946996, -0.0630522260786488], 
    [0.012821569298570035, 1, -0.11243586155538199, 0.07691266199588864], 
    [0, 0, 1, 0], 
    [0.00943572978581031, 0, -0.1140523851998616, 0.5403884387524513]]


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