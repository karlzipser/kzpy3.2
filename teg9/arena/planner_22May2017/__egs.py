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



