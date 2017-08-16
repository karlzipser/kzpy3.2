# 

def get_heading_centers(*args):
	Args = args_to_dictionary(args)
	Cs = lo(Args[aruco_cubic_splines])
	L = h5r(Args[left_timestamp_metadata])

	D = {}
	D[ts] = L[ts][:]
	D[motor] = L[motor][:]
	D[steer] = L[steer][:]
	D[state] = L[state][:]

	good_ts_ = []
	good_ts_indicies_ = []
	for i_ in rlen(D[ts]):
		t_ = D[ts][i_]
		if D[motor][i_] > 49:
			if D[state][i_] == 1:
				good_ts_.append(t_)
				good_ts_indicies_.append(i_)
	good_ts_ = na(good_ts_)
	good_motor_ = D[motor][good_ts_indicies_]
	good_steer_ = D[steer][good_ts_indicies_]


	x_ = (Cs[left][x_meo](good_ts_)+Cs[right][x_meo](good_ts_))/2.0
	y_ = (Cs[left][y_meo](good_ts_)+Cs[right][y_meo](good_ts_))/2.0
	figure(1)
	plot(good_ts_,x_,'.')
	plot(good_ts_,y_,'.')
	figure(2);clf();plt_square();xysqlim(2*107.0/100.0);
	plot(x_[100:],y_[100:],'.')

	hx_ = (Cs[left][hx_meo](good_ts_)+Cs[right][hx_meo](good_ts_))/2.0-(Cs[left][x_meo](good_ts_)+Cs[right][x_meo](good_ts_))/2.0
	hy_ = (Cs[left][hy_meo](good_ts_)+Cs[right][hy_meo](good_ts_))/2.0-(Cs[left][y_meo](good_ts_)+Cs[right][y_meo](good_ts_))/2.0

	figure(3)
	plot(good_ts_,hx_,'.')
	plot(good_ts_,hy_,'.')

	angle_clockwise_ = []
	for i_ in rlen(hx_):
		angle_clockwise_.append(angle_clockwise((0,1),(hx_[i_],hy_[i_])))
	angle_clockwise_ = na(angle_clockwise_)
	figure(4)
	plot(good_ts_,angle_clockwise_,'.')


	figure(5);clf();plt_square();xysqlim(2*107.0/100.0)
	for an_ in range(15,180+15,30):
		ox_=[];oy_=[]
		
		for i_ in range(0,len(hx_),5):
			if angle_clockwise_[i_] > an_-15 and angle_clockwise_[i_]<an_+15:
				ox_.append(x_[i_])
				oy_.append(y_[i_])
		plot(ox_,oy_,'.');spause()

	return {steer:good_steer_, motor:good_motor_, ts:good_ts_, angle:angle_clockwise_, x:x_, y:y_}





def join_dic_lists(*args):
	Args = args_to_dictionary(args)
	dic_list_ = Args[dic_list]
	True
	D = {}
	for k_ in dic_list_[0]:
		D[k_] = []
	for d_ in dic_list_:
		for k_ in D:
			print k_
			D[k_] += list(d_[k_])
	return D


Heading_centers1 = get_heading_centers(
	left_timestamp_metadata,opjD('bdd_car_data_July2017_LCR/h5py/direct_home_LCR_Aruco1_23Jul17_17h39m41s_Mr_Yellow/left_timestamp_metadata.h5py'),
	aruco_cubic_splines,opjD('meta/direct_home_LCR_Aruco1_23Jul17_17h39m41s_Mr_Yellow/Cubic_splines.pkl'))


Heading_centers2 = get_heading_centers(
	left_timestamp_metadata,opjD('bdd_car_data_July2017_LCR/h5py/direct_home_LCR_Aruco1_23Jul17_20h51m31s_Mr_Yellow/left_timestamp_metadata.h5py'),
	aruco_cubic_splines,opjD('meta/direct_home_LCR_Aruco1_23Jul17_20h51m31s_Mr_Yellow/Cubic_splines.pkl'))


Heading_centers = join_dic_lists(dic_list,[Heading_centers1,Heading_centers2])

	

arena_half_width_ = 2*107.0/100.0
from kzpy3.misc.nipy_utils import voronoi

a_=[]
a_i = []

the_range_ = arange(-arena_half_width_,arena_half_width_+arena_half_width_/99.,arena_half_width_/100.)
x_ctr = 0
for x_ in the_range_:
	y_ctr = 0
	for y_ in the_range_:
		a_.append((x_,y_))
		a_i.append((x_ctr,y_ctr))
		y_ctr += 1
	x_ctr += 1
a_=np.array(a_)

Imgs = {}
du_ = 30
for u_ in range(0,331,du_):
	print u_
	Heading_centers[angle] = na(Heading_centers[angle])
	indicies_ = np.where(np.logical_and(Heading_centers[angle]>max(u_-du_,0),Heading_centers[angle]<u_+du_))
	if u_-du_ < 0:
		
		indicies360_ = (np.where(Heading_centers[angle]>360+u_-du_))[0].tolist()
		indicies_ = indicies_[0].tolist()
		indicies_ += indicies360_
	H = {}

	for k_ in Heading_centers:
		H[k_] = list(na(Heading_centers[k_])[indicies_])

	"""
	the_range_ = arange(-arena_half_width_,arena_half_width_+arena_half_width_/2,arena_half_width_/3.)
	for x_ in the_range_:
		for y_ in the_range_:
			H[x].append(x_)
			H[y].append(y_)
			H[steer].append(49)
			H[motor].append(49)
	"""

	figure(1);clf();plt_square();xysqlim(2*107.0/100.0);
	pts_plot(na(a_))
	plot(H[x],H[y],'b.')
	pts_ = na([H[x],H[y]]).transpose()
	v_ = voronoi(a_,pts_)

	# get indicies of different headings

	img_ = np.zeros((202,202))
	for i_ in rlen(a_):
		c_ = v_[i_]
		img_[a_i[i_][0],a_i[i_][1]] = H[steer][c_]
	from scipy import ndimage

	img_ = imresize(img_,(8,8))
	img_=(z2o(img_)*99).astype(np.uint8)

	mi(img_,3);pause(0.01)
	Imgs[u_] = img_
	#raw_enter()
#
#
#
heading_steering_coordinates = lo(opjD('heading_steering_coordinates'))
wall_length = 4*107.0/100.0
#
def get_steer(*args):
	Args = args_to_dictionary(args);_=da
	x = _(Args,X)
	y = _(Args,Y)
	dx = _(Args,DX)
	dy = _(Args,DY)
	True
	a = angle_clockwise((0,1),(dx,dy))

	if a >= 345 or a < 15:
		binned_angle = 0;
	elif a >= 15 and a < 45:
		binned_angle = 30;
	elif a >= 45 and a < 75:
		binned_angle = 60
	elif a >= 75 and a < 105:
		binned_angle = 90
	elif a >= 105 and a < 135:
		binned_angle = 120
	elif a >= 135 and a < 165:
		binned_angle = 150
	elif a >= 165 and a < 195:
		binned_angle = 180
	elif a >= 195 and a < 225:
		binned_angle = 210
	elif a >= 225 and a < 255:
		binned_angle = 240
	elif a >= 255 and a < 285:
		binned_angle = 270
	elif a >= 285 and a < 315:
		binned_angle = 300
	elif a >= 315 and a < 345:
		binned_angle = 330;

	px = int(x*7.0/wall_length + 4.0)
	py = int(y*7.0/wall_length + 4.0)
	steer = heading_steering_coordinates[binned_angle][px,py]

	return steer
#
#
#








timer = Timer(0)
for i in range(100):
	ssh.exec_command(d2s("echo '(1.4,5.2,",i,")' > ~/Desktop/Mr_Color.txt "))
print timer.time()






















h = Heading_centers
Gi=Graph_Image(xmin,-hw, xmax,hw, ymin,-hw, ymax,hw, xsize,25, ysize,25, data_type,np.int)
xp,yp = Gi[floats_to_pixels](x,h[x],y,h[y])
for i in rlen(xp):
	Gi[img][xp[i],yp[i],:] += 1
g = Gi[img][:,:,0].copy()
t = 100
g[g>t]=t # set after looking at histogram
mi(1-z2o(g),1)
figure(2);clf();hist(g.flatten())
figure(3);clf();plot(h[x],h[y],'.')
x1,y1=Gi[floats_to_pixels](x,0.54,y,0.007, NO_REVERSE,True)
#g[x1,y1] =150
mi(z2o(g),4)

# insure pixels out of image set correctly
# make sure headings correspond to yesterday's heading directions

Da = {}
for a in range(360):
	ay = np.sin(np.radians(a))
	ax = np.cos(np.radians(a))
	Da[a]=[ax,ay]
"""
r=0.5
for a in arange(0,90,22.5):
	xya = na(Da[int(a)])*r
	x1,y1=Gi[floats_to_pixels](x,xya[0], y,xya[1], NO_REVERSE,True)
	g[x1,y1] =150
mi(z2o(g),5)
"""

# function, take position, heading, and test granularity and return angle/value pairs (sorted?)
# or return single angle with best value

x_pos = -1
y_pos = -1
heading = 135
heading_floats = []
headings = arange(heading-45,heading+45,22.5)
for a in headings:
	b = int(a)
	if b < 0:
		b = 360 + b
	elif b >= 360:
		b -= 360
	heading_floats.append(Da[b])
heading_floats = na(heading_floats)
r = 0.5
gg = g.copy()
x1,y1=Gi[floats_to_pixels](x,r*heading_floats[:,0]+x_pos, y,r*heading_floats[:,1]+y_pos, NO_REVERSE,True)
gg[x1,y1] = 0
mi(gg,6)


#EOF