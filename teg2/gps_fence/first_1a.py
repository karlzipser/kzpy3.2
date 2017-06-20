
from kzpy3.vis import *
# run "kzpy3/teg2/gps_fence/first.py"

from math import acos
from math import sqrt
from math import pi

def length(v):
    return sqrt(v[0]**2+v[1]**2)
def dot_product(v,w):
   return v[0]*w[0]+v[1]*w[1]
def determinant(v,w):
   return v[0]*w[1]-v[1]*w[0]
def inner_angle(v,w):
   cosx=dot_product(v,w)/(length(v)*length(w))
   rad=acos(cosx) # in radians
   return rad*180/pi # returns degrees
def angle_clockwise(A, B):
    inner=inner_angle(A,B)
    det = determinant(A,B)
    if det<0: #this is a property of the det. If the det < 0 then B is clockwise of A
        return inner
    else: # if the det > 0 then A is immediately clockwise of B
        return 360-inner

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


def rotatePoint(centerPoint,point,angle):
    """http://stackoverflow.com/questions/20023209/function-for-rotating-2d-objects
    Rotates a point around another centerPoint. Angle is in degrees.
    Rotation is counter-clockwise"""
    angle = math.radians(angle)
    temp_point = point[0]-centerPoint[0] , point[1]-centerPoint[1]
    temp_point = ( temp_point[0]*math.cos(angle)-temp_point[1]*math.sin(angle) , temp_point[0]*math.sin(angle)+temp_point[1]*math.cos(angle))
    temp_point = temp_point[0]+centerPoint[0] , temp_point[1]+centerPoint[1]
    return temp_point

"""
my_polygon = [(0,0),(1,0),(0,1)]
print rotatePolygon(my_polygon,90)
print rotatePoint((1,1),(2,2),45)
"""


def distance(my_position,object_position):
	dist = np.sqrt((my_position[0]-object_position[0])**2+(my_position[1]-object_position[1])**2)
	return dist

def force_function(my_position,object_position):
	dist = distance(my_position,object_position)
	if dist < 0.2:
		f = 2.0/((0.01*dist)**4)#1/(dist+0.01)
	elif dist < 2:
		f = 1.0/((0.01*dist)**4)
	else:
		f = 0.0
	vec = na(my_position) - na(object_position)
	vec *= f
	return vec

def force_function2(my_position,object_position):
	dist = distance(my_position,object_position)
	f = -5*dist
	vec = na(my_position) - na(object_position)
	vec *= f
	return vec

my_position = (np.random.random(2)-0.5)/4.0

pts = []

r = 1.0
for a in range(0,360,5):
	x = r*np.sin(np.deg2rad(a))
	y = r*np.cos(np.deg2rad(a))
	pts.append([x,y])
"""
for i in range(200):
	a = np.random.random()
	p = 2*np.random.random(2) - 1
	if distance(p,(0,0))>a**0.1:
		pts.append(p)
		if len(pts) > 150:
			break
"""
for i in range(10):
	p = 2*np.random.random(2) - 1
	pts.append(p)

pts = na(pts)
vec_total_prev = na((0,0))
my_position_prev = na((0,0))
GO_UP = True

while distance(my_position,(0,0)) < 3:

	vec_total = na([0.0,0.0])
	for i in range(1,len(pts)):
		vec_total += 0.01 * force_function((my_position[0],my_position[1]),pts[i,:])
		pass

	vec_total += 0.01 * force_function2((my_position[0],my_position[1]),pts[0,:])

	vec_total_copy = vec_total.copy()
	#print vec_total,vec_total_prev

	while inner_angle(vec_total,vec_total_prev) > 5:
		#print inner_angle(vec_total,vec_total_prev)
		vec_total = 0.1*vec_total + 0.9*vec_total_prev
	print inner_angle(vec_total,vec_total_prev)
	vec_total += 0.03*np.random.random(2)

	"""
	if distance(my_position,(1,1))>0.2 and GO_UP:
		vec_total +=25*na((1,1))
	elif distance(my_position,(1,1))<0.2 and GO_UP:
		GO_UP = False
		vec_total +=25*na((-1,-1))
	elif distance(my_position,(-1,-1))>0.2 and not GO_UP:
		vec_total +=25*na((-1,-1))
	else:
		GO_UP = True
		vec_total +=25*na((1,1))
	"""
	d = distance(my_position,[0,0])
	if d > 0.75:
		q = 0.01
	else:
		q = 0.01
	#my_position += 1.0/distance(vec_total,(0,0)) * vec_total * q
	my_position += 1.0/distance(vec_total,(0,0)) * vec_total * q
	#if distance(my_position_prev,my_position) < q:
	#	my_position+=1.0/distance(vec_total_prev,(0,0)) * vec_total_prev * q
	vec_total_prev = vec_total.copy()
	my_position_prev = my_position.copy()
	
	my_position_R = na([0,0])

	a = angle_clockwise(vec_total,[0,1])
	pts_R = []
	for p in pts:
		p = p.copy()
		p -= my_position
		p = rotatePoint([0,0],p,-a)
		pts_R.append(p)
	pts_R = na(pts_R)
	
	plot_rotated = True

	if d > 0: #0.65:
		plt.figure(1)
		plt.clf()
		if not plot_rotated:
			plt.plot(pts[:,0],pts[:,1],'.')
			#plt.plot([my_position[0],my_position[0]+vec_total[0]/10000.],[my_position[1],my_position[1]+vec_total[1]/10000.],'r-')
			plt.plot(my_position[0],my_position[1],'go')
		else:
			plt.title(a)
			plt.plot(pts_R[:,0],pts_R[:,1],'.')
			plt.plot(my_position_R[0],my_position_R[1],'go')

		plt.xlim(-1.5,1.5)
		plt.ylim(-1.5,1.5)
		plt.pause(0.00333)

