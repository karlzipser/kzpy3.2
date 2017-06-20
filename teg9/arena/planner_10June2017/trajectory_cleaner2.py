from kzpy3.utils2 import *
pythonpaths(['kzpy3','kzpy3/teg9'])
from vis2 import *
from arena.planner.Constants import C
from data.utils.general import car_name_from_run_name

bair_car_data_location = C['bair_car_data_location']

if 'N' not in locals():
	print("Loading trajectory data . . .")
	N = lo(C['trajectory_data_location'])
 
run_name = 'direct_rewrite_test_28Apr17_18h09m52s_Mr_Black'#'direct_rewrite_test_25Apr17_13h21m03s_Mr_Black' #





def get_metadata(run_name,bair_car_data_location):
	print('get_metadata')
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
		for i in rlen(data[d]):
			if not is_number(data[d][i]):
				data[d][i] = 0
		data[d] = array(data[d])
	return ts,data

def time_correct_traj(run_name,ts,N):
	"""
	There is a time offset between the trajectory data and the older metadata timestamps.
	"""
	print('time_correct_traj')
	car_name = car_name_from_run_name(run_name)
	assert('TIME_CORRECTION_DONE' not in N[car_name][run_name])
	traj = N[car_name][run_name]['self_trajectory']
	traj['ts'] = traj['ts'][30:-30]
	for i in range(len(traj['ts'])):
		assert(traj['ts'][i]) == ts[i]
	traj['camera_separation'] = traj['camera_separation'][30:-30]
	for side in ['left','right']:
		for e in ['x','y','t_vel','timestamp_gap']:
			traj[side][e] = traj[side][e][30:-30]
	N[car_name][run_name]['TIME_CORRECTION_DONE'] = True
	return traj

def check_trajectory_point(traj,side,i,t):
	#print('check_trajectory_point')
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

def get_traj_valid(traj,ts):
	print('get_traj_valid')
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
	return array(traj_valid)


def get_invalid_states(traj_valid):
	print('get_invalid_states')
	invalid_states = []
	invalid_state = [0,0]
	waiting_for_first_valid = 1
	waiting_for_valid = 2
	waiting_for_invalid = 3
	vstate = waiting_for_first_valid
	for i in rlen(traj_valid):
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
				vstate = waiting_for_valid
			elif vstate == waiting_for_valid:
				pass
			else:
				assert(False)
	return invalid_states

def interpolate_over_invalid(traj,invalid_states):
	print('interpolate_over_invalid')
	for c in ['x','y','t_vel']:
		for invalid_state in invalid_states:
			start = traj[c][invalid_state[0]-1]
			end = traj[c][invalid_state[1]+1]
			l = invalid_state[1]-invalid_state[0]+1
			for j in range(l):
				traj[c][invalid_state[0]+j] = start + j/(1.0*l)*(end-start)

def interpolate_over_still(traj,data,ts):
	print('interpolate_over_still')
	meoencoder = array(meo(data['encoder'],120))
	for d in ['forward','backward']:
		for c in ['x','y','t_vel']:
			traj[d+'_'+c] = traj[c].copy()
	still = False
	for i in range(0,len(ts)):
		if meoencoder[i] > 0.01:
			still = False
		else:
			if still == False:
				still = True
				x = traj['forward_x'][i-1]
				y = traj['forward_y'][i-1]
				v = traj['forward_t_vel'][i-1]
			traj['forward_x'][i] = x
			traj['forward_y'][i] = y
			traj['forward_t_vel'][i] = v
	still = False
	for i in range(len(ts)-2,0,-1):
		if meoencoder[i] > 0.01:
			still = False
		else:
			if still == False:
				still = True
				x = traj['backward_x'][i+1]
				y = traj['backward_y'][i+1]
				v = traj['backward_t_vel'][i+1]
			traj['backward_x'][i] = x
			traj['backward_y'][i] = y
			traj['backward_t_vel'][i] = v
	traj['new_x'] = array(meo((traj['backward_x']+traj['forward_x'])/2.0,60))
	traj['new_y'] = array(meo((traj['backward_y']+traj['forward_y'])/2.0,60))
	traj['new_t_vel'] = array(meo((traj['backward_t_vel']+traj['forward_t_vel'])/2.0,60))




def get_headings(traj):
	print('get_headings')
	traj['heading'] = []
	traj['absolute_heading'] = []
	traj['relative_heading'] = []
	n = C['n_for_heading']
	pts = array(zip(traj['new_x'],traj['new_y']))
	for i in range(len(traj['new_x'])):
		if i <= n:
			traj['heading'].append(array([0,1]))
		else:
			traj['heading'].append(normalized_vector_from_pts(pts[i-n+1:i]))
			if pts[i-n][0] > pts[i][0]:
				traj['heading'][i] *= -1.0
			#if i > n+1 and np.degrees(angle_between(traj['heading'][i],traj['heading'][i-1])) > 45:
			#		traj['heading'][i] = traj['heading'][i-1]
	traj['heading'] = array(traj['heading'])
	traj['heading_meo'] = 0.0*traj['heading']
	traj['heading_meo'][:,0] = array(meo(traj['heading'][:,0],90))
	traj['heading_meo'][:,1] = array(meo(traj['heading'][:,1],90))
	traj['heading'] = traj['heading_meo']
	for i in range(len(traj['new_x'])):		
		traj['relative_heading'].append(angle_clockwise(traj['heading'][i],pts[i]))
		traj['absolute_heading'].append(angle_clockwise(traj['heading'][i],[0,1]))
	traj['relative_heading'] = array(meo(traj['relative_heading'],90))
	traj['absolute_heading'] = array(traj['absolute_heading'])
	traj['x'] = traj['new_x']
	traj['y'] = traj['new_y']
	traj['t_vel'] = traj['new_t_vel']

def del_traj_extra(traj):
	print('get_headings')
	for d in ['backward_x','new_x','new_y','camera_separation','backward_t_vel','forward_t_vel','new_t_vel',
		'backward_y','right','forward_x','heading_meo','forward_y','left']:
		del traj[d]


def create_and_save_traj(run_name,bair_car_data_location,N):
	print
	ts,data = get_metadata(run_name,bair_car_data_location)

	traj = time_correct_traj(run_name,ts,N)

	traj_valid = get_traj_valid(traj,ts)

	for c in ['x','y','t_vel']:
		traj[c] = (traj['left'][c]+traj['right'][c])/2.0 * traj_valid

	traj['encoder'] = meo(data['encoder'],60)

	figure(1,figsize=(5,2)); clf(); plot(ts-ts[0],traj['encoder']);plt.title(run_name);pause(0.01)

	invalid_states = get_invalid_states(traj_valid)

	interpolate_over_invalid(traj,invalid_states)

	interpolate_over_still(traj,data,ts)

	get_headings(traj)

	del_traj_extra(traj)

	path = opjD('bair_car_data_new_28April2017','meta',run_name)
	path = opjD(bair_car_data_location,'meta',run_name)
	unix('mkdir -p '+path)
	so(traj,opj(path,'traj.pkl'))
	print('saved '+path+'/traj.pkl')
	#return traj




timer = Timer(0)
for car_name in N.keys():
	for run_name in N[car_name].keys():
		print(opj(car_name,run_name))
		print(timer.time())
		if True:#try:
			create_and_save_traj(run_name,bair_car_data_location,N)
		else: #except Exception as e:
			print("********** Exception ***********************")
			print(e.message, e.args)			

GRAPHICS = False
if GRAPHICS:
	traj['ts'] = array(traj['ts'])
	ts = traj['ts']
	figure(5);clf()
	#plot(ts-ts[0],(array(data['motor'])-49)/6.0,'k')
	#plot(ts-ts[0],(array(data['steer'])-49)/20.0,'b')
	#plot(ts-ts[0],data['encoder'],'r')
	#plot(ts-ts[0],array(data['gyro_heading'])/1000.0,'b')
	plot(traj['x'],traj['y'],'.')
	pause(0.001)
	#plot(ts-ts[0],traj_valid,'.')

	#gyro_heading = data['gyro_heading'][:,0]
	#for i in rlen(gyro_heading):
	#	while gyro_heading[i] > 360:
	#		gyro_heading[i] -= 360
	#	while gyro_heading[i] < 0:
	#		gyro_heading[i] += 360
	#plot(ts-[0],gyro_heading,'r')
	plot(ts-[0],traj['absolute_heading'],'g')

############## drive from heading test
#

"""
def vec(heading,encoder):
	velocity = encoder/2.3 # rough guess
	a = [0,1]
	a = array(rotatePoint([0,0],a,heading))
	a *= velocity/30.0
	return array(a)
figure(99);clf()
plt_square();
l = 30
xylim(-l,l,-l,l)
xy = array([0.0,0.0])
xys=[]
if GRAPHICS:
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
"""
#
##############