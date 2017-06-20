
from kzpy3.vis import *
# run "kzpy3/teg2/gps_fence/first.py"
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
	f = 0.001*1.0/((0.01*dist)**2.5)
	vec = np.array(my_position) - np.array(object_position)
	vec *= f
	#print dist,vec
	return vec

my_position = (np.random.random(2)-0.5)/4.0
my_heading = 90

pts = []
for i in range(20000):
	a = np.random.random()
	p = 2*np.random.random(2) - 1
	if distance(p,(0,0))>a**0.1:
		pts.append(p)
		if len(pts) > 150:
			break
for i in range(50):
	p = 2*np.random.random(2) - 1
	pts.append(p)


pts = np.array(pts)
rpts = pts.copy()
vec_total_prev = np.array((0,0))
my_position_prev = np.array((0,0))
GO_UP = True
while distance(my_position,(0,0)) < 10000: #1.415:
	plt.figure(1)
	plt.clf()
	#plt.subplot(1,2,1)
	#plt.plot(pts[:,0],pts[:,1],'.')
	#plt.plot(my_position[0],my_position[1],'o')
	#plt.xlim(-0.5,1.5)
	#plt.ylim(-0.5,1.5)

	
	"""
	rpts[:,0] -= my_position[0]
	rpts[:,1] -= my_position[1]
	rpts = rotatePolygon(rpts,my_heading)
	"""
	#rpts = np.array(rpts)
	#plt.subplot(1,2,2)
	plt.plot(rpts[:,0],rpts[:,1],'.')
	#plt.plot(0,0,'o')
	plt.xlim(-1.5,1.5)
	plt.ylim(-1.5,1.5)



	vec_total = np.array([0.0,0.0])
	for i in range(len(rpts)):
		vec_total += 0.01 * force_function((my_position[0],my_position[1]),rpts[i,:])
	#D = distance(my_position,(0,0))
	#if D > 0.5:
	#	vec_total += -10*D*my_position
	vec_total += 1.0*vec_total_prev + 0.01*np.random.random(2)
	if distance(my_position,(1,1))>0.2 and GO_UP:
		vec_total +=25*np.array((1,1))
	elif distance(my_position,(1,1))<0.2 and GO_UP:
		GO_UP = False
		vec_total +=25*np.array((-1,-1))
	elif distance(my_position,(-1,-1))>0.2 and not GO_UP:
		vec_total +=25*np.array((-1,-1))
	else:
		GO_UP = True
		vec_total +=25*np.array((1,1))

	plt.plot([my_position[0],my_position[0]+vec_total[0]/10000.],[my_position[1],my_position[1]+vec_total[1]/10000.],'r-')
	plt.plot(my_position[0],my_position[1],'go')


	
	my_position += 1.0/distance(vec_total,(0,0)) * vec_total * 0.01
	if distance(my_position_prev,my_position) < 0.01:
		my_position+=1.0/distance(vec_total_prev,(0,0)) * vec_total_prev * 0.01
	vec_total_prev = vec_total.copy()
	my_position_prev = my_position.copy()
	plt.pause(0.00333)

