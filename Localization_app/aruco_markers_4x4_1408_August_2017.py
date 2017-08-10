from kzpy3.utils2 import *
from kzpy3.vis2 import *



def normalize(v):
	"""
	https://stackoverflow.com/questions/4114921/vector-normalization?lq=1
	"""
	import math
	def magnitude(v):
		return math.sqrt(sum(v[i]*v[i] for i in range(len(v))))
	def add(u, v):
		return [ u[i]+v[i] for i in range(len(u)) ]
	def sub(u, v):
		return [ u[i]-v[i] for i in range(len(u)) ]
	def dot(u, v):
		return sum(u[i]*v[i] for i in range(len(u)))	
	vmag = magnitude(v)
	return [ v[i]/vmag  for i in range(len(v)) ]




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






markers_clockwise_ = [ 51,50,4,63,
		# East 2
		146,147,148,149,
		# East 3
		52,189,192,191,
		# East 4
		199,200,202,203,204,205,208,206,
		# South 2
		174,175,176,177,
		# South 3
		57,58,67,59,
		# South 4
		173,172,171,170,227,226,228,225,
		# West 2
		153,152,151,150,
		# West 3
		134,133,139,138,
		# West 4
		216,217,218,219,223,222,221,220,
		# North 2
		132,137,136,135,
		# North 3
		198,196,197,194,
		# North 4
		178,179,180,181]
		###############




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

figure(2);clf();plt_square()
pts = []
for k_ in Marker_xy_dic.keys():
	pts.append(Marker_xy_dic[k_])
	plt.annotate(str(k_),Marker_xy_dic[k_])
pts_plot(np.array(pts))
"""
for i_ in rlen(markers_clockwise_):
	Marker_xy_dic[markers_clockwise_[i_]] = (i_ * marker_spacing_,0)
"""


def get_camera_position(angles_to_center,angles_surfaces,distances_marker):
	marker_ids = angles_to_center.keys()
	x_avg = 0.0
	y_avg = 0.0
	d_sum = 0.0
	xs = []
	ys = []
	ds = []
	for m_ in marker_ids:
		if m_ in [190]: # This one gives false positives on ground.
			continue
		if m_ in markers_xy_dic:
			xy = markers_xy_dic[m_]
			angle1 = angles_to_center[m_]
			distance1 = distances_marker[m_]
			distance2 = 4*107/100.
			angle2 = (np.pi+marker_angles_dic[m_]) - (np.pi/2.0-angles_surfaces[m_])
			xd = distance1 * np.sin(angle2)
			yd = distance1 * np.cos(angle2)
			#print (dp(np.degrees(marker_angles_dic[m_]+np.pi/2.0-angles_surfaces[m_]+angles_to_center[m_]),2))#,dp(np.degrees(marker_angles_dic[m_]),2),dp(np.degrees(angles_surfaces[m_]),2),dp(np.degrees(angles_to_center[m_],2)))
			if distance1 < 2*distance2 and distance1 > 0.05:
			#if distance1 < 2 and distance1 > 0.05:
				xs.append(xd+xy[0])
				ys.append(yd+xy[1])
				ds.append(distance1)
	d = 0
	for i in range(len(xs)):
		d += 1/ds[i]
		x_avg += d*xs[i]
		y_avg += d*ys[i]
		d_sum += d
	if len(ds) > 2:
		median_distance_to_markers = np.median(array(ds))
	elif len(ds) > 0:
		median_distance_to_markers = array(ds).min()
	else:
		median_distance_to_markers = None
	if d_sum == 0:
		return None,None,None,None
	x_avg /= d_sum
	y_avg /= d_sum
	return marker_ids,x_avg,y_avg,median_distance_to_markers







	




Marker_orientation_parameters = {}
for q_ in ['angle1','angle2','sign1','sign2']:
	Marker_orientation_parameters[q_] = {}
for m_ in Markers_clockwise['North']:
	Marker_orientation_parameters['angle1'][m_] = 90.0
	Marker_orientation_parameters['sign1'][m_] = -1.0
	Marker_orientation_parameters['angle2'][m_] = 1.0
	Marker_orientation_parameters['sign2'][m_] = -90.0
for m_ in Markers_clockwise['East']:
	Marker_orientation_parameters['angle1'][m_] = 90
	Marker_orientation_parameters['sign1'][m_] = sign1_
	Marker_orientation_parameters['angle2'][m_] = 0.0
	Marker_orientation_parameters['sign2'][m_] = -1.0
###########################################################
for m_ in Markers_clockwise['South']:
	Marker_orientation_parameters['angle1'][m_] = -90
	Marker_orientation_parameters['sign1'][m_] = -1.0
	Marker_orientation_parameters['angle2'][m_] = 90.0
	Marker_orientation_parameters['sign2'][m_] = -1.0
###########################################################

for m_ in Markers_clockwise['West']:
	Marker_orientation_parameters['angle1'][m_] = 0
	Marker_orientation_parameters['sign1'][m_] = 1.0
	Marker_orientation_parameters['angle2'][m_] = 1.0
	Marker_orientation_parameters['sign2'][m_] = 0.0


L = A['left']
ts_ = sorted(L.keys())


ctr_=0
for t_ in ts_[0:]:
	print ctr_
	Q = L[t_]

	figure(3)
	clf()
	N=6
	xylim(-N,N,-N,N)
	plt_square()
	pts = []
	for k_ in Marker_xy_dic.keys():
		plt.annotate(str(k_),Marker_xy_dic[k_])
		pts.append(Marker_xy_dic[k_])
	pts_plot(np.array(pts),'g')


	Mop = Marker_orientation_parameters
	for k_ in Q['distances_marker'].keys():
		if k_ not in Marker_xy_dic.keys():
			continue
		p0_ = np.array(Marker_xy_dic[k_])
		p1_ = np.array([p0_[0],p0_[1]-Q['distances_marker'][k_]])
		rp0_ = rotatePoint(p0_,p1_,-np.degrees(Q['angles_to_center'][k_]))
		rp1_ = rotatePoint(p0_,rp0_,Mop['angle1'][k_])
		#rp1_ = rotatePoint(rp0_,p0_,Mop['angle2'][k_]+Mop['sign2'][k_]*np.degrees(Q['angles_surfaces'][k_]))
		#v_ = np.array(rp1_) - np.array(rp0_)
		#vn_ = normalize(v_)
		#p2_ = np.array(vn_)/10.0+np.array(rp0_)
		plot(p0_[0],p0_[1],'k.')
		plot(rp1_[0],rp1_[1],'r.')
		plot([p0_[0],rp1_[0]], [p0_[1],rp1_[1]],'k')
		#plot(p2_[0],p2_[1],'b.')

	ctr_+=1
	pause(0.01)
	#print angle1_,sign1_
	#raw_input('hit enter')






	# check if estimate is in space
	"""
	for k_ in Markers[x].keys():
		plot(Markers[x][k_],Markers[y][k_],'o')
		p1 = [Markers[x][k_],Markers[y][k_]]
		p2 = [Markers[x][k_],Markers[y][k_]-Q['distances_marker'][k_]]
		rp_ = rotatePoint(p1,p2,Markers['angle'][k_]+Markers['sign'][k_]*np.degrees(Q['angles_to_center'][k_]))
		plot(rp_[0],rp_[1],'x')
		plot([Markers[x][k_],rp_[0]],[  Markers[y][k_],rp_[1]])
		rp2_ = rotatePoint(rp_,p1,Markers['angle2'][k_]+Markers['sign2'][k_]*np.degrees(Q['angles_surfaces'][k_]))
		#plot([rp2_[0],rp_[0]],[rp2_[1],rp_[1]])
		v = np.array(rp2_) - np.array(rp_)
		vn = normalize(v)

		p3 = np.array(vn)/10.0+np.array(rp_)
		plot([rp_[0],p3[0]],[rp_[1],p3[1]])
	#rotatePoint(centerPoint,point,angle)
	"""


#EOF
