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


ar = np.array

o = ar([0.,0.])
w = 0.1
v1 = ar([1.,1.])
v1_ = ar([0,1])
d = 0.3

def pt_plot(p):
	plt.plot(p[0],p[1],'o')

def line_plot(p1,p2):
	plt.plot([p1[0],p2[0]],[p1[1],p2[1]],'r-')


def plt_square():
	plt.gca().set_aspect('equal', adjustable='box')
	plt.draw()



def get_pts(v1,w):
	m = np.sqrt(v1[0]**2 + v1[1]**2)
	u1 = v1 / m
	v2 = -w * u1
	v3a = rotatePoint(o,v2,90)
	v3b = rotatePoint(o,v2,-90)
	v4a = v1 + v3a
	v4b = v1 + v3b
	v5a = ar([d*v4a[0]/v4a[1],d])
	v5b = ar([d*v4b[0]/v4b[1],d])
	if False:
		plt.figure(1)
		plt.plot([-2,2],[d,d])
		pt_plot(o)
		pt_plot(v1)
		pt_plot(v4a)
		pt_plot(v4b)
		pt_plot(v5a)
		pt_plot(v5b)
		line_plot(o,v4a)
		line_plot(o,v4b)
		plt.xlim(-2,2);plt.ylim(-2,2)
		plt_square()
	return v5a[0],v5b[0],m

img = zeros((100,200))
plt.figure(1)
plt.clf()

def picture(v1,w):
	a,b,m = get_pts(v1,w)
	a0,b0,m0 = get_pts(ar([0,m]),w)
	aa = 100*a
	bb = 100*b	
	aa0 = 100*a0
	bb0 = 100*b0
	img[50-(aa0-bb0)/2.:50+(aa0-bb0)/2.,100+bb:100+aa] = 1/(10*m)
	mi(img,2)

picture(ar([1,1]),w)
picture(ar([-2,3]),w)
picture(ar([0,0.4]),w)
raw_input('enter to quit')

