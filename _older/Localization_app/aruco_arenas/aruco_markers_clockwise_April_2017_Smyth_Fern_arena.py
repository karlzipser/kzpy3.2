from kzpy3.utils2 import *
from kzpy3.vis2 import *


markers_clockwise = [56,
62,
55,
61,

134,
133,
139,
138,

199,
200,
202,
203,

204,
205,
208,
206,

174,
175,
176,
177,

57,
58,
67,
59,

173,
172,
171,
170,

5,
53,
54,
60,

153,
152,
151,
150,

169,
168,
167,
165,

207,
209,
210,
211,

154,
155,
156,
157,

215,
212,
213,
214,

227,
226,
228,
225,

216,
217,
218,
219,

223,
222,
221,
220,

66,
70,
64,
65,

132,
137,
136,
135,

198,
196,
197,
194,

140,
141,
143,
142,

68,
69,
74,
6,

162,
163,
164,
166,

229,
131,
144,
145,

190,
188,
193,
195,

48,
46,
49,
47,

161,
160,
159,
158]








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
assert(len(markers_clockwise) == len(marker_xys))
for i in range(len(markers_clockwise)):
	m = markers_clockwise[i]
	xy = marker_xys[i]
	markers_xy_dic[m] = xy

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


figure(1)
clf()
plt_square()
for m in markers_xy_dic:
	xy = markers_xy_dic[m]
	plot(xy[0],xy[1],'.')
title(P[MARKER_SETUP])