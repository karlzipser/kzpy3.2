from kzpy3.teg2.gps_fence.fourth_3 import *
from kzpy3.teg2.gps_fence.geometry import *

orig = na([0.,0.])


def pt_plot(p):
	plt.plot(p[0],p[1],'orig')

def line_plot(p1,p2):
	plt.plot([p1[0],p2[0]],[p1[1],p2[1]],'r-')

def pt_to_img_coordinates(pt,img_shape):
	pt = na(pt)
	wid = img_shape[1]
	hei = img_shape[0]
	pt *= (wid/2.0)
	pt[0] += wid/2.0
	pt[1] += hei/2.0
	return pt




def get_pts(v1,w,h,d,graphics=False):
	v1 = na(v1)
	m = np.sqrt(v1[0]**2 + v1[1]**2)
	u1 = v1 / m
	v2 = -w * u1
	v3a = rotatePoint(orig,v2,90)
	v3b = rotatePoint(orig,v2,-90)
	v4a = v1 + v3a
	v4b = v1 + v3b
	v5a = na([d*v4a[0]/v4a[1],d])
	v5b = na([d*v4b[0]/v4b[1],d])
	if graphics:
		plt.figure(3)
		plt.plot([-2,2],[d,d])
		pt_plot(orig)
		pt_plot(v4a);pt_plot(v4b)
		pt_plot(v1)		
		line_plot(orig,v5a)
		line_plot(orig,v5b)
		plt.xlim(-2,2);plt.ylim(-2,2)
		plt_square()
	return v5a[0],v5b[0],m

def get_pts2(v1,w,h,d,to_one_scale_factor,y_offset,graphics=False):
	v1 = na(v1)
	m = np.sqrt(v1[0]**2 + v1[1]**2)
	a,b,m2 = get_pts([0,m],w,h,d,False)
	object_screen_width = np.abs(a-b)
	a2,b2,m3 = get_pts(v1,0.00001,h,d,False)
	v_center = [a2,d]
	v_left = [a2-object_screen_width/2.,d]
	v_right = [a2+object_screen_width/2.,d]
	v_bottom = [h*(1-d/m),d]
	x0 = v_left[0] * to_one_scale_factor
	y0 = -v_bottom[0] * to_one_scale_factor + y_offset*to_one_scale_factor
	x1 = v_right[0] * to_one_scale_factor
	y1 = -v_bottom[0] * to_one_scale_factor + y_offset*to_one_scale_factor
	x2 = v_left[0] * to_one_scale_factor
	y2 = (h/w*object_screen_width-v_bottom[0]) * to_one_scale_factor + y_offset*to_one_scale_factor
	x3 = v_right[0] * to_one_scale_factor
	y3 = (h/w*object_screen_width-v_bottom[0]) * to_one_scale_factor + y_offset*to_one_scale_factor
	if graphics:
		plt.figure(3)
		plot([x0,x1,x3,x2,x0],[-y0,-y1,-y3,-y2,-y0],'k')
	return [[x0,y0],[x1,y1],[x2,y2],[x3,y3]],m


def get_pts3(v1,w,h,d,to_one_scale_factor,y_offset,graphics=False):
	pts,m = get_pts2(v1,w,h,d,to_one_scale_factor,y_offset,True)
	img_pts = []
	for p in pts:
		img_pts.append(pt_to_img_coordinates(p,(380,520)))
	if graphics:
		figure(4)
		plt_square()
		plt.xlim(0,200)
		plt.ylim(0,100)
		x1 = int(img_pts[0][0])
		x2 = int(img_pts[1][0])
		y1 = int(img_pts[1][1])
		y2 = int(img_pts[3][1])
		plot([x1,x2],[y1,y1],'r')
		plot([x1,x2],[y2,y2],'r')
		plot([x1,x1],[y1,y2],'r')
		plot([x2,x2],[y1,y2],'r')
	return img_pts,m


def mi_picture(img,img_pts,m,graphics=False):
	x1 = int(img_pts[0][0])
	x2 = int(img_pts[1][0])
	y1 = int(img_pts[1][1])
	y2 = int(img_pts[3][1])

	c = 255 - 128/(1.0*m)
	if c < 0:
		c = 0
	if c > 255:
		c = 255

	img[y1:y2,x1:x2] = c

	if graphics:
		mi(img,2)










def main():

	screen_distance = 0.005
	rng = 19.2
	to_one_scale_factor = rng*10 * 7.0 / screen_distance * 0.01
	y_offset = 0.075+0.00485
	shape_height = 0.08
	shape_width = shape_height / 4.0
	img_start = imread(opjD('temp.png')) #zeros((300,300))

	p = Points()
	for i in range(1000):
		#img = img_start.copy()
		pts_R = p.do_update()
		figure(3)
		clf()
		plot([-rng,rng],[0,0],'r')
		plot([0,0],[-rng,rng],'r')
		
		plt.xlim(-rng,rng)
		plt.ylim(-rng,rng)
		#mi(img,3)
		figure(2)
		clf()
		plt.xlim(-1.5,1.5)
		plt.ylim(-1.5,1.5)
		plot(0,0,'ko')
		plot(pts_R[:,0],pts_R[:,1],'b.')
		


		dist = []
		for rp in pts_R:
			dist.append(np.sqrt(rp[0]**2+rp[1]**2))

		pts_V = []
		pts_A = []

		import operator
		dist_sorted = sorted(enumerate(dist), key=operator.itemgetter(1))

		for i in range(len(dist_sorted)-1,-1,-1):
			s = dist_sorted[i]
			rp = pts_R[s[0]]
			x = rp[0]
			y = rp[1]
			pts_A.append([x,y])
			if y > 0:#screen_distance:
				if np.rad2deg(angle_between([1,0],[x,y])) > 30:
					if np.rad2deg(angle_between([1,0],[x,y])) < 180-30:
						pts_V.append([x,y])
		figure(2)
		for pt in pts_A:
			x = pt[0]
			y = pt[1]
			plot(x,y,'bx')
		for pt in pts_V:
			x = pt[0]
			y = pt[1]
			figure(2)
			plot(x,y,'ro')
			img_pts,m = get_pts3([x,y],shape_width,shape_height,screen_distance,to_one_scale_factor,y_offset,False)

			#mi_picture(img,img_pts,m,False)

		#img[100,0]=0.33
		#mi(img,'img')#mi(img[:,50:150],'img')
		plt.pause(0.001)

if __name__ == '__main__':
	main()


