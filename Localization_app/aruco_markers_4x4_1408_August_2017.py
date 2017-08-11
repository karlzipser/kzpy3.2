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



#for i_ in rlen(markers_clockwise_):
#	Marker_xy_dic[markers_clockwise_[i_]] = (i_ * marker_spacing_,0)









Marker_orientation_parameters = {}
for q_ in ['angle1','angle2','sign1','sign2']:
	Marker_orientation_parameters[q_] = {}
for m_ in Markers_clockwise['North']:
	Marker_orientation_parameters['angle1'][m_] = 90.0
	Marker_orientation_parameters['sign1'][m_] = -1.0
	Marker_orientation_parameters['angle2'][m_] = 1.0
	Marker_orientation_parameters['sign2'][m_] = -90.0
for m_ in Markers_clockwise['East']:
	Marker_orientation_parameters['angle1'][m_] = 0
	Marker_orientation_parameters['sign1'][m_] = 1
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

w_ = 90/180.0
ctr_= 100

for t_ in ts_[ctr_:ctr_+1]:
	print ctr_
	Q = L[t_]
	figure(5)
	clf()
	N=4
	xylim(-N,N,-N,N)
	plt_square()
	pts = []
	for k_ in Marker_xy_dic.keys():
		plt.annotate(str(k_),Marker_xy_dic[k_])
		pts.append(Marker_xy_dic[k_])
	pts_plot(np.array(pts),'g')

	Mop = Marker_orientation_parameters
	for k_ in sorted(Q['distances_marker'].keys()):
		if k_ not in Marker_xy_dic.keys():
			continue
		if k_ in Markers_clockwise['West']:
			p0_ = np.array(Marker_xy_dic[k_])
			p1_ = np.array([p0_[0],p0_[1]-Q['distances_marker'][k_]])
			rp0_ = rotatePoint(p0_,p1_,-np.degrees(w_*Q['angles_to_center'][k_]));print k_,dp(-np.degrees(w_*Q['angles_to_center'][k_])),dp(np.degrees(Q['angles_to_center'][k_]))
			rp1_ = rotatePoint(p0_,rp0_,-90)
			plot(p0_[0],p0_[1],'k.')
			plot(rp1_[0],rp1_[1],'r.')
			plot([p0_[0],rp1_[0]], [p0_[1],rp1_[1]],'k')
			"""
			elif k_ in Markers_clockwise['North']:
				p0_ = np.array(Marker_xy_dic[k_])
				p1_ = np.array([p0_[0],p0_[1]-Q['distances_marker'][k_]])
				rp0_ = rotatePoint(p0_,p1_,-90+np.degrees(w_*Q['angles_to_center'][k_]));print k_,dp(-np.degrees(w_*Q['angles_to_center'][k_])),dp(np.degrees(Q['angles_to_center'][k_]))
				rp1_ = rotatePoint(p0_,rp0_,-90)
				plot(p0_[0],p0_[1],'k.')
				plot(rp1_[0],rp1_[1],'r.')
				plot([p0_[0],rp1_[0]], [p0_[1],rp1_[1]],'k')
			"""
		elif k_ in Markers_clockwise['North']:
			p0_ = np.array(Marker_xy_dic[k_])
			p1_ = np.array([p0_[0],p0_[1]-Q['distances_marker'][k_]])
			rp0_ = rotatePoint(p0_,p1_,-np.degrees(w_*Q['angles_to_center'][k_]));print k_,dp(-np.degrees(w_*Q['angles_to_center'][k_])),dp(np.degrees(Q['angles_to_center'][k_]))
			rp1_ = rotatePoint(p0_,rp0_,180)
			plot(p0_[0],p0_[1],'k.')
			plot(rp1_[0],rp1_[1],'r.')
			plot([p0_[0],rp1_[0]], [p0_[1],rp1_[1]],'k')
			
		elif k_ in Markers_clockwise['East']:
			p0_ = np.array(Marker_xy_dic[k_])
			p1_ = np.array([p0_[0],p0_[1]-Q['distances_marker'][k_]])
			rp0_ = rotatePoint(p0_,p1_,-np.degrees(w_*Q['angles_to_center'][k_]));print k_,dp(-np.degrees(w_*Q['angles_to_center'][k_])),dp(np.degrees(Q['angles_to_center'][k_]))
			rp1_ = rotatePoint(p0_,rp0_,90)
			plot(p0_[0],p0_[1],'k.')
			plot(rp1_[0],rp1_[1],'r.')
			plot([p0_[0],rp1_[0]], [p0_[1],rp1_[1]],'k')
		elif k_ in Markers_clockwise['South']:
			p0_ = np.array(Marker_xy_dic[k_])
			p1_ = np.array([p0_[0],p0_[1]-Q['distances_marker'][k_]])
			rp0_ = rotatePoint(p0_,p1_,-np.degrees(w_*Q['angles_to_center'][k_]));print k_,dp(-np.degrees(w_*Q['angles_to_center'][k_])),dp(np.degrees(Q['angles_to_center'][k_]))
			rp1_ = rotatePoint(p0_,rp0_,-90)
			plot(p0_[0],p0_[1],'k.')
			plot(rp1_[0],rp1_[1],'r.')
			plot([p0_[0],rp1_[0]], [p0_[1],rp1_[1]],'k')
	ctr_+=1

	pause(0.01)
	mi(F[left_image][vals][ctr_],0);pause(0.01)
	#raw_input('enter')
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

F = h5r('/media/karlzipser/ExtraDrive2/bdd_car_data_July2017_LCR/h5py/direct_home_LCR_Aruco1_23Jul17_20h51m31s_Mr_Yellow/original_timestamp_data.h5py')


pts='pts'
deg='deg'




def rotate_translate_polygon(*args):
	Args = args_to_dictionary(args)
	pts_ = Args[pts]
	deg_ = Args[deg]
	x_ = Args[x]
	y_ = Args[y]
	True
	new_pts_ =  np.array(rotatePolygon(pts_,deg_))
	new_pts_[:,0] += x_
	new_pts_[:,1] += y_
	return new_pts_


	"""
	Translate from .bag files to original_timestamp_data.h5py
	"""
	

L = A['left']
ts_ =F[left_image][ts][:]


def mdif(a,b):
	return (np.sqrt((a[:,0]-b[:,0])**2+(a[:,1]-b[:,1])**2)).mean()

def mn(*args):
	Args = args_to_dictionary(args)
	movable_pts_ = np.array(Args[movable_pts])
	static_pts_ = np.array(Args[static_pts])
	True
	rotate_pts_ = rotate_translate_polygon(pts,movable_pts_, deg,np.random.randn(1)[0]*5, x,np.random.randn(1)[0]*0.1, y,np.random.randn(1)[0]*0.1)
	if mdif(rotate_pts_,static_pts_) < mdif(movable_pts_,static_pts_):
		return rotate_pts_
	return movable_pts_



movable_pts = 'movable_pts'
static_pts = 'static_pts'
degs = 'degs'
scale = 'scale'
result_prev = 'result_prev'

def mn2(*args):
	Args = args_to_dictionary(args)
	movable_pts_ = np.array(Args[movable_pts])
	static_pts_ = np.array(Args[static_pts])
	degs_ = Args[degs]
	x_ = Args[x]
	y_ = Args[y]
	scale_ = Args[scale]
	result_prev_ = Args[result_prev]
	True
	def rndn():
		return np.random.randn(1)[0]
	d_deg_	= rndn()*5*scale_
	d_x_ 	= rndn()*0.1*scale_
	d_y_ 	= rndn()*0.1*scale_
	rotate_pts_ = rotate_translate_polygon(pts,movable_pts_, deg,degs_+d_deg_, x,x_+d_x_, y,y_+d_y_)
	result1_ = mdif(rotate_pts_,static_pts_)
	if result1_ < result_prev_:
		return rotate_pts_,degs_+d_deg_,x_+d_x_,y_+d_y_,result1_,True
	else:
		return movable_pts_,degs_,x_,y_,result_prev_,False

def mdif(a,b):
	return (np.sqrt((a[:,0]-b[:,0])**2+(a[:,1]-b[:,1])**2)).mean()




result_prev_ = 1000**2
scale_ = 1
x_ = 0; y_ = 0; degs_ = 0
i0_ = 306
for i_ in range(i0_,len(ts_)):
	print i_
	t_ = ts_[i_]
	if t_ in L.keys():
		Q = L[t_]
		mi(F[left_image][vals][i_])
		figure(3)
		clf()
		N=6
		xylim(-N,N,-N,N)
		plt_square()
		pts_ = []
		ks_ = []
		for k_ in Q['angles_to_center'].keys():
			if k_ in Marker_xy_dic.keys():
				ks_.append(k_)
				p0_ = [0,Q['distances_marker'][k_]]
				p1_ = rotatePoint([0,0],p0_,-np.degrees(Q['angles_to_center'][k_])*(80/180.0))
				pts_.append(p1_)
		pts_ = np.array(pts_)
		figure(2);clf();xylim(-N,N,-N,N);plt_square();#pts_plot(pts_);pts_plot(new_pts_,'b');plot(0,0,'ok')

		mpts_ = []
		for k_ in Marker_xy_dic.keys():
			plt.annotate(str(k_),Marker_xy_dic[k_])
			mpts_.append(Marker_xy_dic[k_])
		pts_plot(np.array(mpts_),'g')

		actual_pts_ = []
		for i_ in rlen(ks_):
			k_ = ks_[i_]
			actual_pts_.append(Marker_xy_dic[k_])	
		for i_ in range(100):
			new_pts_,degs_,x_,y_,result_,new_ = mn2(result_prev,result_prev_, movable_pts,pts_, static_pts,actual_pts_,degs,degs_,x,x_,y,y_, scale,i_*scale_/(50.0))
			if result_ > result_prev_:
				assert(False)
			result_prev_ = result_
			if new_:
				#pts_plot(np.array(new_pts_),'b');pause(0.00001)
				pass#print result_
			else:
				pass#print result_,False
		new_pts_ = rotate_translate_polygon(pts,pts_, deg,degs_, x,x_, y,y_)
		pts_plot(np.array(new_pts_),'r');plot(x_,y_,'kx');pause(0.01)

		print 1,dp(degs_)



"""
def mn(*args):
	Args = args_to_dictionary(args)
	movable_pts_ = np.array(Args[movable_pts])
	static_pts_ = np.array(Args[static_pts])
	True
	rotate_pts_ = rotate_translate_polygon(pts,movable_pts_, deg,np.random.randn(1)[0]*5, x,np.random.randn(1)[0]*0.1, y,np.random.randn(1)[0]*0.1)
	if mdif(rotate_pts_,static_pts_) < mdif(movable_pts_,static_pts_):
		return rotate_pts_,True
	return movable_pts_,False
"""






#EOF
