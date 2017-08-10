from kzpy3.utils2 import *
from kzpy3.vis2 import *


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
ctr_ = -7.5
for k_ in Markers_clockwise['North']:
	Marker_xy_dic[k_] = [ctr_*marker_spacing_,-8*marker_spacing_]
	ctr_ += 1
ctr_ = -7.5
for k_ in Markers_clockwise['South']:
	Marker_xy_dic[k_] = [ctr_*marker_spacing_,8*marker_spacing_]
	ctr_ += 1
ctr_ = -7.5
for k_ in Markers_clockwise['East']:
	Marker_xy_dic[k_] = [-8*marker_spacing_,ctr_*marker_spacing_]
	ctr_ += 1
ctr_ = -7.5
for k_ in Markers_clockwise['West']:
	Marker_xy_dic[k_] = [8*marker_spacing_,ctr_*marker_spacing_]
	ctr_ += 1

pts = []
for k_ in Marker_xy_dic.keys():
	pts.append(Marker_xy_dic[k_])
figure(2);clf();plt_square();pts_plot(np.array(pts))




def get_camera_position(angles_to_center,angles_surfaces,distances_marker):
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
			#print (dp(np.degrees(marker_angles_dic[m]+np.pi/2.0-angles_surfaces[m]+angles_to_center[m]),2))#,dp(np.degrees(marker_angles_dic[m]),2),dp(np.degrees(angles_surfaces[m]),2),dp(np.degrees(angles_to_center[m],2)))
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



Q={'angles_surfaces': {138: 1.2496890515802406,
  216: 1.2304502402873205,
  217: 1.3127486308556253,
  218: 1.8040529215946637,
  219: 1.9538203601949251,
  220: 0.76371584047729324},
 'angles_to_center': {138: -1.2085845077652309,
  216: -0.84264398498218307,
  217: -0.52151679090575254,
  218: -0.18078284872212613,
  219: 0.15296201882677507,
  220: 1.0967007205999866},
 'distances_marker': {138: 1.4822421901775522,
  216: 1.5541935926105519,
  217: 1.5871800515715988,
  218: 1.6198948011118468,
  219: 1.6188416675292261,
  220: 0.74014715055300995}}



# https://stackoverflow.com/questions/4114921/vector-normalization?lq=1

import math

def magnitude(v):
    return math.sqrt(sum(v[i]*v[i] for i in range(len(v))))

def add(u, v):
    return [ u[i]+v[i] for i in range(len(u)) ]

def sub(u, v):
    return [ u[i]-v[i] for i in range(len(u)) ]

def dot(u, v):
    return sum(u[i]*v[i] for i in range(len(u)))

def normalize(v):
    vmag = magnitude(v)
    return [ v[i]/vmag  for i in range(len(v)) ]

if __name__ == '__main__':
    l = [1, 1, 1]
    v = [0, 0, 0]

    h = normalize(add(l, v))
    print h





figure(1)
clf()
plt_square()

a_ = 0
b_ = -90
c_ = -1.0
d_ = 1.0
e_ = 1
f_ = 1
g_ = -90
h_ = 0

marker_spacing = 107/4.0/100.0

m138x = 11.5*marker_spacing

Markers = {}
Markers[x]={138:m138x, 216:m138x+marker_spacing, 217:m138x+2*marker_spacing, 218:m138x+3*marker_spacing, 219:m138x+4*marker_spacing,220:m138x+4*marker_spacing+0.5*marker_spacing}
Markers[y]={138:16*marker_spacing, 216:16*marker_spacing, 217:16*marker_spacing, 218:16*marker_spacing, 219:16*marker_spacing,220:12*marker_spacing+0.5*marker_spacing}
Markers['angle']={138:a_, 216:a_, 217:a_, 218:a_, 219:a_,220:b_}
Markers['sign']={138:c_, 216:c_, 217:c_, 218:c_, 219:c_,220:d_}
Markers['sign2']={138:e_, 216:e_, 217:e_, 218:e_, 219:e_,220:f_}
Markers['angle2']={138:g_, 216:g_, 217:g_, 218:g_, 219:g_,220:h_}


# check if estimate is in space

for k in Markers[x].keys():
	plot(Markers[x][k],Markers[y][k],'o')
	p1 = [Markers[x][k],Markers[y][k]]
	p2 = [Markers[x][k],Markers[y][k]-Q['distances_marker'][k]]
	rp_ = rotatePoint(p1,p2,Markers['angle'][k]+Markers['sign'][k]*np.degrees(Q['angles_to_center'][k]))
	plot(rp_[0],rp_[1],'x')
	plot([Markers[x][k],rp_[0]],[  Markers[y][k],rp_[1]])
	rp2_ = rotatePoint(rp_,p1,Markers['angle2'][k]+Markers['sign2'][k]*np.degrees(Q['angles_surfaces'][k]))
	#plot([rp2_[0],rp_[0]],[rp2_[1],rp_[1]])
	v = np.array(rp2_) - np.array(rp_)
	vn = normalize(v)

	p3 = np.array(vn)/10.0+np.array(rp_)
	plot([rp_[0],p3[0]],[rp_[1],p3[1]])
#rotatePoint(centerPoint,point,angle)




