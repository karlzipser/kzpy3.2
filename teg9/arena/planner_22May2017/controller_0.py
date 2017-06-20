from kzpy3.utils import *
pythonpaths(['kzpy3','kzpy3/teg9'])
from vis import *
import data.utils.animate as animate
import arena.planner.Markers as Markers
import arena.planner.Potential_Fields as Potential_Fields
import arena.planner.Cars as Cars

bair_car_data_location = '/Volumes/SSD_2TB/bair_car_data_new_28April2017'


	


def get_sample_points(pts,angles,pfield,heading):

    sample_points = []
    potential_values = []


    heading *= 0.5 # 50 cm, about the length of the car
    h_color = 'yellow'
    #if pts[-n,0] > pts[-1,0]:
    #    heading *= -1
    #    h_color = 'red'
        #print "heading negated"
    #cprint(d2s(dp(heading[0],2),dp(heading[0],2)),h_color)
    #if pts[-3,1] > pts[-1,1]:
    #    heading *= -1

    for the_arena in angles:

        sample_points.append( rotatePoint([0,0],heading,the_arena) )
    #figure(3)
    #pts_plot(pts)
    for k in range(len(sample_points)):
        f = sample_points[k]
        #plot([pts[-1,0],pts[-1,0]+f[0]],[pts[-1,1],pts[-1,1]+f[1]])
    #figure(1)
    for sp in sample_points:
    	pfield['Image']['plot_pts'](array(sp)+array(pts[-1,:]),'g')
        pix = pfield['Image']['floats_to_pixels']([sp[0]+pts[-1,0],sp[1]+pts[-1,1]])
        #plot(pix[0],pix[1],'kx')
        potential_values.append(pfield['Image']['img'][pix[0],pix[1]])

    return sample_points,potential_values




def __get_sample_points(pts,angles,pfield,n=3):

    sample_points = []
    potential_values = []

    heading = normalized_vector_from_pts(pts[-n:,:])
    heading *= 0.5 # 50 cm, about the length of the car
    h_color = 'yellow'
    if pts[-n,0] > pts[-1,0]:
        heading *= -1
        h_color = 'red'
        #print "heading negated"
    cprint(d2s(dp(heading[0],2),dp(heading[0],2)),h_color)
    #if pts[-3,1] > pts[-1,1]:
    #    heading *= -1

    for the_arena in angles:

        sample_points.append( rotatePoint([0,0],heading,the_arena) )
    #figure(3)
    #pts_plot(pts)
    for k in range(len(sample_points)):
        f = sample_points[k]
        #plot([pts[-1,0],pts[-1,0]+f[0]],[pts[-1,1],pts[-1,1]+f[1]])
    #figure(1)
    for sp in sample_points:
    	pfield['Image']['plot_pts'](array(sp)+array(pts[-1,:]),'g')
        pix = pfield['Image']['floats_to_pixels']([sp[0]+pts[-1,0],sp[1]+pts[-1,1]])
        #plot(pix[0],pix[1],'kx')
        potential_values.append(pfield['Image']['img'][pix[0],pix[1]])

    return sample_points,potential_values


def _interpret_potential_values(potential_values):
    min_potential_index = potential_values.index(min(potential_values))
    max_potential_index = potential_values.index(max(potential_values))
    middle_index = int(len(potential_values)/2)

    d = 99.0/(1.0*len(potential_values)-1)
    steer_angles = np.floor(99-arange(0,100,d))
    dp = potential_values[max_potential_index] - potential_values[min_potential_index]
    
    p = min(1,dp/max( (0.6-max(0,potential_values[max_potential_index]-0.8)) ,0.2) )
    steer = int((p*steer_angles[min_potential_index]+(1-p)*49.0))
    return steer


def interpret_potential_values(potential_values):
	min_potential_index = potential_values.index(min(potential_values))
	max_potential_index = potential_values.index(max(potential_values))
	middle_index = int(len(potential_values)/2)
	potential_values = array(potential_values)
	pmin = potential_values.min()
	pmax = potential_values.max()
	potential_values = z2o(potential_values) * pmax

	figure(9);plot(potential_values,'bo-')

	d = 99.0/(1.0*len(potential_values)-1)
	steer_angles = np.floor(99-arange(0,100,d))

	p = min(pmax/0.8,1.0)

	steer = int((p*steer_angles[min_potential_index]+(1-p)*49.0))
	return steer


def meters_to_pixels(x,y):
    return (int(-Mult*x)+Origin),(int(Mult*y)+Origin)



angles = -arange(-45,46,9)


if __name__ == "__main__":

	if 'INITALIZED' not in locals():
		INITALIZED = True
		DISPLAY_LEFT = True
		

		if 'N' not in locals():
			print("Loading trajectory data . . .")
			N = lo(opjD('N_pruned.pkl'))
		markers = Markers.Markers(Markers.markers_clockwise,4*107/100.)
		Origin = int(2*1000/300.*300 / 5)
		Mult = 1000/300.*50 / 5
		the_arena = Potential_Fields.Play_Arena_Potential_Field(Origin,Mult,markers)
		the_arena['Image']['img'] = z2o(the_arena['Image']['img'])

		cars = {}
		for car_name in ['Mr_Black','Mr_Silver','Mr_Yellow','Mr_Orange','Mr_Blue']:
			cars[car_name] =  Cars.Car(N,car_name,Origin,Mult,markers)

		run_name = 'direct_rewrite_test_28Apr17_17h23m15s_Mr_Black'
		our_car = Cars.car_name_from_run_name(run_name)
		T0 = cars[our_car]['runs'][run_name]['trajectory']['ts'][0]
		Tn = cars[our_car]['runs'][run_name]['trajectory']['ts'][-1]
		loct = cars[our_car]['runs'][run_name]['list_of_other_car_trajectories']
		cars[our_car]['load_image_and_meta_data'](run_name,bair_car_data_location)
		timer = Timer(0)
		for car_name in cars:
			cars[car_name]['rewind']()
		figure(1,figsize=(12,12));clf();ds = 5;xylim(-ds,ds,-ds,ds)




	for car_name in cars:
		cars[car_name]['rewind']()

	stats=[]
	ctr_q = 0
	t_prev = 0
	for t in arange(T0+210,Tn,1/30.):
		#print(t-t_prev)
		t_prev = t
		#if timer.time() > 1500:
		#	break
		p = cars[our_car]['report_camera_positions'](run_name,t)
		other_cars_add_list = []
		other_cars_point_list = []
		if p != False:
			pass
			pix = the_arena['Image']['floats_to_pixels'](p[0])
			#print pix
			#the_arena['Image']['img'][pix[0]-1:pix[0]+1,pix[1]-1:pix[1]+1] = 0
			p = array(p)
			xy_our = 1* p
			our_heading = cars[our_car]['state_info']['heading']
			#xy_our[:,0]=p[:,1]
			#xy_our[:,1]=p[:,0]
			p_mod = p#0*p
			#p_mod[:,0]=-p[:,1]
			#p_mod[:,1]=-p[:,0]			
			
			#other_cars_add_list.append(p_mod[0])#p[0]) # TEMP
			no_cars_in_view = True
			for l in loct:
				other_car_name = l[0]
				other_car_run_name = l[1]
				p = cars[other_car_name]['report_camera_positions'](other_car_run_name,t)
				if p != False:
					other_cars_point_list.append(p[0])
					#pix = the_arena['Image']['floats_to_pixels'](p[0])
					#the_arena['Image']['img'][pix[0]-1:pix[0]+1,pix[1]-1:pix[1]+1] = 5
					if our_heading != None:
						angle_to_other_car = np.degrees(angle_between(our_heading, array(p[0])-xy_our[0]))
						if abs(angle_to_other_car) < 40:
							other_cars_add_list.append(p[0])
							no_cars_in_view = False
					
					#the_arena['other_cars']([p[0]])
					pass
			if False:#no_cars_in_view:
				continue
			the_arena['other_cars'](other_cars_add_list)
			#mi(the_arena['Image']['img']);
			img = the_arena['Image']['img']
			width = shape(img)[0]
			origin = Origin
			#mi(img[width/2-origin/2:width/2+origin/2,width/2-origin/2:width/2+origin/2],1)
			mi(img,1)
			the_arena['Image']['plot_pts'](other_cars_point_list,'b')
			the_arena['Image']['plot_pts'](xy_our,'r')
			if len(other_cars_add_list) > 0:
				other_cars_add_list = array(other_cars_add_list)
				xy = other_cars_add_list*0
				xy[:,0] = other_cars_add_list[:,1]
				xy[:,1] = other_cars_add_list[:,0]
			#pts_plot(the_arena['Image']['floats_to_pixels'](xy),'b')
			#pt_plot(the_arena['Image']['floats_to_pixels'](p[0]),'r')
			pause(0.000001)
			if cars[our_car]['state_info']['heading'] != None:
				sample_points,potential_values = get_sample_points(array(cars[our_car]['state_info']['pts']),angles,the_arena,cars[our_car]['state_info']['heading'])
				figure(9)
				if ctr_q > 10:
					clf()
					ctr_q = 0
				plot(potential_values,'r.-');xylim(0,9,0,2);
				ctr_q += 1

				steer = interpret_potential_values(potential_values)
				img = cars[our_car]['get_left_image'](run_name).copy()
				#print steer
				#mi(img,6,img_title=potential_values)
				#animate.prepare_and_show_or_return_frame(img,steer,0,6,66,1.0,cv2.COLOR_RGB2BGR)
				#apply_rect_to_img(img,steer,0,99,bar_color,bar_color,0.9,0.1,center=True,reverse=True,horizontal=True)
				img = cars[our_car]['get_left_image'](run_name).copy()
				k = animate.prepare_and_show_or_return_frame(img=img,steer=steer,motor=None,state=1,delay=1,scale=2,color_mode=cv2.COLOR_RGB2BGR,window_title='plan')
				real_steer = cars[our_car]['runs'][run_name]['trajectory']['data']['steer'][cars[our_car]['state_info']['near_i']]
				img = cars[our_car]['get_left_image'](run_name).copy()
				k = animate.prepare_and_show_or_return_frame(img=img,steer=real_steer,motor=None,state=6,delay=1,scale=2,color_mode=cv2.COLOR_RGB2BGR,window_title='real')
				stats.append([steer,real_steer])
				if k == ord('q'):
					break
				#pause(0.06)
				#raw_input('hit enter')
		else:
			cars[our_car]['state_info']['pts'] = []
		








