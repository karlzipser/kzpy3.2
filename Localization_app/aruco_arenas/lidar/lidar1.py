
if False:
	"""
	KERNEL=="ttyUSB*", MODE="0666"
	sudo chmod 666 /dev/ttyUSB0
	roslaunch rplidar_ros rplidar.launch

	sleep 10;rostopic echo -n 100 -w 5 /scan/ranges > ~/Desktop/ranges2.txt

	inf = 3.0
	plt.polar(np.radians(range(360)),a,'.')
	"""






# https://stackoverflow.com/questions/20924085/python-conversion-between-coordinates
import numpy as np
from kzpy3.Grapher_app.Graph_Image_Module import *


def cart2pol(x, y):
	rho = np.sqrt(x**2 + y**2)
	phi = np.arctan2(y, x)
	return rho, phi
def pol2cart(rho, phi):
	x = rho * np.cos(phi)
	y = rho * np.sin(phi)
	return x,y


path = '/home/karlzipser/kzpy3/Localization_app/data/ranges1.txt'
name = fname(path.split('.')[0])
a=txt_file_to_list_of_strings(path)  
b=[]
for c in a:                                                             
	if '---' not in c:
		b.append(c)
d = 'inf = -999\n\nranges = ['
for e in b:
	d += e+',\n\n'
d += ']'
exec(d)
f = na(ranges)

fig = figure(1);clf()
Angle_dic = {}
for i in range(shape(f)[0]):
	for j in range(360):

		h = f[i,j]
		if h > 0:
			if j not in Angle_dic:
				Angle_dic[j] = []
				Angle_dic[j].append(h)
Ranges_dic = {}
for i in Angle_dic.keys():
	Ranges_dic[i] = np.median(Angle_dic[i])

xy = []
for j in sorted(Ranges_dic.keys()):
	k = Ranges_dic[j]
	r = np.radians(j)
	xy.append(pol2cart(k,r))
xy = na(xy)
figure(1);clf();plt_square();pts_plot(xy,'b')
if False:
	so(xy,opjD('xy_'+name+'.pkl'))



Cdat = Click_Data(FIG=fig)
xy_list = Cdat[CLICK](NUM_PTS=11)
pts_plot(na(xy_list),'r')

xy_list.append(xy_list[0])

for i in range(len(xy_list)-1):
	pd2s('panel',i+1,'left:',xy_list[i],'right',xy_list[i+1])




paper = 8.5*2.54
edge = 2*2.54
space = (108-2*edge-4*8.5*2.54)/3.0
additions = [edge,paper,space,paper,space,paper,space,paper]
panel_with_marker_pts = []
pt_prev = 0
for a in additions:
	panel_with_marker_pts.append([a+pt_prev,0,0])
	pt_prev = panel_with_marker_pts[-1][0]
panel_with_marker_pts = np.matrix(panel_with_marker_pts)/100.0




#figure(2);plt_square();

def fit_markers(left_pt=None,right_pt=None):

	xy = na([42.5*2.54/100.0,0])
	moving_pts_2d = [0*xy,0.333*xy,0.9*xy,xy]
	stationary_pts_2d = [left_pt,left_pt+0.333*(right_pt-left_pt),left_pt+0.9*(right_pt-left_pt),right_pt]
	moving,stationary = [],[]
	for p in moving_pts_2d:
		moving.append(list(p)+[0])
	for p in stationary_pts_2d:
		stationary.append(list(p)+[0])
	ret_R,ret_t = rigid_transform_3D(moving,stationary)
	moving = np.matrix(moving)
	fitted = (ret_R*moving.T) + np.tile(ret_t,(1,len(moving)))
	fitted = fitted.T
	fitted = na(fitted)[:,:2]

	
	fitted_markers = (ret_R*panel_with_marker_pts.T) + np.tile(ret_t,(1,len(panel_with_marker_pts)))
	fitted_markers = fitted_markers.T
	fitted_markers = na(fitted_markers)[:,:2]

	pts_plot(na(stationary)[:,:2],'r')								
	pts_plot(na(moving)[:,:2],'b')								
	pts_plot(na(fitted),'g')								
	pts_plot(na(fitted_markers),'k')								
	return na(fitted_markers)


fitted_markers = []
for i in range(len(xy_list)-1):
	left_pt = na(xy_list[i])
	right_pt = na(xy_list[i+1])
	fitted_markers.append( fit_markers(left_pt=left_pt,right_pt=right_pt) )

fitted_markers_ = []
for f in fitted_markers:
	for p in f:
		fitted_markers_.append(p)

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

Marker_xy_dic = {}
pt_ctr = 0
for m in markers_clockwise:
	for s in ['left','right']:
		Marker_xy_dic[(m,s)] = fitted_markers_[pt_ctr]
		pt_ctr += 1
	Marker_xy_dic[m] = (Marker_xy_dic[(m,'left')]+Marker_xy_dic[(m,'right')])/2.0


pts = []
figure('arena');clf();plt_square();#xylim(-0.1,0.6,-0.1,0.6)#xysqlim(1.)
for k in Marker_xy_dic:
	pts_plot(na([Marker_xy_dic[k]]))
	if is_number(k):
		
		txt = str(k)
		plt.annotate(txt,Marker_xy_dic[k])
		pts.append(Marker_xy_dic[k])
		left_pt = Marker_xy_dic[(k,'left')]
		right_pt = Marker_xy_dic[(k,'right')]
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

#EOF