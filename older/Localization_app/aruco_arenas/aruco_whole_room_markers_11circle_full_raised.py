#!/usr/bin/env python 
from kzpy3.vis2 import *
graphics = True
if graphics and 'nvidia' not in opjh():
	from kzpy3.Grapher_app.Graph_Image_Module import *





p2=[182,183,184,201]	# + door
p3=[178,179,180,181]	# J
p4=[66,70,64,65]	# +
p5=[51,50,4,63]	# H
p6=[154,155,156,157]	# +
p7=[52,189,192,191]	# F
p8=[146,147,148,149]	# E fireplace
p9=[132,137,136,135]	# +
p10=[199,200,202,203]	# C
p11=[215,212,213,214]		# +
p12=[198,196,197,194]	# A windows



markers_clockwise = p4+p5+p6+p7+p8+p9+p10+p11+p12+p2+p3
markers_clockwise.reverse() # because panels turned upside down
mc = markers_clockwise

na = np.array

marker_spacing = 107/4.0/100.0
marker_width = 21/100.0

north = marker_spacing * na([0,1.])
north_east = na(rotatePoint((0,0),north,-45))
north_west = na(rotatePoint((0,0),north,45))
north_west2 = na(rotatePoint((0,0),north,49))
east = na(rotatePoint((0,0),north,-90))
south = na(rotatePoint((0,0),north,-180))
south_east = na(rotatePoint((0,0),north,-138))
south_west = na(rotatePoint((0,0),north,-225))
south_west1 = na(rotatePoint((0,0),north,-228))
south_west2 = na(rotatePoint((0,0),north,-222))
west = na(rotatePoint((0,0),north,-270))



FIRST_MARKER = 'FIRST_MARKER'
LEFT = 'left'
RIGHT = 'right'
LEFT2 = 'LEFT2'
RIGHT2 = 'RIGHT2'



Marker_xy_dic = {}
Marker_headings = {}

marker_angles_dic = {}
marker_angles = 2*np.pi*np.arange(len(markers_clockwise))/(1.0*len(markers_clockwise))
marker_xys = []
for i in range(len(markers_clockwise)):
	a = marker_angles[i]
	marker_angles_dic[markers_clockwise[i]] = a
	x_ = 2*107/100.*np.sin(a)
	y_ = 2*107/100.*np.cos(a)
	marker_xys.append([x_,y_])
markers_xy_dic = {}
assert(len(markers_clockwise) == len(marker_xys))
for i in range(len(markers_clockwise)):
	m = markers_clockwise[i]
	xy = marker_xys[i]
	Marker_xy_dic[m] = xy


"""
Marker_xy_dic[0] = na([0.21,-(0.82+marker_width)])
Marker_xy_dic[100] = Marker_xy_dic[0] - na([0,1.1*marker_width])
Marker_xy_dic[102] =  na([-0.12,-0.12]) + Marker_xy_dic[0]
Marker_xy_dic[11] = na([0.12,-0.11]) + Marker_xy_dic[0]
"""
"""
D[100] = ((),south)
D[0] = ((),north)
D[11] = ((),east)
D[102] = ((),west)
"""


for k in Marker_xy_dic.keys():
	xy = na(Marker_xy_dic[k])
	Marker_xy_dic[(k,LEFT)] = xy+na(rotatePoint((0,0),xy,95))/(2*107/100.)*marker_width/2.0#/marker_spacing
	Marker_xy_dic[(k,RIGHT)] = xy-na(rotatePoint((0,0),xy,85))/(2*107/100.)*marker_width/2.0#/marker_spacing




if graphics and 'nvidia' not in opjh():
	#from kzpy3.Grapher_app.Graph_Image_Module import *
	pts = []
	figure('arena');clf();plt_square();#xylim(-0.1,0.6,-0.1,0.6)#xysqlim(1.)
	for k in Marker_xy_dic:
		pts_plot(na([Marker_xy_dic[k]]))
		if is_number(k):
			
			txt = str(k)
			plt.annotate(txt,Marker_xy_dic[k])
			pts.append(Marker_xy_dic[k])
			left_pt = Marker_xy_dic[(k,LEFT)]
			right_pt = Marker_xy_dic[(k,RIGHT)]
			pts.append(left_pt)
			pts.append(right_pt)
			plot([left_pt[0],right_pt[0]],[left_pt[1],right_pt[1]],'g')
		elif not is_number(k):
			txt = str(k[1])
			if '2' not in txt:
				plt.annotate(d2s(k),Marker_xy_dic[k])

	pts = np.array(pts)
	x_min = -(6.03/2.0)
	x_max = (6.03/2.0)
	y_min = -(6.03/2.0)
	y_max = 6.03/2.0

	Gi = Graph_Image(xmin,x_min,ymin,y_min,xmax,x_max,ymax,y_max,xsize,350,ysize,350)
	Gi[ptsplot](x,pts[:,0],y,pts[:,1],color,(255,0,0))
	mi(Gi[img],3)
	figure(4)
	pts = []
	for k in Marker_xy_dic.keys():
		if not is_number(k):
			pts.append(Marker_xy_dic[k])
	pts = na(pts)
	pts_plot(pts,'r')
	#raw_enter()


#EOF

