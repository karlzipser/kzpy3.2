from kzpy3.vis import *
from kzpy3.data_analysis.Angle_Dict_Creator import get_angles_and_distance
from kzpy3.data_analysis.markers_clockwise import markers_clockwise


out_img = zeros((1000,1000,3),np.uint8)

def plot_it(angle1,distance1,angle2,distance2):


	xc = distance1 * np.sin(angle1)
	yc = distance1 * np.cos(angle1)

	plot([0,xc],[0,yc])

	xd = distance2 * np.sin(angle2)
	yd = distance2 * np.cos(angle2)

	plot([xc,xd+xc],[yc,yd+yc])

	circ=plt.Circle((xd+xc,yd+yc),distance2,fill=False)

	ax.add_patch(circ)
	pause(0.03)

marker_ids_all = []
"""
for i in range(0,2300):
	img = imread('/home/karlzipser/Desktop/temp2_/'+str(i)+'.png' )
	#mi(img,2)
	angles_to_center, angles_surfaces, distances_marker, markers = get_angles_and_distance(img) 

	#fig=plt.figure(1)
	#plt.clf()
	#ax=fig.add_subplot(1,1,1)
	#xlim(-10,10)
	#ylim(-10,10)

	distance2 = 4*107/100.

	marker_ids = angles_to_center.keys()

	for m in marker_ids:

		angle1 = angles_to_center[m]
		distance1 = distances_marker[m]
		angle2 = angles_surfaces[m]
		if distance1 < 2:
			marker_ids_all.append(m)
		if distance1 < 2:
			pass #plot_it(angle1,distance1,angle2,distance2)

	#raw_input('>')
		
if False:
	seen = {}
	new = []
	for i in range(3500,len(marker_ids_all)):
		m = marker_ids_all[i]
		if m in seen:
			pass
		else:
			new.append(m)
			seen[m] = True
"""
marker_angles_dic = {}
marker_angles = 2*np.pi*np.arange(len(markers_clockwise))/(1.0*len(markers_clockwise))
marker_xys = []
for i in range(len(markers_clockwise)):
	a = marker_angles[i]
	marker_angles_dic[markers_clockwise[i]] = a
	x = 4*107/100.*np.sin(a)
	y = 4*107/100.*np.cos(a)
	marker_xys.append([x,y])
#marker_xys = array(marker_xys)

markers_xy_dic = {}
figure(1)
clf()
assert(len(markers_clockwise) == len(marker_xys))
for i in range(len(markers_clockwise)):
	m = markers_clockwise[i]
	xy = marker_xys[i]
	markers_xy_dic[m] = xy
	cv2.circle(out_img,(int(100*xy[0])+500,int(100*xy[1])+500),4,(255,0,0),-1)
	#plot(xy[0],xy[1],'bo-')
	#plt.text(xy[0],xy[1],str(m),fontsize=6)


#plot(marker_xys[:,0],marker_xys[:,1],'o')





def plot_it2(angle1,distance1,angle2,distance2,xy):


	#xc = distance1 * np.sin(angle1)
	#yc = distance1 * np.cos(angle1)

	#plot([0,xc],[0,yc])

	xd = distance1 * np.sin(angle2)
	yd = distance1 * np.cos(angle2)

	plot([xy[0],xd+xy[0]],[xy[1],yd+xy[1]])

	#circ=plt.Circle((xd+xc,yd+yc),distance2,fill=False)

	#ax.add_patch(circ)
	pause(0.001)


x_avgs = []
y_avgs = []
ctr = 0
for side in ['left','temp2']:
	for i in range(0,1000,1):
		
			if side == 'left':
				dot_color = (0,0,255)
			else:
				dot_color = (255,255,0)
			img = imread('/home/karlzipser/Desktop/'+side+'/'+str(i)+'.png' )
			
			angles_to_center, angles_surfaces, distances_marker, markers = get_angles_and_distance(img) 
			#print angles_surfaces
			#print distances_marker
			print "---------------------"
			#fig=plt.figure(1)
			#plt.clf()
			#ax=fig.add_subplot(1,1,1)
			#xlim(-10,10)
			#ylim(-10,10)

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
				if m == 190: # This one gives false positives on ground.
					continue
				if m in markers_xy_dic:
					xy = markers_xy_dic[m]
					angle1 = angles_to_center[m]
					distance1 = distances_marker[m]
					print(m,(np.degrees(marker_angles_dic[m])),np.degrees(angles_surfaces[m]),distances_marker[m])
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
			median_d = median_d**2+3
			print int(median_d)
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
				mci(out_img,delay=1,title='out_img')
				k = mci(img)
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




