from kzpy3.vis2 import *


def plot_line(a,b,c):
	plot([a[0],b[0]],[a[1],b[1]],c)



Markers_clockwise = {
	################
	# East 1
	'East':[ 51,50,4,63,
		# East 2
		146,147,148,149,
		# East 3
		52,189,192,191,
		# East 4
		199,200,202,203],
		#
		################

	# South 1
	'South':[204,205,208,206,
		# South 2
		174,175,176,177,
		# South 3
		57,58,67,59,
		# South 4
		173,172,171,170],
	#
	################
	# West 1
	'West':[227,226,228,225,
		# West 2
		153,152,151,150,
		# West 3
		134,133,139,138,
		# West 4
		216,217,218,219],
	#################
	# North 1
	'North':[223,222,221,220,
		# North 2
		132,137,136,135,
		# North 3
		198,196,197,194,
		# North 4
		178,179,180,181]
		###############
}
Marker_xy_dic = {}

marker_spacing_ = 107/4.0/100.0

ctr_ = 7.5
for k_ in Markers_clockwise['North']:
	Marker_xy_dic[k_] = [ctr_*marker_spacing_,-8*marker_spacing_]
	ctr_ -= 1
ctr_ = -7.5
for k_ in Markers_clockwise['South']:
	Marker_xy_dic[k_] = [ctr_*marker_spacing_,8*marker_spacing_]
	ctr_ += 1
ctr_ = -7.5
for k_ in Markers_clockwise['East']:
	Marker_xy_dic[k_] = [-8*marker_spacing_,ctr_*marker_spacing_]
	ctr_ += 1
ctr_ = 7.5
for k_ in Markers_clockwise['West']:
	Marker_xy_dic[k_] = [8*marker_spacing_,ctr_*marker_spacing_]
	ctr_ -= 1



F = h5r('/media/karlzipser/ExtraDrive2/bdd_car_data_July2017_LCR/h5py/direct_home_LCR_Aruco1_23Jul17_20h51m31s_Mr_Yellow/original_timestamp_data.h5py')



#if 'A' not in locals():
#	A=preprocess_bagfile(path,'/media/karlzipser/ExtraDrive4/Mr_Yellow_23_24July2017/processed2/direct_home_LCR_Aruco1_23Jul17_20h51m31s_Mr_Yellow/bair_car_2017-07-23-20-52-11_1.bag', visualize,0)

L = A['left']
ts_ = sorted(L.keys())
ctr_ = 0
for t_ in ts_:
	Q = L[t_]
	marker_ids = sorted(Q['angles_surfaces'].keys())


	pts_ = []
	figure(33)
	plt_square()
	N=4
	xylim(-N,N,-N,N)
	for k_ in Marker_xy_dic.keys():
		plt.annotate(str(k_),Marker_xy_dic[k_])
		pts_.append(Marker_xy_dic[k_])
		pts_plot(np.array(pts_),'g')
		

	figure(22);clf()
	figure(1)
	clf()
	plt_square()
	N=4
	xylim(-N,N,-N,N)

	for marker in marker_ids:
		alpha = np.degrees(Q['angles_to_center'][marker])/2.0
		beta = np.degrees(Q['angles_surfaces'][marker])
		dist = Q['distances_marker'][marker]
		#print(marker,alpha,beta,dist)
		




		a = [0,1]
		h = [0.1,0]
		a_rotated = np.array(rotatePoint([0,0],a,-90-alpha))
		marker_point = dist*a_rotated
		marker_face = np.array(rotatePoint([0,0],-marker_point,beta))/length(marker_point)/10.0

		marker_point_centered_car_point = -marker_point
		marker_point_centered_heading = marker_point_centered_car_point+h
		gamma = angle_clockwise([0,-1],marker_face)
		"""
		rotated_neg_marker_point = np.array(rotatePoint([0,0],-marker_point,gamma))
		rotated_marker_face = np.array(rotatePoint([0,0],marker_face,gamma))
		a_rotated2 = np.array(rotatePoint([0,0],a,gamma))
		rotated_h = np.array(rotatePoint([0,0],h,gamma))
		"""
		plot_line([0,0],h,'k')
		plot_line([0,0],a,'r')
		plot_line([0,0],marker_point,'b')
		plt.annotate(marker,marker_point)
		#plot_line([0,0],-marker_point,'b:')
		#plot_line([0,0],marker_face,'y:')
		plot_line(marker_point,marker_point+marker_face,'y')
		
		figure(22)
		
		plt_square()
		N=4
		xylim(-N,N,-N,N)

		if marker in Marker_xy_dic:
			xy = np.array(Marker_xy_dic[marker])
			origin = np.array([0,0])

			plot_line(xy+origin, xy+np.array( rotatePoint(origin,marker_face,gamma)),'y')
			plot_line(xy+origin, xy+np.array( rotatePoint(origin,marker_point_centered_car_point,gamma)),'b')
			plot_line(xy+np.array( rotatePoint(origin,marker_point_centered_car_point,gamma)),
				xy+np.array( rotatePoint(origin,marker_point_centered_heading,gamma)),'k')
			plt.annotate(marker,xy+np.array( rotatePoint(origin,marker_point_centered_heading,gamma)))
		
		figure(33)
		plt_square()
		N=4
		xylim(-N,N,-N,N)
		xy = np.array(Marker_xy_dic[58])
		plot_line(xy,xy+h,'k')
		plot_line(xy,xy+a,'r')
		plot_line(xy,xy+marker_point,'b')
		plt.annotate(marker,marker_point)
		plot_line(marker_point,marker_point+marker_face,'y')


		figure(1)
		#print(marker,dp(angle_clockwise([0,-1],marker_face)))
	mi(F[left_image][vals][ctr_],0);pause(0.01)
	ctr_ += 1
	pause(.001)
	raw_input('enter')