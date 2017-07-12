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


x_avgs = []
y_avgs = []
ctr = 0
#A = lo('/home/karlzipser/Desktop/bair_car_data_new/meta/direct_rewrite_test_25Apr17_14h32m22s_Mr_Orange/marker_data.pkl' )
#A = lo('/home/karlzipser/Desktop/bair_car_data_new/meta/direct_rewrite_test_25Apr17_13h09m04s_Mr_Black/marker_data.pkl')
A = lo('/home/karlzipser/Desktop/bair_car_data_new/meta/direct_rewrite_test_25Apr17_13h09m04s_Mr_Black/marker_data.pkl')


out_img *= 0 
ts = {}
ts['right'] = sorted(A['right'].keys())
ts['left'] = sorted(A['left'].keys())

for i in range(len(A['left'])):

	for side in ['right']:#,'right']:
		
			if side == 'left':
				dot_color = (0,0,255)
			else:
				dot_color = (255,255,0)
			
			
			angles_to_center = A[side][ts[side][i]]['angles_to_center']
			angles_surfaces = A[side][ts[side][i]]['angles_surfaces']
			distances_marker = A[side][ts[side][i]]['distances_marker']

			print side+" ---------------------"


			distance2 = 4*107/100.

			marker_ids = angles_to_center.keys()
			xlim(-5,5);ylim(-5,5)
			xs = []
			ys = []
			ds = []
			x_avg = 0.0
			y_avg = 0.0
			d_sum = 0.0
			for m in marker_ids:
				if m in [190]: #, 170,171,172,173]: # This one gives false positives on ground.
					continue
				if m in markers_xy_dic:
					xy = markers_xy_dic[m]
					angle1 = angles_to_center[m]
					distance1 = distances_marker[m]
					#print(m,(np.degrees(marker_angles_dic[m])),np.degrees(angles_surfaces[m]),distances_marker[m])
					angle2 = (np.pi+marker_angles_dic[m]) - (np.pi/2.0-angles_surfaces[m])
					#angle2=angle1
					#distance1 = 1
					#if distance1 < 2:
					#	plot_it2(angle1,distance1,angle2,distance2,xy)
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
				continue
			x_avg /= d_sum
			y_avg /= d_sum
			#x_avg = np.mean(array(xs))
			#y_avg = np.mean(array(ys))
			x_avgs.append(x_avg)
			y_avgs.append(y_avg)
			#if np.mod(ctr,3) == 0:
			median_d = max(median_d,1)
			median_d = 1#median_d**2+3
			#print int(median_d)
			print marker_ids
			if len(x_avgs)>10:
				x = array(x_avgs)[-int(5*median_d):].mean()
				y = array(y_avgs[-int(5*median_d):]).mean()
				cv2.circle(out_img,(int(-100*x)+500,int(100*y)+500),4,dot_color,-1)
				for i in range(len(markers_clockwise)):
					m = markers_clockwise[i]
					xy = marker_xys[i]
					markers_xy_dic[m] = xy
					c = (255,0,0)
					if m in marker_ids:
						c = (0,255,0)
					cv2.circle(out_img,(int(-100*xy[0])+500,int(100*xy[1])+500),4,c,-1)
				k = mci(out_img,delay=1,title='out_img')
				#k = mci(img)
				if k == ord('q'):
					break
				#plot(array(x_avgs)[-int(5*median_d):].mean(),array(y_avgs[-int(5*median_d):]).mean(),'r.')
			#if np.mod(i,10) == 0:
				#pause(0.001)
			if len(x_avgs) > 100:
				x_avgs = x_avgs[-100:]
				y_avgs = y_avgs[-100:]
			#ctr += 1
			#plot(array(x_avgs[-5:]).mean(),array(y_avgs[-5:]).mean(),'r.')
			#plot([xy[0],xd+xy[0]],[xy[1],yd+xy[1]])
			

					#plot(x_avg,y_avg,'r.')
					#pause(0.001)
			#raw_input('>')
		#except:
		#	pass



ids={}
ids['left'] = []
ids['right'] = []
for side in ['left','right']:
	ts = sorted(A[side].keys())
	for t in ts:
		ids[side] += A[side][t]['angles_to_center'].keys()