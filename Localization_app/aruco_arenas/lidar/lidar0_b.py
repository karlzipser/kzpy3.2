from kzpy3.vis2 import *
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
def cart2pol(x, y):
	rho = np.sqrt(x**2 + y**2)
	phi = np.arctan2(y, x)
	return rho, phi
def pol2cart(rho, phi):
	x = rho * np.cos(phi)
	y = rho * np.sin(phi)
	return x,y


path = opjD('ranges1.txt')
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



figure(2)
paper = 8.5*2.54
edge = 2*2.54
space = (108-2*edge-4*8.5*2.54)/3.0
additions = [edge,paper,space,paper,space,paper,space,paper]
panel_with_marker_pts = []
pt_prev = 0
for a in additions:
	panel_with_marker_pts.append([a+pt_prev,0,0])
	pt_prev = panel_with_marker_pts[-1][0]





left_pt = na([0,0])
right_pt = na([0,1.00])

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

panel_with_marker_pts = np.matrix(panel_with_marker_pts)/100.0
fitted_markers = (ret_R*panel_with_marker_pts.T) + np.tile(ret_t,(1,len(panel_with_marker_pts)))
fitted_markers = fitted_markers.T
fitted_markers = na(fitted_markers)[:,:2]

pts_plot(na(stationary)[:,:2],'r')								
pts_plot(na(moving)[:,:2],'b')								
pts_plot(na(fitted),'g')								
pts_plot(na(fitted_markers),'k')								




def Panel(**Args):
	left_pt,right_pt = Args[LEFT_PT],Args[RIGHT_PT]
	_ = {}


	return _

#EOF