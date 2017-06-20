from kzpy3.teg2.gps_fence.fourth import *



def rotatePoint(centerPoint,point,angle):
    """http://stackoverflow.com/questions/20023209/function-for-rotating-2d-objects
    Rotates a point around another centerPoint. Angle is in degrees.
    Rotation is counter-clockwise"""
    angle = math.radians(angle)
    temp_point = point[0]-centerPoint[0] , point[1]-centerPoint[1]
    temp_point = ( temp_point[0]*math.cos(angle)-temp_point[1]*math.sin(angle) , temp_point[0]*math.sin(angle)+temp_point[1]*math.cos(angle))
    temp_point = temp_point[0]+centerPoint[0] , temp_point[1]+centerPoint[1]
    return temp_point


def unit_vector(vector):
    """http://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python
    Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

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










ar = np.array

o = ar([0.,0.])
w = 0.1
v1 = ar([1.,1.])
v1_ = ar([0,1])
d = 0.1

def pt_plot(p):
	plt.plot(p[0],p[1],'o')

def line_plot(p1,p2):
	plt.plot([p1[0],p2[0]],[p1[1],p2[1]],'r-')

def get_pts(v1,w,graphics=False):
	v1 = na(v1)
	m = np.sqrt(v1[0]**2 + v1[1]**2)
	u1 = v1 / m
	v2 = -w * u1
	v3a = rotatePoint(o,v2,90)
	v3b = rotatePoint(o,v2,-90)
	v4a = v1 + v3a
	v4b = v1 + v3b
	v5a = ar([d*v4a[0]/v4a[1],d])
	v5b = ar([d*v4b[0]/v4b[1],d])
	if graphics:
		plt.figure(3)
		#clf()
		plt.plot([-2,2],[d,d])
		pt_plot(o)
		pt_plot(v4a);pt_plot(v4b)
		pt_plot(v1)
		#line_plot(o,v4a)
		#line_plot(o,v4b)		
		line_plot(o,v5a)
		line_plot(o,v5b)
		plt.xlim(-2,2);plt.ylim(-2,2)
		plt_square()
	return v5a[0],v5b[0],m


def get_pts2(v1,w,graphics=False):
	v1 = na(v1)
	m = np.sqrt(v1[0]**2 + v1[1]**2)
	a,b,m2 = get_pts([0,m],w,False)
	object_screen_width = np.abs(a-b)
	a2,b2,m3 = get_pts(v1,0.00001,False)
	v_center = [a2,d]
	v_left = [a2-object_screen_width/2.,d]
	v_right = [a2+object_screen_width/2.,d]

	if graphics:
		plt.figure(3)
		#clf()
		plt.plot([-2,2],[d,d])
		pt_plot(o)
		line_plot(o,v1)
		line_plot(o,v_left)
		line_plot(o,v_right)
		plt.xlim(-2,2);plt.ylim(-2,2)
		plt_square()
	return [[v_left[0],-object_screen_width/2.],[v_right[0],-object_screen_width/2.],[v_left[0],object_screen_width/2.],[v_right[0],object_screen_width/2.]],m


def pt_to_img_coordinates(pt):
	pt = na(pt)
	pt *= 600.
	pt[0] += 100
	pt[1] += 50
	return pt

def get_pts3(v1,w,graphics=False):
	pts,m = get_pts2(v1,w,False)
	img_pts = []
	for p in pts:
		img_pts.append(pt_to_img_coordinates(p))
	if graphics:
		figure(4)
		plt_square()
		plt.xlim(0,200)
		plt.ylim(0,100)

		#line_plot(img_pts[0],img_pts[1])
		#line_plot(img_pts[1],img_pts[2])
		#line_plot(img_pts[2],img_pts[3])
		#line_plot(img_pts[3],img_pts[0])
		x1 = int(img_pts[0][0])
		x2 = int(img_pts[1][0])
		y1 = int(img_pts[1][1])
		y2 = int(img_pts[3][1])
		plot([x1,x2],[y1,y1],'r')
		plot([x1,x2],[y2,y2],'r')
		plot([x1,x1],[y1,y2],'r')
		plot([x2,x2],[y1,y2],'r')
	return img_pts,m



def mi_picture(img_pts,m,graphics=False):
	global img
	x1 = int(img_pts[0][0])
	x2 = int(img_pts[1][0])
	y1 = int(img_pts[1][1])
	y2 = int(img_pts[3][1])

	img[y1:y2,x1:x2] = 1/(10.0*m)

	if graphics:
		mi(img,2)













img = zeros((100,200))

p = Points()
for i in range(1000):
	img *= 0
	pts_R = p.do_update()
	figure(2)
	clf()
	plt.xlim(-1.5,1.5)
	plt.ylim(-1.5,1.5)
	plot(0,0,'ro')
	plot(pts_R[:,0],pts_R[:,1],'b.')
	


	dist = []
	for rp in pts_R:
		dist.append(np.sqrt(rp[0]**2+rp[1]**2))

	import operator
	dist_sorted = sorted(enumerate(dist), key=operator.itemgetter(1))
	for i in range(len(dist_sorted)-1,0,-1):
		s = dist_sorted[i]
		rp = pts_R[s[0]]
		x = rp[0]
		y = rp[1]
		if y > 0:
			if np.rad2deg(angle_between([1,0],[x,y])) > 35:
				if np.rad2deg(angle_between([1,0],[x,y])) < 180-35:
					plot(x,y,'ro')
					img_pts,m = get_pts3([x,y],0.01,False)
					mi_picture(img_pts,m,False)
	mi(img[:,50:150],'img')
	plt.pause(0.001)
