from kzpy3.vis import *
from kzpy3.data_analysis.markers_clockwise import markers_clockwise


out_img = zeros((1000,1000,3),np.uint8)



marker_ids_all = []

marker_angles_dic = {}
marker_angles = 2*np.pi*np.arange(len(markers_clockwise))/(1.0*len(markers_clockwise))
marker_xys = []
for i in range(len(markers_clockwise)):
	a = marker_angles[i]
	marker_angles_dic[markers_clockwise[i]] = a
	x = 4*107/100.*np.sin(a)
	y = 4*107/100.*np.cos(a)
	marker_xys.append([x,y])


markers_xy_dic = {}
#figure(1)
#clf()
assert(len(markers_clockwise) == len(marker_xys))
for i in range(len(markers_clockwise)):
	m = markers_clockwise[i]
	xy = marker_xys[i]
	markers_xy_dic[m] = xy
	cv2.circle(out_img,(int(100*xy[0])+500,int(100*xy[1])+500),4,(255,0,0),-1)





def plot_it2(angle1,distance1,angle2,distance2,xy):

	xd = distance1 * np.sin(angle2)
	yd = distance1 * np.cos(angle2)

	plot([xy[0],xd+xy[0]],[xy[1],yd+xy[1]])

	pause(0.001)



#A = lo('/home/karlzipser/Desktop/bair_car_data_new/meta/direct_rewrite_test_25Apr17_14h32m22s_Mr_Orange/marker_data.pkl' )
#A = lo('/home/karlzipser/Desktop/bair_car_data_new/meta/direct_rewrite_test_25Apr17_13h09m04s_Mr_Black/marker_data.pkl')
#A = lo('/home/karlzipser/Desktop/bair_car_data_new/meta/direct_rewrite_test_25Apr17_13h09m04s_Mr_Black/marker_data.pkl')
A = lo('/home/karlzipser/Desktop/bair_car_data_new/meta/direct_rewrite_test_25Apr17_21h31m25s_Mr_Yellow/marker_data.pkl')

x_avgs = {}
x_avgs['left'] = []
x_avgs['right'] = []
y_avgs = {}
y_avgs['left'] = []
y_avgs['right'] = []
ctr = 0

def get_position(angles_to_center,angles_surfaces,distances_marker):

	marker_ids = angles_to_center.keys()

	x_avg = 0.0
	y_avg = 0.0
	d_sum = 0.0

	xs = []
	ys = []
	ds = []
	for m in marker_ids:
		if m in [190]: # This one gives false positives on ground.
			continue
		if m in markers_xy_dic:
			xy = markers_xy_dic[m]
			angle1 = angles_to_center[m]
			distance1 = distances_marker[m]
			distance2 = 4*107/100.
			angle2 = (np.pi+marker_angles_dic[m]) - (np.pi/2.0-angles_surfaces[m])
			xd = distance1 * np.sin(angle2)
			yd = distance1 * np.cos(angle2)
			if distance1 < 2*distance2 and distance1 > 0.05:
				xs.append(xd+xy[0])
				ys.append(yd+xy[1])
				ds.append(distance1)
	d = 0
	for i in range(len(xs)):
		d += 1/ds[i]
		x_avg += d*xs[i]
		y_avg += d*ys[i]
		d_sum += d

	median_d = np.median(array(ds))
	if d_sum == 0:
		return None,None,None,None
	x_avg /= d_sum
	y_avg /= d_sum

	median_d = max(median_d,1)
	median_d = median_d**2+3

	return marker_ids,x_avg,y_avg,median_d




out_img *= 0 
ts = {}
ts['right'] = sorted(A['right'].keys())
ts['left'] = sorted(A['left'].keys())
pts = {}
pts['left'] = []
pts['right'] = []

for i in range(len(A['left'])):

	for side in ['left','right']:
		
		if side == 'left':
			dot_color = (0,0,255)
		else:
			dot_color = (255,255,0)

		angles_to_center = A[side][ts[side][i]]['angles_to_center']
		angles_surfaces = A[side][ts[side][i]]['angles_surfaces']
		distances_marker = A[side][ts[side][i]]['distances_marker']

		marker_ids,x_avg,y_avg,median_d = get_position(angles_to_center,angles_surfaces,distances_marker)
		if marker_ids == None:
			continue
		x_avgs[side].append(x_avg)
		y_avgs[side].append(y_avg)

		if len(x_avgs[side])>10:
			#x = int(500+-100*array(x_avgs[side])[-int(5*median_d):].mean())
			#y = int(500+100*array(y_avgs[side][-int(5*median_d):]).mean())
			x = array(x_avgs[side])[-int(5*median_d):].mean()
			y = array(y_avgs[side][-int(5*median_d):]).mean()
			pts[side].append([x,y])
			if len(pts[side]) > 100:
				pts[side] = pts[side][-100:]
			#cv2.circle(out_img,(int(-100*pts[side][-1][0])+500),(int(100*pts[side][-1][0])),4,dot_color,-1)
			#cv2.circle(out_img,x,y,4,dot_color,-1)
			if len(pts[side])>11:
				for qq in range(10,0,-1):
					x,y = pts[side][-qq][0],pts[side][-qq][1]
					new_dot_color = array(dot_color)/(np.sqrt(qq))
					#print new_dot_color
					cv2.circle(out_img,(int(-100*x)+500,int(100*y)+500),4,new_dot_color,-1)
			for j in range(len(markers_clockwise)):
				m = markers_clockwise[j]
				xy = marker_xys[j]
				markers_xy_dic[m] = xy
				c = (255,0,0)
				if m in marker_ids:
					c = (0,255,0)

				cv2.circle(out_img,(int(-100*xy[0])+500,int(100*xy[1])+500),4,c,-1)

			k = mci(out_img,delay=1,title='out_img')
			if k == ord('q'):
				break

		if len(x_avgs[side]) > 100:
			x_avgs[side] = x_avgs[side][-100:]
			y_avgs[side] = y_avgs[side][-100:]			


