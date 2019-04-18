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








Marker_xy_dic = {}
marker_angles = 2*np.pi*np.arange(len(markers_clockwise))/(1.0*len(markers_clockwise))

for i in range(len(markers_clockwise)):
	m = markers_clockwise[i]
	a = marker_angles[i]
	marker_angles_dic[markers_clockwise[i]] = a
	x = 4*107/100.*np.sin(a)
	y = 4*107/100.*np.cos(a)
	xy = na([x,y])
	b=0.0234
	x_left =  4*107/100.*np.sin(a-b)
	x_right = 4*107/100.*np.sin(a+b)
	y_left =  4*107/100.*np.cos(a-b)
	y_right = 4*107/100.*np.cos(a+b)
	Marker_xy_dic[m] = xy
	Marker_xy_dic[(m,'left')] = na([x_left,y_left])
	Marker_xy_dic[(m,'right')] = na([x_right,y_right])
	#print length(na([x_left,y_left])-na([x_right,y_right]))

figure(1)
clf()
plt_square()
ctr = 0
for m in markers_xy_dic:
	xy = Marker_xy_dic[(m,'left')]
	plot(xy[0],xy[1],'r.')
	xy = Marker_xy_dic[(m,'right')]
	plot(xy[0],xy[1],'b.')
	xy = Marker_xy_dic[m]
	plot(xy[0],xy[1],'xg')
	ctr += 1
	if ctr > 5:
		break



