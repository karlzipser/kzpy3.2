
import kzpy3.Grapher_app.Graph_Image_Module as Graph_Image_Module
from Parameters_Module import *
from kzpy3.vis2 import *

data_folder = Args['DATA_FOLDER']



if 'BATCH' in Args:
	if Args['BATCH'] == 'True':
		for car in P['CAR_LIST']:
			os.system(d2s("xterm -hold -e python",opjh('kzpy3/Localization_app/visualize_cars_with_gaussians__4.py'),'DATA_FOLDER',data_folder,'CAR_NAME',car,'&'))
			pause(2)
		raw_enter();
		exit()
		assert(False)

Marker_xy_dic = False
pkl_files = sggo(data_folder,'*.pkl')
for p in pkl_files:
	if 'Marker_xy_dic' in p:
		Marker_xy_dic = lo(p)
		break
assert(Marker_xy_dic != False)
pts = []
for k in Marker_xy_dic.keys():
	if not is_number(k):
		pts.append(Marker_xy_dic[k])
pts = na(pts)

half_angle = 60#45
radius = 0.5
the_delay = 1
bar_color = (255,0,0)
robot_steer_gain = 1.03125 # this is to correct for steer momentum of 0.75
steer_momentum = 0.75
display_timer = Timer(10)


def angle_dist_to_car(ax,ay,hx,hy,ox,oy,half_angle):
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
	headings = arange(heading-45,heading+46,22.5/4.0).astype(np.int)
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


def get_car_position_heading_validity(h5py_car_data_folder,car_position_dic_list,behavioral_mode,Aruco_steering_trajectories,observer):
	L = h5r(opj(h5py_car_data_folder,'left_timestamp_metadata_right_ts.h5py'))
	O = h5r(opj(h5py_car_data_folder,'original_timestamp_data.h5py'))
	Q = h5r(opj(h5py_car_data_folder,'aruco_position.h5py'))


	graphics = True
	CA()
	timer = Timer(0)

	pause_flag = False
	t = Q['ts'][:] 
	ax = Q['aruco_position_x'][:]
	ay = Q['aruco_position_y'][:]
	hx = Q['aruco_heading_x'][:] - ax #!!!!!! NOTE, this is different from pre-demo convention
	hy = Q['aruco_heading_y'][:] - ay #!!!!!! NOTE, this is different from pre-demo convention
	#o_meo = Q['o_meo'][:]

	steer_prev = 49

	if graphics:
		Gi_size = 100
		m = 6
		spd2s('m set to 10 or 6, =',m,'depending on arena type')
		
		x_min = -m
		x_max = m
		y_min = -m
		y_max = m
		time_counter = Timer(1/3.0)
		cv2.destroyAllWindows()
		
		Gi = Graph_Image_Module.Graph_Image(xmin,x_min,ymin,y_min,xmax,x_max,ymax,y_max,xsize,Gi_size,ysize,Gi_size)
		potential_image = np.zeros((100,100))
		car_potential_image = np.zeros((100,100))
		g1 = Gaussian_2D(2)
		g5 = Gaussian_2D(20)
		g6 = Gaussian_2D(50)
		for mult in ([1.0,1.0],[0.3,0.01],[0.1,0.03],[1.2,1.5]):

			for p in pts:
				pix = Gi[floats_to_pixels](x,[mult[0]*p[0]],y,[mult[0]*p[1]])
				iadd(mult[1]*g5,potential_image,pix)
		potential_image_255 = (255*z2o(potential_image)).astype(np.int)
		mci(128+0*Gi[img],scale=6,title='map');
		mci(O[left_image][vals][0],scale=4,title='left_image')
		cv2.moveWindow('left_image',700,50)
		cv2.moveWindow('map',50,50)


		for i in range(0,len(O[left_image][vals])):

			min_car_dist = 99999
			min_car_dist_angle = None
			#j=i+20  !!!!! What was this for?  This was a pre-demo correction for some live aruco analysis.
			j = i

			if i >= len(o_meo):
				spd2s("len(O[left_image][vals])",len(O[left_image][vals]),"len(o_meo)",len(o_meo))
				continue
			if o_meo[i]>1 or observer:
				print i
				Gi[img] *= 0
				Gi[img][:,:,2] = potential_image_255

				q = dp(t[j],1)
				car_potential_image *= 0.0
				other_car = False
				for C in car_position_dic_list:
					if q in C['ax']:
						ox = C['ax'][q]
						oy = C['ay'][q]
						ohx = C['hx'][q]-ox
						ohy = C['hy'][q]-oy
						ohx *= 5
						ohy *= 5

						car_angle,car_dist = angle_dist_to_car(ax[j],ay[j],hx[j],hy[j],ox,oy,half_angle)
						other_car_in_view = False
						if np.abs(car_angle) < half_angle or np.abs(car_angle) > (360-half_angle):
							other_car_in_view = True
						pix = Gi[floats_to_pixels](x,ox,y,oy)
						iadd(g1,car_potential_image,pix)
						if other_car_in_view:
							iadd(g6,car_potential_image,pix)
							if min_car_dist > car_dist:
								min_car_dist = car_dist
								min_car_dist_angle = car_angle


						car_angle,car_dist = angle_dist_to_car(ax[j],ay[j],hx[j],hy[j],ox-ohx,oy-ohy,half_angle)
						other_car_in_view = False
						if np.abs(car_angle) < half_angle or np.abs(car_angle) > (360-half_angle):
							other_car_in_view = True
						pix = Gi[floats_to_pixels](x,ox-ohx,y,oy-ohy)
						iadd(g1,car_potential_image,pix)
						if other_car_in_view:
							iadd(g5,car_potential_image,pix)
							if min_car_dist > car_dist:
								min_car_dist = car_dist
								min_car_dist_angle = car_angle

								other_car = True

				#if other_car == False:
				#	pass#continue # NOTE, DOES NOT HANDLE FOLLOW CASE

				
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

				
				heading_new,heading_floats,x1,y1,potential_values = get_best_heading(ax[j],ay[j],heading,radius,Gi)
				heading_new_2,heading_floats_2,x1_2,y1_2,potential_values_2 = get_best_heading(ax[j],ay[j],heading,radius/2.0,Gi)
				heading_delta = (heading_new - heading)

				steer = 99-99*(heading_delta + 45)/(44+45.0)

				
				if behavioral_mode == 'Follow_Arena_Potential_Field':
					if min_car_dist_angle != None:
						if min_car_dist > 0.0:
							if min_car_dist_angle < half_angle:
								ag = min_car_dist_angle
								steer = 49-ag
							elif min_car_dist_angle -360 > -half_angle:
								ag = min_car_dist_angle -360
								steer = 49-ag

				steer = int((1.0-steer_momentum)*(steer-49)+steer_momentum*(steer_prev-49)+49)
				steer = int((steer-49.0)*robot_steer_gain+49.0)
				steer = min(99,steer)
				steer = max(0,steer)
					
				steer_prev = steer

				potential_values = 1.0*na(potential_values)
				potential_values_2 = 1.0*na(potential_values_2)
				mx = potential_values.max()

				try:
					motor = max(49,int(49+(65-49)*(0.8-potential_values.min()/(mx))))
				except:
					motor = 49
					pd2s('motor = 49 error,',fname(h5py_car_data_folder),' t =',timer.time())

				Gi[ptsplot](x,na([ax[j]]),y,na([ay[j]]),color,(255,255,255))
				Gi[ptsplot](x,na([4*hx[j]+ax[j]]),y,na([4*hy[j]+ay[j]]),color,(0,255,0))

				tmp = cv2.resize(Gi[img], (0,0), fx=6, fy=6, interpolation=0)
				cv2.putText(tmp,d2s(direction,head_on),(50,50),cv2.FONT_HERSHEY_SIMPLEX,1.0,(255,255,255),1)
				mci(tmp,scale=1,title='map',delay=the_delay);
				l_img = O[left_image][vals][i].copy()
				l_img[:52,:,:] = 128 #47
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
			else:
				if not pause_flag:
					mci(128+0*O[left_image][vals][i],scale=4,title='left_image',delay=the_delay)
					pause(0.5)
					pause_flag = True
	L.close()
	O.close()
	Q.close()




h5py_folder = opj(data_folder,'h5py')
unix(d2s("mkdir -p",opj(data_folder,'Aruco_Steering_Trajectories')))

print Args
car_name = Args['CAR_NAME']

car_position_dictionaries = sggo(data_folder,'position_dictionaries/*.pkl')
car_position_dic_list = []
print('car_position_dictionaries...')
if True:
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
		if len(sggo(data_folder,'h5py',run_name,'observer.txt')) > 0:
			observer = True
			spd2s('Observer')
		else:
			observer = False
		if False:#run_name != 'Mr_Black_2017-10-23-11-53-40': #!!!!!!!!!!!!!!!!!!!! TEMP!!!!!!!!!!!!!!!!!!!!!!!!!!
			spd2s("if run_name != Mr_Black_2017-10-23-11-53-40: continue")
			continue
		if True:#try:
			for behavioral_mode in ['Direct_Arena_Potential_Field','Follow_Arena_Potential_Field']:
				Aruco_steering_trajectories[behavioral_mode] = {}
				Aruco_steering_trajectories[behavioral_mode][0] = {}
				Aruco_steering_trajectories[behavioral_mode][1] = {}
				spd2s(h5py_car_data_folder)
				get_car_position_heading_validity(h5py_car_data_folder,car_position_dic_list,behavioral_mode,Aruco_steering_trajectories,observer)

			so(opj(data_folder,'Aruco_Steering_Trajectories',run_name),Aruco_steering_trajectories)
			success_count += 1
		else:#except Exception as e:
			print("********** get_car_position_heading_validity failed: Exception ***********************")
			print run_name
			print(e.message, e.args)
			failure_count += 0
		spd2s('success_count =',success_count,' failure_count =',failure_count)

		

spd2s('Done!')


















