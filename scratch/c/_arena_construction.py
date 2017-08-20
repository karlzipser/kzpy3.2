#!/usr/bin/env python 
from kzpy3.vis2 import *

na = np.array

marker_spacing = 107/4.0/100.0
marker_width = 21/100.0

north = marker_spacing * na([0,1.])
north_east = na(rotatePoint((0,0),north,-45))
east = na(rotatePoint((0,0),north,-90))
south = na(rotatePoint((0,0),north,-180))
south_east = na(rotatePoint((0,0),north,-135))
south_west = na(rotatePoint((0,0),north,-225))
west = na(rotatePoint((0,0),north,-270))

m0 = 0
m1 = 1
m2 = 2
m3 = 3
m4 = 4
m5 = 5
m6 = 6
m7 = 7
m8 = 8
m9 = 9
m10 = 10
m11 = 11
m12 = 12
m13 = 13



FIRST_MARKER = 'FIRST_MARKER'
LEFT = 'left'
RIGHT = 'right'
LEFT2 = 'LEFT2'
RIGHT2 = 'RIGHT2'
D = {
	m0:((FIRST_MARKER,na([0.,0.])),north),
	m1:((m0,[west]),north),
	m2:((m1,[west]),north),
	m3:((m2,[west]),north),
	m4:((m3,[west/2.,north/2.]),east),
	m5:((m4,[north]),east),
	m6:((m5,[north/2.0,east/2.0]),south),
	m7:((m6,[east]),south),
	m8:((m7,[east]),south),
	m9:((m8,[north*0.35,east*0.14,south_east]),south_west),
	m10:((m9,[south_east]),south_west),

}

Marker_xy_dic = {}

for k in D:
	if D[k][0][0] == FIRST_MARKER:
		first_marker = k
		break

Marker_xy_dic[first_marker] = D[first_marker][0][1]
k_prev = first_marker
for k in D:
	if D[k][0][0] == k_prev:
		Marker_xy_dic[k] = Marker_xy_dic[k_prev].copy()
		for d in D[k][0][1]:

			Marker_xy_dic[k] += d
		print k,dp(d[0]),dp(d[1]), Marker_xy_dic[k]
		k_prev = k


for k in D:
	marker_heading = D[k][1]
	Marker_xy_dic[(k,LEFT)] = Marker_xy_dic[k] + marker_width/2.0/marker_spacing * na(rotatePoint((0,0),marker_heading,90))
	Marker_xy_dic[(k,RIGHT)] = Marker_xy_dic[k] + marker_width/2.0/marker_spacing * na(rotatePoint((0,0),marker_heading,-90))
	Marker_xy_dic[(k,LEFT2)] = Marker_xy_dic[k] + 1/2.0 * na(rotatePoint((0,0),marker_heading,90))
	Marker_xy_dic[(k,RIGHT2)] = Marker_xy_dic[k] + 1/2.0 * na(rotatePoint((0,0),marker_heading,-90))





figure('arena');clf();plt_square();#xylim(-0.1,0.6,-0.1,0.6)#xysqlim(1.)
for k in Marker_xy_dic:
	pts_plot(na([Marker_xy_dic[k]]))
	if is_number(k):
		txt = str(k)
		plt.annotate(txt,Marker_xy_dic[k])
		left_pt = Marker_xy_dic[(k,LEFT2)]
		right_pt = Marker_xy_dic[(k,RIGHT2)]
		plot([left_pt[0],right_pt[0]],[left_pt[1],right_pt[1]],'b')
		left_pt = Marker_xy_dic[(k,LEFT)]
		right_pt = Marker_xy_dic[(k,RIGHT)]
		plot([left_pt[0],right_pt[0]],[left_pt[1],right_pt[1]],'g')
	else:
		txt = str(k[1])
		if '2' not in txt:
			plt.annotate(txt,Marker_xy_dic[k])






#raw_enter()


#EOF


