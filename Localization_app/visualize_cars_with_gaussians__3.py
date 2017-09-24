
from kzpy3.Grapher_app.Graph_Image_Module import *
if Args['MARKERS'] == 'whole_room':
	from kzpy3.Localization_app.aruco_whole_room_markers_no_pillar import *
elif Args['MARKERS'] == 'circle':
	from kzpy3.Localization_app.aruco_whole_room_markers_12circle_no_pillar import *
else:
	assert(False)

pts_with_no_pillar = na(pts).copy()
from kzpy3.utils2 import *

#data_folder = opjD('bdd_car_data_Sept2017_aruco_demo_2')

data_folder = Args['DATA_FOLDER']

if 'BATCH' in Args:
	if Args['BATCH'] == 'True':
		for color in ['Blue','Lt_Blue','Orange','Black','Yellow','Purple']:
			os.system(d2s("xterm -hold -e python",opjh('kzpy3/Localization_app/visualize_cars_with_gaussians__3.py'),'MARKERS',Args['MARKERS'],'DATA_FOLDER',data_folder,'CAR_NAME','Mr_'+color,'&'))
			pause(2)
		raw_enter();
		exit()
		assert(False)



del pts
if Args['MARKERS'] == 'whole_room':
	from kzpy3.Localization_app.aruco_whole_room_markers import *
elif Args['MARKERS'] == 'circle':
	from kzpy3.Localization_app.aruco_whole_room_markers_12circle import *
else:
	assert(False)


pts_with_pillar = pts


half_angle = 45
radius = 0.5
the_delay = 1
bar_color = (255,0,0)
robot_steer_gain = 1.0
steer_momentum = 0.5
display_timer = Timer(10)

"""
if desired_direction == 'clockwise':
	dd = 0
else:
	dd = 1
"""
"""
def other_car_in_view(ax,ay,hx,hy,ox,oy,half_angle):
	#print ax,ay,hx,hy,ox,oy,half_angle
	ac = angle_clockwise((hx,hy),(ox-ax,oy-ay))
	if np.abs(ac) < half_angle or np.abs(ac) > (360-half_angle):
		return True
	return False
"""
def angle_dist_to_car(ax,ay,hx,hy,ox,oy,half_angle):
	#print ax,ay,hx,hy,ox,oy,half_angle
	car_angle = angle_clockwise((hx,hy),(ox-ax,oy-ay))
	car_dist = np.sqrt((ax-ox)**2+(ay-oy)**2)
	return car_angle,car_dist

Polar_Cartesian_dictionary = {}
Pc = Polar_Cartesian_dictionary
for a in range(360):
	ay = np.sin(np.radians(a))
	ax = np.cos(np.radians(a))
	Pc[a]=[ax,ay]

def angle_360_correction(angle):
	if angle < 0:
		angle = 360 + angle
	elif angle >= 360:
		angle -= 360
	if angle >= 0 and angle < 360:
		return angle
	else:
		return angle_360_correction(angle)


def get_headings(x_pos_input,y_pos_input,heading):
	heading_floats = []
	headings = arange(heading-45,heading+45,22.5/4.0).astype(np.int)
	for a in headings:
		b = angle_360_correction(int(a))
		heading_floats.append(Pc[b])
	heading_floats = na(heading_floats)
	return headings,heading_floats


def get_best_heading(x_pos,y_pos,heading,radius,Potential_graph):
	headings,heading_floats = get_headings(x_pos,y_pos,heading)
	middle_heading_index = int(len(headings)/2)
	x1,y1 = Potential_graph[floats_to_pixels](
		x,radius*heading_floats[:,1]+x_pos, y,radius*heading_floats[:,0]+y_pos, NO_REVERSE,False)
	min_potential = 9999
	min_potential_index = -9999
	potential_values = []
	for i in rlen(x1):
		p = Potential_graph[img][x1[i],y1[i],:].sum()
		#Potential_graph[img][x1[i],y1[i],:] = 255
		potential_values.append(p)
		if p < min_potential:
			min_potential = p
			min_potential_index = i
	return headings[min_potential_index],heading_floats,x1,y1,potential_values

Marker_xy_dic_numbers_only = {}
for k in Marker_xy_dic.keys():
	if is_number(k):
		Marker_xy_dic_numbers_only[k] = Marker_xy_dic[k]
def nearest_marker(x_pos,y_pos,Marker_xy_dic):
	min_dist = 999999
	min_id = None
	for k in Marker_xy_dic.keys():
		xy = Marker_xy_dic[k]
		dist_sq = (x_pos-xy[0])**2+(y_pos-xy[1])**2
		if min_dist > dist_sq:
			min_dist = dist_sq
			min_id = k
	min_dist = np.sqrt(min_dist)
	return min_id,min_dist

def angle_to_marker(x_pos,y_pos,h_x,h_y,marker_id,Marker_xy_dic):
	xy = Marker_xy_dic[marker_id]
	return angle_clockwise((h_x,h_y),(xy[0]-x_pos,xy[1]-y_pos))


def get_car_position_heading_validity(h5py_car_data_folder,car_position_dic_list,behavioral_mode,Aruco_steering_trajectories):
	L = h5r(opj(h5py_car_data_folder,'left_timestamp_metadata_right_ts.h5py'))
	O = h5r(opj(h5py_car_data_folder,'original_timestamp_data.h5py'))
	P = h5r(opj(h5py_car_data_folder,'position_data.h5py'))

	left_images = O[left_image][vals][:].copy()
	left_images = left_images.mean(axis=3)
	right_images = O[right_image][vals][:].copy()
	right_images = right_images.mean(axis=3)
	graphics = True
	CA()
	timer = Timer(0)

	n = [0]
	for i in range(1,shape(left_images)[0]):
		if i < len(right_images):
			ml = np.abs(left_images[i]-left_images[i-1]).mean()
			mr = np.abs(right_images[i]-right_images[i-1]).mean()
			n.append((ml+mr)/2.0)
		else:
			ml = np.abs(left_images[i]-left_images[i-1]).mean()
			n.append(ml)			

	pause_flag = False
	t = P['t'][:] #;print(len(t));raw_enter()
	ax = P['ax'][:]
	ay = P['ay'][:]
	hx = P['hx'][:]
	hy = P['hy'][:]
	o_meo = P['o_meo'][:]

	steer_prev = 49

	if graphics:
		Gi_size = 100
		m = 6
		x_min = -m
		x_max = m
		y_min = -m
		y_max = m
		time_counter = Timer(1/3.0)
		cv2.destroyAllWindows()
		
		Gi = Graph_Image(xmin,x_min,ymin,y_min,xmax,x_max,ymax,y_max,xsize,Gi_size,ysize,Gi_size)
		potential_image = np.zeros((100,100))
		car_potential_image = np.zeros((100,100))
		g5 = Gaussian_2D(20)
		g6 = Gaussian_2D(50)
		for mult in ([1.0,1.0],[0.3,0.01],[0.1,0.03],[1.2,1.5]):
			if mult[0] == 1.0:
				pts = pts_with_pillar
			else:
				pts = pts_with_no_pillar
			for p in pts:
				pix = Gi[floats_to_pixels](x,[mult[0]*p[0]],y,[mult[0]*p[1]])
				iadd(mult[1]*g5,potential_image,pix)
		potential_image_255 = (255*z2o(potential_image)).astype(np.int)
		mci(128+0*Gi[img],scale=6,title='map');
		mci(O[left_image][vals][0],scale=4,title='left_image')
		cv2.moveWindow('left_image',700,50)
		cv2.moveWindow('map',50,50)


		for i in range(0,len(left_images)-20):
			min_car_dist = 99999
			min_car_dist_angle = None
			j=i+20
			if o_meo[i] >1:

				Gi[img] *= 0
				Gi[img][:,:,2] = potential_image_255

				q = dp(t[j],1)
				car_potential_image *= 0.0
				for C in car_position_dic_list:
					if q in C['ax']:
						ox = C['ax'][q]
						oy = C['ay'][q]
						car_angle,car_dist = angle_dist_to_car(ax[j],ay[j],hx[j],hy[j],ox,oy,half_angle)

						other_car_in_view = False
						if np.abs(car_angle) < half_angle or np.abs(car_angle) > (360-half_angle):
							other_car_in_view = True
						if other_car_in_view:
							pix = Gi[floats_to_pixels](x,ox,y,oy)
							iadd(g6,car_potential_image,pix)
							if min_car_dist > car_dist:
								min_car_dist = car_dist
								min_car_dist_angle = car_angle
				car_potential_image_255 = (255*z2o(car_potential_image)).astype(np.int)
				Gi[img][:,:,0] = car_potential_image_255

				min_id,min_dist = nearest_marker(ax[j],ay[j],Marker_xy_dic_numbers_only)
				angle_to_nearest_marker = angle_to_marker(ax[j],ay[j],hx[j],hy[j],min_id,Marker_xy_dic_numbers_only)

				heading = angle_clockwise((0,1),(hx[j],hy[j]))

				direction = 'undefined'
				head_on = False
				if angle_to_nearest_marker > 330 or angle_to_nearest_marker < 30:
					head_on = True
				if angle_to_nearest_marker > 150 and angle_to_nearest_marker < 210:
					head_on = True
				if (heading < 180 and ay[j] < 0) or (heading > 180 and ay[j] > 0):
					direction = 'counter-clockwise'
				else:
					direction = 'clockwise'
				#print(min_id,dp(min_dist,1),int(heading),direction,head_on,(dp(ax[j],1),dp(ay[j],1)))
				#print(dp(min_car_dist,1),min_car_dist_angle)
				
				heading_new,heading_floats,x1,y1,potential_values = get_best_heading(ax[j],ay[j],heading,radius,Gi)
				heading_new_2,heading_floats_2,x1_2,y1_2,potential_values_2 = get_best_heading(ax[j],ay[j],heading,radius/2.0,Gi)
				heading_delta = (heading_new - heading)

				steer = heading_delta*(-99.0/45)
				steer = int((steer-49.0)*robot_steer_gain+49.0)

				if behavioral_mode == 'Follow_Arena_Potential_Field':
					if min_car_dist_angle != None:
						if min_car_dist > 0.0:
							if min_car_dist_angle < half_angle:
								ag = min_car_dist_angle
								steer = 49-ag
							elif min_car_dist_angle -360 > -half_angle:
								ag = min_car_dist_angle -360
								steer = 49-ag

				steer = min(99,steer)
				steer = max(0,steer)
				steer = int((1.0-steer_momentum)*steer+steer_momentum*steer_prev)

					
				steer_prev = steer

				potential_values = 1.0*na(potential_values)
				potential_values_2 = 1.0*na(potential_values_2)
				mx = potential_values.max()
				"""
				if desired_direction == 'counter-clockwise':
					clock_gradient = z2o(na(range(len(potential_values),0,-1)))
				else:
					clock_gradient = z2o(na(range(0,len(potential_values))))
				if desired_direction != direction:
					potential_values += 0.5*mx*clock_gradient
					mx = potential_values.max()
				"""
				try:
					motor = max(49,int(49+(65-49)*(0.8-potential_values.min()/(mx))))
				except:
					motor = 49
					pd2s('motor = 49 error,',fname(h5py_car_data_folder),' t =',timer.time())

				#figure(2);clf();ylim(0,1.1);plot(clock_gradient,'k');plot(potential_values/mx,'r.-');plot(potential_values_2/mx,'g.-');plot((potential_values-potential_values_2)/mx,'b.-');plt.title(d2s(steer,motor));spause()
				Gi[ptsplot](x,na([ax[j]]),y,na([ay[j]]),color,(255,255,255))
				Gi[ptsplot](x,na([hx[j]+ax[j]]),y,na([hy[j]+ay[j]]),color,(0,255,0))
				tmp = cv2.resize(Gi[img], (0,0), fx=6, fy=6, interpolation=0)
				cv2.putText(tmp,d2s(direction,head_on),(50,50),cv2.FONT_HERSHEY_SIMPLEX,1.0,(255,255,255),1)
				mci(tmp,scale=1,title='map',delay=the_delay);
				l_img = O[left_image][vals][i].copy()
				l_img[:40,:,:] = 128
				tmp = cv2.resize(l_img, (0,0), fx=4, fy=4, interpolation=0)
				apply_rect_to_img(tmp, steer, 0, 99, bar_color, bar_color, 0.9, 0.1, center=True, reverse=True, horizontal=True)
				apply_rect_to_img(tmp, motor, 0, 99, bar_color, bar_color, 0.9, 0.1, center=True, reverse=True, horizontal=False)
				cv2.putText(tmp,d2s(steer,motor,direction,head_on),(50,50),cv2.FONT_HERSHEY_SIMPLEX,1.0,(255,255,255),1)
				mci(tmp,scale=1,title='left_image',delay=the_delay)#;spause();
				pause_flag = False

				if direction == 'clockwise':
					dd = 0
				else:
					dd = 1
				Aruco_steering_trajectories[behavioral_mode][dd][t[i]] = {}
				Aruco_steering_trajectories[behavioral_mode][dd][t[i]]['steer'] = steer
				Aruco_steering_trajectories[behavioral_mode][dd][t[i]]['motor'] = motor
				#print(behavioral_mode,dd,steer,t[i])
			else:
				if not pause_flag:
					mci(128+0*O[left_image][vals][i],scale=4,title='left_image',delay=the_delay)
					pause(0.5)
					pause_flag = True
	L.close()
	O.close()
	P.close()



#desired_direction = 'counter-clockwise'

h5py_folder = opj(data_folder,'h5py')
unix(d2s("mkdir -p",opj(data_folder,'Aruco_Steering_Trajectories')))
#h5py_car_data_folder = opj(h5py_folder,'Mr_Blue_2017-09-02-14-55-25')#'Mr_Black_2017-09-04-17-05-28')#
# python kzpy3/Localization_app/visualize_cars_with_gaussians.py
#car_name ='Mr_Purple'# 'Mr_' + h5py_car_data_folder.split('/')[-1].split('_')[1]
print Args
car_name = Args['CAR_NAME']

car_position_dictionaries = sggo(data_folder,'position_dictionaries/*.pkl')
car_position_dic_list = []
print('car_position_dictionaries...')
for c in car_position_dictionaries:
	if car_name not in c:
		car_position_dic_list.append(lo(c))
print('...done')


success_count = 0
failure_count = 0
for h5py_car_data_folder in sggo(h5py_folder,'*'):
	if car_name in h5py_car_data_folder:
		Aruco_steering_trajectories = {}
		run_name = fname(h5py_car_data_folder)
		print run_name
		try:
			for behavioral_mode in ['Direct_Arena_Potential_Field','Follow_Arena_Potential_Field']:
				Aruco_steering_trajectories[behavioral_mode] = {}
				Aruco_steering_trajectories[behavioral_mode][0] = {}
				Aruco_steering_trajectories[behavioral_mode][1] = {}
				
				get_car_position_heading_validity(h5py_car_data_folder,car_position_dic_list,behavioral_mode,Aruco_steering_trajectories)

			so(opj(data_folder,'Aruco_Steering_Trajectories',run_name),Aruco_steering_trajectories)
			success_count += 1
		except Exception as e:
			print("********** get_car_position_heading_validity failed: Exception ***********************")
			print run_name
			print(e.message, e.args)
			failure_count += 0
		spd2s('success_count =',success_count,' failure_count =',failure_count)

		

spd2s('Done!')


















