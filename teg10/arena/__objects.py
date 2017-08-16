from kzpy3.utils import *
pythonpaths(['kzpy3','kzpy3/teg9'])

import inspect


from vis import *
import data.utils.general
from data.utils.general import car_name_from_run_name
from data.utils.general import car_colors as colors
import data.utils.animate as animate


bair_car_data_location = '/Volumes/SSD_2TB/bair_car_data_new_28April2017'
bag_folders_dst_rgb1to4_path = opj(bair_car_data_location,'rgb_1to4')
bag_folders_dst_meta_path = opj(bair_car_data_location,'meta')

def Markers(markers_clockwise,radius):
	D = {}
	D['Purpose'] = d2s(inspect.stack()[0][3],':','Markers for the aruco arena.')
	D['clockwise'] = markers_clockwise
	D['ids_all'] = []
	D['angles_dic'] = {}
	D['angles'] = 2*np.pi*np.arange(len(markers_clockwise))/(1.0*len(markers_clockwise))
	D['xy'] = []
	for i in range(len(markers_clockwise)):
		a = D['angles'][i]
		D['angles_dic'][markers_clockwise[i]] = a
		x = radius*np.sin(a)
		y = radius*np.cos(a)
		D['xy'].append([x,y])
	D['xy_dic'] = {}
	assert(len(markers_clockwise) == len(D['xy']))
	def _cv2_draw(img):
		for j in range(len(D['clockwise'])):
			m = D['clockwise'][j]
			xy = D['xy'][j]
			D['xy_dic'][m] = xy
			c = (255,0,0)
			xp,yp = img['floats_to_pixels'](xy)
			cv2.circle(img['img'],(xp,yp),4,c,-1)
	D['cv2_draw'] = _cv2_draw
	return D










def Potential_Field(xy_sizes,origin,mult):
	D = {}
	D['Purpose'] = d2s(inspect.stack()[0][3],':','Potential field for path planning.')
	D['Image'] = Image(xy_sizes,origin,mult,data_type=np.float)
	D['previous_additions'] = []
	def _sub_add(additions):
		for p in D['previous_additions']:
			isub(p[0],D['Image']['img'],p[1])
		D['previous_additions'] = []
		for a in additions:
			D['add'](a[0],a[1])
	def _add(addition,xy):
		xy_pixels = D['Image']['floats_to_pixels'](xy)
		iadd(addition,D['Image']['img'],xy_pixels)
		D['previous_additions'].append([addition,xy_pixels])
	D['sub_add'] = _sub_add
	D['add'] = _add
	return D









def Arena_Potential_Field(origin,mult,markers):
	xy_sizes = [2*origin,2*origin]
	D = Potential_Field(xy_sizes,origin,mult)
	D['Purpose'] = d2f('\n',d2s(inspect.stack()[0][3],':','Potential field specific for arena.'),D['Purpose'])
	gau_marker = Gaussian_2D(mult)
	gau_s = Gaussian_2D(0.24*mult)
	gau_center = Gaussian_2D(6*mult)
	gau_follow = Gaussian_2D(12*mult)
	gau_car = Gaussian_2D(6*mult)
	for xy in markers['xy']:
		D['add'](gau_marker,xy)
		D['add'](-1.0*gau_s,xy)
		D['add'](2*gau_marker,1.05*(array(xy)))
		D['add'](3*gau_marker,1.1*(array(xy)))
		D['add'](4*gau_marker,1.15*(array(xy)))
	D['previous_additions'] = []
	def _test(iterations=1,Graphics=True):
		timer = Timer(0)
		ctr = 0
		for i in range(iterations):
			print (dp(timer.time(),2),ctr)
			for xy in markers['xy']:
				ctr += 1
				D['sub_add']([[-15*gau_follow,0.75*(array(xy))],[10*gau_marker,0.75*(array(xy))]])
				if Graphics:
					img = D['Image']['img']
					width = shape(img)[0]
					mi(img[width/2-origin/2:width/2+origin/2,width/2-origin/2:width/2+origin/2],1)
					figure(2);clf();plot(a['Image']['img'][Origin,:],'o-');pause(0.0001)
		print timer.time()
		print ctr
	D['test'] = _test
	def _other_cars(xy_list,follow=False):
		sub_add_list = []
		for xy in xy_list:
			if follow:
				sub_add_list.append([-15/6.5*gau_follow,array(xy)])
				sub_add_list.append([10/6.5*gau_car,array(xy)])
			else:
				sub_add_list.append([5/6.5*gau_car,array(xy)])
				sub_add_list.append([5/6.5*gau_marker,array(xy)])
		D['sub_add'](sub_add_list)
	D['other_cars'] = _other_cars
	return D


def Play_Arena_Potential_Field(origin,mult,markers):
	D = Arena_Potential_Field(origin,mult,markers)
	gau_center = Gaussian_2D(6*mult)
	for xy in markers['xy']:
		D['add'](gau_center,xy)
	D['previous_additions'] = []
	return D

def Follow_Arena_Potential_Field(origin,mult,markers):
	D = Arena_Potential_Field(origin,mult,markers)
	D['other_cars_parent'] = D['other_cars']
	def _other_cars(xy_list,follow=False):
		D['other_cars_parent'](xy_list,follow=True)
	D['other_cars'] = _other_cars
	return D

def Direct_Arena_Potential_Field(origin,mult,markers):
	gau_marker = Gaussian_2D(mult)
	gau_s = Gaussian_2D(0.24*mult)
	gau_center = Gaussian_2D(6*mult)
	gau_follow = Gaussian_2D(12*mult)
	gau_car = Gaussian_2D(6*mult)
	D = Arena_Potential_Field(origin,mult,markers)
	for xy in markers['xy']:
		D['add'](-1.0*gau_marker,0.75*(array(xy)))
	D['add'](4*gau_center,[0,0])
	D['previous_additions'] = []
	return D


def Furtive_Arena_Potential_Field(origin,mult,markers):
	gau_marker = Gaussian_2D(mult)
	gau_s = Gaussian_2D(0.24*mult)
	gau_center = Gaussian_2D(6*mult)
	gau_follow = Gaussian_2D(12*mult)
	gau_car = Gaussian_2D(6*mult)
	D = Arena_Potential_Field(origin,mult,markers)
	for xy in markers['xy']:
		D['add'](-1.0*gau_marker,0.92*(array(xy)))
	D['add'](4*gau_center,[0,0])
	D['previous_additions'] = []
	return D







def Car(N,car_name,origin,mult,markers):
	D = {}
	D['Purpose'] = d2s(inspect.stack()[0][3],':','Car object.')
	D['car_name'] = car_name
	D['potential_field'] = Arena_Potential_Field(origin,mult,markers)
	#D['xy'] = [0,0]
	D['runs'] = {}
	for run_name in N[car_name].keys():
		D['runs'][run_name] = {}
		R = D['runs'][run_name]
		R['trajectory'] = N[car_name][run_name]['self_trajectory']
		R['list_of_other_car_trajectories'] = []
		for ot in N[car_name][run_name]['other_trajectories']:
			other_run_name = ot['run_name']
			other_car_name = car_name_from_run_name(other_run_name)
			R['list_of_other_car_trajectories'].append( [other_car_name,other_run_name] )
	D['positions'] = {}
	D['near_i'] = 0
	D['near_t'] = 0
	def _rewind():
		D['near_i'] = 0
		D['near_t'] = 0	
		D['pts'] = []
	D['rewind'] = _rewind
	def _check_trajectory_point(traj,side,i,t):
		assert(traj['ts'][i] <= t)
		if traj['ts'][i] == t:
			if traj[side]['t_vel'][i] > 2: # 1.788: # Above 4 mph
				return False
			elif traj['camera_separation'][i] > 0.25: # almost larger than length of car
				return False
			elif traj[side]['timestamp_gap'][i] > 0.1: # missed data points
				return False
			elif length([traj[side]['x'][i],traj[side]['y'][i]]) > length(markers['xy'][0]):
				return False
			return True
		assert(False)
	def _valid_time_and_index(run_name,t):
		traj = D['runs'][run_name]['trajectory']
		if t>traj['ts'][0] and t<traj['ts'][-1]:
			near_t = -1
			for i in range(D['near_i'],len(traj['ts'])):
				if traj['ts'][i-1]<t and traj['ts'][i]>t:
					near_t = traj['ts'][i]
					near_i = i
					break
			if near_t > 0:
				D['near_i'] = near_i
				D['near_t'] = near_t
				for side in ['left','right']:
					if not _check_trajectory_point(traj,side,near_i,near_t):
						return False,False
				return near_t,near_i
		return False,False
	def _report_camera_positions(run_name,t):
		near_t,near_i = _valid_time_and_index(run_name,t)
		if not near_t:
			return False
		traj = D['runs'][run_name]['trajectory']
		positions = []
		for side in ['left','right']:
			positions.append([traj[side]['x'][near_i],traj[side]['y'][near_i]])
			D['pts'].append(positions[0])
		return positions
	D['report_camera_positions'] = _report_camera_positions
	def _get_left_image(run_name):
		traj = D['runs'][run_name]['trajectory']
		index = traj['data']['t_to_indx'][D['near_t']]
		img = traj['data']['left'][index]
		return img
	D['get_left_image'] = _get_left_image
	def _load_image_and_meta_data(run_name):
		import data.utils.general
		import data.utils.multi_preprocess_pkl_files_1
		D['runs'][run_name]['trajectory']['data'] = data.utils.general.get_new_Data_dic()
		data.utils.multi_preprocess_pkl_files_1.multi_preprocess_pkl_files(
			D['runs'][run_name]['trajectory']['data'],
				opj(bag_folders_dst_meta_path,run_name),
				opj(bag_folders_dst_rgb1to4_path,run_name))
	D['load_image_and_meta_data'] = _load_image_and_meta_data
	return D







	



def get_sample_points(pts,angles,pfield,n=3):

    sample_points = []
    potential_values = []

    heading = normalized_vector_from_pts(pts[-n:,:])
    heading *= 0.5 # 50 cm, about the length of the car
    if pts[-n,0] > pts[-1,0]:
        heading *= -1
    #if pts[-3,1] > pts[-1,1]:
    #    heading *= -1

    for a in angles:

        sample_points.append( rotatePoint([0,0],heading,a) )
    #figure(3)
    #pts_plot(pts)
    for k in range(len(sample_points)):
        f = sample_points[k]
        #plot([pts[-1,0],pts[-1,0]+f[0]],[pts[-1,1],pts[-1,1]+f[1]])
    #figure(1)
    for sp in sample_points:
        pix = meters_to_pixels(sp[0]+pts[-1,0],sp[1]+pts[-1,1])
        #plot(pix[0],pix[1],'kx')
        potential_values.append(pfield[pix[0],pix[1]])

    return sample_points,potential_values


def interpret_potential_values(potential_values):
    min_potential_index = potential_values.index(min(potential_values))
    max_potential_index = potential_values.index(max(potential_values))
    middle_index = int(len(potential_values)/2)

    d = 99.0/(1.0*len(potential_values)-1)
    steer_angles = np.floor(99-arange(0,100,d))
    dp = potential_values[max_potential_index] - potential_values[min_potential_index]
    
    p = min(1,dp/max( (0.6-max(0,potential_values[max_potential_index]-0.8)) ,0.2) )
    steer = 99-int((p*steer_angles[min_potential_index]+(1-p)*49.0))
    return steer




def meters_to_pixels(x,y):
    return (int(-Mult*x)+Origin),(int(Mult*y)+Origin)










if __name__ == "__main__":
	DISPLAY_LEFT = True

		

	angles = range(-30,31,10)

	if 'N' not in locals():
		print("Loading trajectory data . . .")
		N = lo(opjD('N_pruned.pkl'))
	from arena.markers_clockwise import markers_clockwise
	markers = Markers(markers_clockwise,4*107/100.)
	Origin = int(2*1000/300.*300 / 5)
	Mult = 1000/300.*50 / 5
	a = Play_Arena_Potential_Field(Origin,Mult,markers)
	a['Image']['img'] = z2o(a['Image']['img'])
	cars = {}
	for car_name in ['Mr_Black','Mr_Silver','Mr_Yellow','Mr_Orange','Mr_Blue']:
		cars[car_name] =  Car(N,car_name,Origin,Mult,markers)

	run_name = 'direct_rewrite_test_28Apr17_17h23m15s_Mr_Black'
	T0 = cars['Mr_Black']['runs'][run_name]['trajectory']['ts'][0]
	Tn = cars['Mr_Black']['runs'][run_name]['trajectory']['ts'][-1]
	loct = cars['Mr_Black']['runs'][run_name]['list_of_other_car_trajectories']
	cars['Mr_Black']['load_image_and_meta_data'](run_name)
	timer = Timer(0)
	for car_name in cars:
		cars[car_name]['rewind']()
	figure(1,figsize=(12,12));clf();ds = 5;xylim(-ds,ds,-ds,ds)





	for car_name in cars:
		cars[car_name]['rewind']()
	for t in arange(T0+200,Tn,1/5.):
		#print(t)
		#if timer.time() > 1500:
		#	break
		p = cars['Mr_Black']['report_camera_positions'](run_name,t)
		other_cars_add_list = []

		if p != False:
			pass
			#pix = a['Image']['floats_to_pixels'](p[0])
			#a['Image']['img'][pix[0]-1:pix[0]+1,pix[1]-1:pix[1]+1] = 0

			#pt_plot(p[0],'r')
			#pt_plot(p[1],'r')
			#other_cars_add_list.append(p[0]) # TEMP
		
		for l in loct:
			other_car_name = l[0]
			other_car_run_name = l[1]
			p = cars[other_car_name]['report_camera_positions'](other_car_run_name,t)
			if p != False:
				#pix = a['Image']['floats_to_pixels'](p[0])
				#a['Image']['img'][pix[0]-1:pix[0]+1,pix[1]-1:pix[1]+1] = 5
				other_cars_add_list.append(p[0])
				#a['other_cars']([p[0]])
				pass
		a['other_cars'](other_cars_add_list)
		#mi(a['Image']['img']);
		img = a['Image']['img']
		width = shape(img)[0]
		origin = Origin
		mi(img[width/2-origin/2:width/2+origin/2,width/2-origin/2:width/2+origin/2],1)
		#other_cars_add_list = array(other_cars_add_list)
		#xy = other_cars_add_list*0
		#xy[:,0] = other_cars_add_list[:,1]
		#xy[:,1] = other_cars_add_list[:,0]
		#pts_plot(a['Image']['floats_to_pixels'](xy))

		pause(0.000001)
		if len(cars['Mr_Black']['pts']) > 3:
			sample_points,potential_values = get_sample_points(array(cars['Mr_Black']['pts']),angles,a['Image']['img'],3)
			steer = interpret_potential_values(potential_values)
			img = cars['Mr_Black']['get_left_image'](run_name).copy()
			print steer
			#mi(img,6,img_title=potential_values)
			#animate.prepare_and_show_or_return_frame(img,steer,0,6,66,1.0,cv2.COLOR_RGB2BGR)
			#apply_rect_to_img(img,steer,0,99,bar_color,bar_color,0.9,0.1,center=True,reverse=True,horizontal=True)
			animate.prepare_and_show_or_return_frame(img=img,steer=steer,motor=None,state=6,delay=66,scale=1,color_mode=cv2.COLOR_RGB2BGR)
			pause(0.06)
	#print timer.time()





















	if False:
		from arena.markers_clockwise import markers_clockwise
		markers = Markers(markers_clockwise,4*107/100.)
		Origin = int(2*1000/300.*300)# / 5)
		Mult = 1000/300.*50# / 5
		a = Arena_Potential_Field(Origin,Mult,markers)
		a['other_cars']([[-3.2,0],[0,3.2]])
		mi(a['Image']['img'])
		figure(2);clf();plot(a['Image']['img'][Origin,:],'o-')
		pause(0.1)
		#a['test']()




	if False:
		from arena.markers_clockwise import markers_clockwise
		markers = Markers(markers_clockwise,4*107/100.)
		Origin = int(2*1000/300.*300)# / 5)
		Mult = 1000/300.*50# / 5
		c = Car(N,'Mr_Black',Origin,Mult,markers)
		run_name = 'direct_rewrite_test_28Apr17_17h23m15s_Mr_Black'
		T0 = c['runs'][run_name]['trajectory']['ts'][0]
		Tn = c['runs'][run_name]['trajectory']['ts'][-1]
		loct = c['runs'][run_name]['list_of_other_car_trajectories']
		timer = Timer(0)
		c['near_i'] = 0
		clf()
		for t in arange(T0,Tn,1/30.):
			p = c['report_camera_positions'](run_name,t)
			if p != False:
				pt_plot(p[0],'r')
				pt_plot(p[1],'r')
			#c['runs'][run_name]['list_of_other_car_trajectories']
		print timer.time()
		pause(0.0001)
		xylim(-4,4,-4,4)



	if False:
		from arena.markers_clockwise import markers_clockwise
		markers = Markers(markers_clockwise,4*107/100.)
		Origin = int(2*1000/300.*300)# / 5)
		Mult = 1000/300.*50# / 5
		
		cars = {}
		for car_name in ['Mr_Black','Mr_Silver','Mr_Yellow','Mr_Orange','Mr_Blue']:
			cars[car_name] =  Car(N,car_name,Origin,Mult,markers)

		run_name = 'direct_rewrite_test_28Apr17_17h23m15s_Mr_Black'
		T0 = cars['Mr_Black']['runs'][run_name]['trajectory']['ts'][0]
		Tn = cars['Mr_Black']['runs'][run_name]['trajectory']['ts'][-1]
		loct = cars['Mr_Black']['runs'][run_name]['list_of_other_car_trajectories']
		timer = Timer(0)
		for car_name in cars:
			cars[car_name]['rewind']()
		figure(1,figsize=(12,12))
		clf()
		for t in arange(T0,Tn,1/30.):
			if timer.time() > 15:
				break
			p = cars['Mr_Black']['report_camera_positions'](run_name,t)
			if p != False:
				pt_plot(p[0],'r')
				pt_plot(p[1],'r')
			for l in loct:
				other_car_name = l[0]
				other_car_run_name = l[1]
				p = cars[other_car_name]['report_camera_positions'](other_car_run_name,t)
				if p != False:
					pt_plot(p[0],'b')
					pt_plot(p[1],'b')			
		print timer.time()
		pause(0.0001)
		ds = 5
		xylim(-ds,ds,-ds,ds)



