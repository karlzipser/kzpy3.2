from kzpy3.utils2 import *
pythonpaths(['kzpy3','kzpy3/teg9'])
from vis2 import *
from arena.planner.Constants import C
from data.utils.general import car_name_from_run_name


bair_car_data_location = C['bair_car_data_location']

if 'N' not in locals():
	print("Loading trajectory data . . .")
	N = lo(C['trajectory_data_location'])

 
run_name = 'direct_rewrite_test_28Apr17_18h09m52s_Mr_Black'

car_name = car_name_from_run_name(run_name)

bag_folders_dst_rgb1to4_path = opj(bair_car_data_location,'rgb_1to4')
bag_folders_dst_meta_path = opj(bair_car_data_location,'meta')

L = lo(opj(bair_car_data_location,'meta',run_name,'left_image_bound_to_data.pkl'))
ts,data_list = get_sorted_keys_and_data(L)
ts = array(ts)
data_types = data_list[0].keys()
data = {}
for d in data_types:
	data[d] = []
for e in data_list:
	for d in data_types:
		data[d].append(e[d])
for d in data_types:
	data[d] = array(data[d])


figure(5);clf()

ref=XX('traj = N/`car_name/`run_name/self_trajectory'		) ;exec(ref)

ref=XX('left = traj/left'								) ;exec(ref)
ref=XX('right = traj/right'								) ;exec(ref)
left['x'] = left['x'][30:-30]
left['y'] = left['y'][30:-30]
left['t_vel'] = left['t_vel'][30:-30]
right['x'] = right['x'][30:-30]
right['y'] = right['y'][30:-30]
right['t_vel'] = right['t_vel'][30:-30]


#plot(ts,meo((array(run_meta['motor'])-49)/6.0,10),'k')
#plot(ts,meo(run_meta['encoder'],30),'r-')
#plot(ts,array(run_meta['state'])/10.0,'c')
plot(ts-ts[0],(array(data['motor'])-49)/6.0,'k')
plot(ts-ts[0],(array(data['steer'])-49)/20.0,'b')
plot(ts-ts[0],data['encoder'],'r')
#plot(ts-ts[0],array(data['state'])/10.0,'y')
#plot(ts-ts[0],array(data['gyro'])/100.0,'b')
plot(ts-ts[0],array(data['gyro_heading'])/1000.0,'b')
##plot(ts-ts[0],array(data['acc'])/10.0,'r')

plot(ts-ts[0],left['t_vel'],'g')
#plot(N_ts-ts[0],left['x'],'c');plot(N_ts-ts[0],left['y'],'c')
#plot(N_ts-ts[0],right['x'],'c');plot(N_ts-ts[0],right['y'],'c')
#xlim(0,4000)
#ylim(-5,5)
#xylim(-5,5,-5,5)
pause(0.001)





def check_trajectory_point(traj,side,i,t):
	#assert(traj['ts'][i] <= t)
	#if traj['ts'][i] == t:
	if traj[side]['t_vel'][i] > 3: # 1.788: # Above 4 mph
		return False
	if traj[side]['t_vel'][i]<0.1: #TEMP
		return False
	elif traj['camera_separation'][i] > 0.5: # almost larger than length of car
		return False
	elif traj[side]['timestamp_gap'][i] > 0.5: # missed data points
		return False
	elif length([traj[side]['x'][i],traj[side]['y'][i]]) > C['Marker_Radius']:
		return False
	return True
	#assert(False)
traj_valid = []
for i in range(len(ts)):
	t = ts[i]
	valid = True
	for side in ['left','right']:
		if not check_trajectory_point(traj,side,i,t):
			valid = False
			break
	if valid:
		v = 1
	else:
		v = 0
	traj_valid.append(v)
plot(ts,traj_valid,'.')



def rlen(a):
	return range(len(a))


new_traj_x = (left['x'] + right['x'])/2.0
new_traj_y = (left['y'] + right['y'])/2.0
new_traj_x *= traj_valid
new_traj_y *= traj_valid


invalid_states = []
invalid_state = [0,0]
waiting_for_first_valid = 1
waiting_for_valid = 2
waiting_for_invalid = 3

vstate = waiting_for_first_valid
for i in rlen(traj_valid):
	print (i,vstate)
	if traj_valid[i] == 1:
		if vstate == waiting_for_first_valid:
			vstate = waiting_for_invalid
		elif vstate == waiting_for_invalid:
			pass
		elif vstate == waiting_for_valid:
			invalid_state[1] = i-1
			invalid_states.append(invalid_state)
			invalid_state = [0,0]
			vstate = waiting_for_invalid
		else:
			assert(False)
	elif traj_valid[i] == 0:
		if vstate == waiting_for_first_valid:
			pass
		elif vstate == waiting_for_invalid:
			invalid_state[0] = i
			print invalid_state
			vstate = waiting_for_valid
		elif vstate == waiting_for_valid:
			pass
		else:
			assert(False)




for invalid_state in invalid_states:
	start = new_traj_x[invalid_state[0]-1]
	end = new_traj_x[invalid_state[1]+1]
	l = invalid_state[1]-invalid_state[0]+1
	for j in range(l):
		new_traj_x[invalid_state[0]+j] = start + j/(1.0*l)*(end-start)


aN_ts = N_ts[30:-30]
assert(aN_ts[0]==ts[0])
assert(len(aN_ts)==len(ts))
meoencoder = array(meo(data['encoder'],120))

still = False
for i in rlen(ts):
	if meoencoder[i] > 0.01:
		still = False
	else:
		if still == False:
			still = True
			x = new_traj_x[i-1]
			y = new_traj_y[i-1]
		new_traj_x[i] = x
		new_traj_y[i] = y





############## drive from heading test
#
def vec(heading,encoder):
	velocity = encoder/2.3 # rough guess
	a = [0,1]
	a = array(rotatePoint([0,0],a,heading))
	a *= velocity/30.0
	return array(a)
figure(99);clf()
plt_square();
xylim(-15,15,-15,15)
xy = array([0.0,0.0])
xys=[]
for i in range(len(ts)):
	#plot(xy[0],xy[1],'r.')
	heading = data['gyro_heading'][i][0]
	encoder = data['encoder'][i]
	v = vec(heading,encoder)
	xy += v
	xys.append(array(xy))
	print i#(heading,encoder,v)
	#pause(0.0001)
pts_plot(array(xys))
#
##############