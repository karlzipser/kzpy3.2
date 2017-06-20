from kzpy3.utils import *
pythonpaths(['kzpy3','kzpy3/teg9'])
from vis import *
import data.utils.animate as animate
import arena.planner.Markers as Markers
import arena.planner.Potential_Fields as Potential_Fields
import arena.planner.Cars as Cars

bair_car_data_location = '/Volumes/SSD_2TB/bair_car_data_new_28April2017'

GRAPHICS = True
	


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
    	if GRAPHICS:
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
	if GRAPHICS:
		figure(9);plot(potential_values,'bo-')

	d = 99.0/(1.0*len(potential_values)-1)
	steer_angles = np.floor(99-arange(0,100,d))

	p = min(pmax/0.8,1.0)

	steer = int((p*steer_angles[min_potential_index]+(1-p)*49.0))
	return steer


def meters_to_pixels(x,y):
    return (int(-Mult*x)+Origin),(int(Mult*y)+Origin)



angles = -arange(-45,46,9)
view_angle = 35


def find_index_of_closest(val,lst):
	d = []
	for i in range(len(lst)):
		d.append(abs(lst[i]-val))
	return d.index(min(d))
		



# https://stackoverflow.com/questions/31735499/calculate-angle-clockwise-between-two-points
from math import acos
from math import sqrt
from math import pi
def length(v):
    return sqrt(v[0]**2+v[1]**2)
def dot_product(v,w):
   return v[0]*w[0]+v[1]*w[1]
def determinant(v,w):
   return v[0]*w[1]-v[1]*w[0]
def inner_angle(v,w):
   cosx=dot_product(v,w)/(length(v)*length(w))
   rad=acos(cosx) # in radians
   return rad*180/pi # returns degrees
def angle_clockwise(A, B):
    inner=inner_angle(A,B)
    det = determinant(A,B)
    if det<0: #this is a property of the det. If the det < 0 then B is clockwise of A
        return inner
    else: # if the det > 0 then A is immediately clockwise of B
        return 360-inner






if __name__ == "__main__":


	DISPLAY_LEFT = True
	
	if 'N' not in locals():
		print("Loading trajectory data . . .")
		N = lo(opjD('N_pruned.pkl'))
	markers = Markers.Markers(Markers.markers_clockwise,4*107/100.)
	Origin = int(2*1000/300.*300 / 5)
	Mult = 1000/300.*50 / 5
	

	the_arena = Potential_Fields.Play_Arena_Potential_Field(Origin,Mult,markers)
	mode = the_arena['type']
	
	the_arena['Image']['img'] = z2o(the_arena['Image']['img'])
	if mode == 'Follow_Arena_Potential_Field':
		the_arena['Image']['img'] *= 0.5
		the_arena['Image']['img'] += 0.5
	
	if 'INITALIZED' not in locals():
		INITALIZED = True
		cars = {}
		for car_name in ['Mr_Black','Mr_Silver','Mr_Yellow','Mr_Orange','Mr_Blue']:
			cars[car_name] =  Cars.Car(N,car_name,Origin,Mult,markers)
		run_name = 'direct_rewrite_test_28Apr17_17h23m15s_Mr_Black'
		our_car = Cars.car_name_from_run_name(run_name)
		T0 = cars[our_car]['runs'][run_name]['trajectory']['ts'][0]
		Tn = cars[our_car]['runs'][run_name]['trajectory']['ts'][-1]
		loct = cars[our_car]['runs'][run_name]['list_of_other_car_trajectories']
		cars[our_car]['load_image_and_meta_data'](run_name,bair_car_data_location)
	
	for car_name in cars:
		cars[car_name]['rewind']()
	if GRAPHICS:			
		figure(1,figsize=(12,12));clf();ds = 5;xylim(-ds,ds,-ds,ds)


	output_data = {}
	output_data[run_name] = {}
	output_data[run_name][mode] = {}
	output_data[run_name][mode]['sample_points'] = []
	output_data[run_name][mode]['potential_values'] = []
	output_data[run_name][mode]['steer'] = []
	output_data[run_name][mode]['real_steer'] = []
	output_data[run_name][mode]['near_t'] = []
	output_data[run_name][mode]['near_i'] = []




	for car_name in cars:
		cars[car_name]['rewind']()
	timer = Timer(10)
	stats=[]
	ctr_q = 0
	t_prev = 0
	for t in arange(T0+210,Tn,1/30.):
		#print(t-t_prev)
		t_prev = t
		if timer.check():
			print(time_str('Pretty'))
			timer.reset()
		#	break
		p = cars[our_car]['report_camera_positions'](run_name,t)
		other_cars_add_list = []
		other_cars_point_list = []
		other_cars_angle_distance_list = []
		if len(p) > 0:
			pix = the_arena['Image']['floats_to_pixels'](p)#[0])
			p = array(p)
			xy_our = 1* p
			our_heading = cars[our_car]['state_info']['heading']
			p_mod = p#0*p
			no_cars_in_view = True
			for l in loct:
				other_car_name = l[0]
				other_car_run_name = l[1]
				p = cars[other_car_name]['report_camera_positions'](other_car_run_name,t)
				if len(p) > 0:
					other_cars_point_list.append(p)#[0])
					if our_heading != None:
						#angle_to_other_car = angle_clockwise(our_heading, array(p[0])-xy_our[0])
						#print(d2s('p:',p,'xy_our:',xy_our))
						angle_to_other_car = angle_clockwise(our_heading, array(p)-xy_our)
						if angle_to_other_car > 360-view_angle:
							angle_to_other_car = angle_to_other_car-360
						#distance_to_other_car = length(p[0]-xy_our[0])
						distance_to_other_car = length(p-xy_our)
						
						
						if angle_to_other_car > -view_angle and angle_to_other_car < view_angle: 
							#print((other_car_name,int(angle_to_other_car),dp(distance_to_other_car,2)))
							#other_cars_add_list.append(p[0])
							other_cars_angle_distance_list.append([angle_to_other_car,distance_to_other_car])
							other_cars_add_list.append(p)
							no_cars_in_view = False
			if no_cars_in_view:
				continue
			the_arena['other_cars'](other_cars_add_list,mode,xy_our)
			img = the_arena['Image']['img']
			width = shape(img)[0]
			origin = Origin
			if GRAPHICS:
				mi(img,1)
				the_arena['Image']['plot_pts'](other_cars_point_list,'b')
				the_arena['Image']['plot_pts'](xy_our,'r')
			if len(other_cars_add_list) > 0:
				other_cars_add_list = array(other_cars_add_list)
				#xy = other_cars_add_list*0
				#xy[:,0] = other_cars_add_list[:,1]
				#xy[:,1] = other_cars_add_list[:,0]
			pause(0.000001)
			if cars[our_car]['state_info']['heading'] != None:
				sample_points,potential_values = get_sample_points(array(cars[our_car]['state_info']['pts']),angles,the_arena,cars[our_car]['state_info']['heading'])
				if mode == 'Follow_Arena_Potential_Field':
					for ang,dist in other_cars_angle_distance_list:
						indx = find_index_of_closest(-ang,angles)
						if dist > 1.5:
							potential_values[indx] *= (dist-1.5)/8.0
				steer = interpret_potential_values(potential_values)
				real_steer = cars[our_car]['runs'][run_name]['trajectory']['data']['steer'][cars[our_car]['state_info']['near_i']]

				output_data[run_name][mode]['sample_points'].append(sample_points)
				output_data[run_name][mode]['potential_values'].append(potential_values)
				output_data[run_name][mode]['steer'].append(steer)
				output_data[run_name][mode]['real_steer'].append(real_steer)
				output_data[run_name][mode]['near_t'].append(cars[our_car]['state_info']['near_t'])
				output_data[run_name][mode]['near_i'].append(cars[our_car]['state_info']['near_i'])


				if GRAPHICS:
					figure(9)
					if ctr_q > 1:
						clf()
						ctr_q = 0
					plot(potential_values,'r.-');xylim(0,9,0,2);
					ctr_q += 1
					img = cars[our_car]['get_left_image'](run_name).copy()
					img = cars[our_car]['get_left_image'](run_name).copy()
					k = animate.prepare_and_show_or_return_frame(img=img,steer=steer,motor=None,state=1,delay=1,scale=2,color_mode=cv2.COLOR_RGB2BGR,window_title='plan')
					img = cars[our_car]['get_left_image'](run_name).copy()
					k = animate.prepare_and_show_or_return_frame(img=img,steer=real_steer,motor=None,state=6,delay=1,scale=2,color_mode=cv2.COLOR_RGB2BGR,window_title='real')
					if k == ord('q'):
						break

		else:
			cars[our_car]['state_info']['pts'] = []
		

	so(output_data,opjD(run_name+'.output_data'))



def replay_potential_values(pv):
	ctr = 0
	for p in pv:
		if ctr >= 30:
			clf()
			ctr = 0
		plot(p,'r.-');xylim(0,9,0,2);pause(0.01)
		ctr += 1




