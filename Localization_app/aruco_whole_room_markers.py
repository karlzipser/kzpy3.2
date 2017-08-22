#!/usr/bin/env python 
from kzpy3.vis2 import *

p1=[199,200,202,203]
p2=[204,205,208,206]
p3=[174,175,176,177]
p4=[57,58,67,59]
p5=[173,172,171,170]

p6=[227,226,228,225]
p7=[153,152,151,150]
p8=[134,133,139,138]
p9=[216,217,218,219] 

p10=[223,222,221,220]
p11=[169,168,167,165]
p12=[207,209,210,211]
p13=[132,137,136,135]
p14=[161]

p15=[55,61]

p16=[160,159,158]

p17=[182,183,184,201]

p18=[51,50,4,63]
p19=[146,147,148,149]

p20=[52,189,192,191]

markers_clockwise = p1+p2+p3+p4+p5+p6+p7+p8+p9+p10+p11+p12+p13+p14+p15+p16+p17+p18+p19+p20
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

# South Wall
D = {
	mc[0]:((FIRST_MARKER,na([3.076,-8*marker_spacing])),north)
}
for i in range(1,4*5):
	D[mc[i]] = ((mc[i-1],[west]),north)

# West Wall
D[mc[i+1]] = ((mc[i],[west/2.,north/2.]),east)
for j in range(i+2,i+17):
	D[mc[j]] = ((mc[j-1],[north]),east)


# North Wall
D[mc[j+1]] = ((mc[j],[north/2.0,east/2.0]),south)
for k in range(j+2,j+18):
	D[mc[k]] = ((mc[k-1],[east]),south)

# East Wall segment 1
D[mc[k+1]] = ((mc[k],[south/2.0,east/2.0]),west)
for l in range(k+2,k+3):
	D[mc[l]] = ((mc[l-1],[south]),west)


# East Wall segment 2
D[mc[l+1]] = ((mc[l],[south/2.0,east/2.0]),south)
for m in range(l+2,l+4):
	D[mc[m]] = ((mc[m-1],[east]),south)

# East Wall segment 3
D[mc[m+1]] = ((mc[m],[0.55*south_east,0.45*east]),south_west)
for n in range(m+2,m+5):
	D[mc[n]] = ((mc[n-1],[south_east]),south_west1)

# East Wall segment 4
D[mc[n+1]] = ((mc[n],[south*0.85,0.355*east]),west)
for o in range(n+2,n+9):
	D[mc[o]] = ((mc[o-1],[south]),west)

# East Wall segment 5
D[mc[o+1]] = ((mc[o],[0.85*south,0.335*west]),north_west)
for p in range(o+2,o+5):
	D[mc[p]] = ((mc[p-1],[south_west2]),north_west2)


Marker_xy_dic = {}

for k in D:
	if D[k][0][0] == FIRST_MARKER:
		first_marker = k
		break

Marker_xy_dic[first_marker] = D[first_marker][0][1]
k_prev = first_marker
for k in markers_clockwise:
	if k in D:
		if D[k][0][0] == k_prev:
			Marker_xy_dic[k] = Marker_xy_dic[k_prev].copy()
			for d in D[k][0][1]:
				Marker_xy_dic[k] += d
			#print k,dp(d[0]),dp(d[1]), Marker_xy_dic[k]
			k_prev = k


Marker_xy_dic[0] = na([0.21,0.82+marker_width])
Marker_xy_dic[100] = Marker_xy_dic[0] - na([0,1.1*marker_width])
Marker_xy_dic[102] =  na([-0.12,-0.12]) + Marker_xy_dic[0]
Marker_xy_dic[11] = na([0.12,-0.11]) + Marker_xy_dic[0]
D[100] = ((),south)
D[0] = ((),north)
D[11] = ((),east)
D[102] = ((),west)



for k in D:
	marker_heading = D[k][1]
	Marker_xy_dic[(k,LEFT)] = Marker_xy_dic[k] + marker_width/2.0/marker_spacing * na(rotatePoint((0,0),marker_heading,-90))
	Marker_xy_dic[(k,RIGHT)] = Marker_xy_dic[k] + marker_width/2.0/marker_spacing * na(rotatePoint((0,0),marker_heading,90))
	Marker_xy_dic[(k,LEFT2)] = Marker_xy_dic[k] + 1/2.0 * na(rotatePoint((0,0),marker_heading,-90))
	Marker_xy_dic[(k,RIGHT2)] = Marker_xy_dic[k] + 1/2.0 * na(rotatePoint((0,0),marker_heading,90))


rotating_keys = []
rotating_vals = []
for k in Marker_xy_dic:
	rotating_keys.append(k)
	rotating_vals.append(Marker_xy_dic[k])
rotating_vals = rotatePolygon(rotating_vals,180)
rotating_vals = na(rotating_vals)
rotating_vals[:,0] -= (rotating_vals[:,0].max()+rotating_vals[:,0].min())/2.0

for k,v in zip(rotating_keys,rotating_vals):
	Marker_xy_dic[k] = v



graphics = True

if graphics:
	from kzpy3.Grapher_app.Graph_Image_Module import *
	pts = []
	figure('arena');clf();plt_square();#xylim(-0.1,0.6,-0.1,0.6)#xysqlim(1.)
	for k in Marker_xy_dic:
		pts_plot(na([Marker_xy_dic[k]]))
		if is_number(k):
			txt = str(k)
			plt.annotate(txt,Marker_xy_dic[k])
			pts.append(Marker_xy_dic[k])
			left_pt = Marker_xy_dic[(k,LEFT2)]
			right_pt = Marker_xy_dic[(k,RIGHT2)]
			plot([left_pt[0],right_pt[0]],[left_pt[1],right_pt[1]],'b')
			left_pt = Marker_xy_dic[(k,LEFT)]
			right_pt = Marker_xy_dic[(k,RIGHT)]
			pts.append(left_pt)
			pts.append(right_pt)
			plot([left_pt[0],right_pt[0]],[left_pt[1],right_pt[1]],'g')
		else:
			txt = str(k[1])
			if '2' not in txt:
				plt.annotate(txt,Marker_xy_dic[k])

	pts = np.array(pts)
	x_min = -(6.03/2.0)#-6.03+hw
	x_max = (6.03/2.0)#hw
	y_min = -(6.03/2.0)#-hw#
	y_max = 6.03/2.0#hw#

	Gi = Graph_Image(xmin,x_min,ymin,y_min,xmax,x_max,ymax,y_max,xsize,350,ysize,250)
	Gi[ptsplot](x,pts[:,0],y,pts[:,1],color,(255,0,0))
	mi(Gi[img],3)
	figure(4)
	pts = []
	for k in Marker_xy_dic.keys():
		if not is_number(k):
			pts.append(Marker_xy_dic[k])
	pts = na(pts)
	pts_plot(pts,'r')
	raw_enter()


#EOF


