#!/usr/bin/env python 
from kzpy3.vis2 import *
import kzpy3.Grapher_app.Graph_Image_Module as Graph_Image_Module





p1=[199,200,202,203]	#
p2=[204,205,208,206]	# K
p3=[174,175,176,177]	# J
p4=[57,58,67,59]		# I
p5=[173,172,171,170]	# H
p6=[227,226,228,225]	# G
p7=[153,152,151,150]	# F
p8=[134,133,139,138]	# E
p9=[216,217,218,219]	# D
p10=[223,222,221,220]	# C
p11=[169,168,167,165]	# B
p12=[207,209,210,211]	# A



markers_clockwise = p4+p5+p6+p7+p8+p9+p10+p11+p12   +    p2+p3

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
	x = 2*107/100.*np.sin(a)
	y = 2*107/100.*np.cos(a)
	marker_xys.append([x,y])
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


graphics = True

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

	Gi = Graph_Image_Module.Graph_Image(xmin,x_min,ymin,y_min,xmax,x_max,ymax,y_max,xsize,350,ysize,350)
	Gi[ptsplot]('x',pts[:,0],'y',pts[:,1],color,(255,0,0))
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


