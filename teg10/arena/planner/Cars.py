from kzpy3.utils2 import *
pythonpaths(['kzpy3','kzpy3/teg9'])
from vis2 import *
import data.utils.general
from data.utils.general import car_name_from_run_name
from arena.planner.Constants import C


def Car(N,car_name,origin,mult,markers,bair_car_data_location):
	D = {}
	D['Purpose'] = d2s(inspect.stack()[0][3],':','Car object.')
	D['car_name'] = car_name
	D['type'] = 'Car'
	D['runs'] = {}
	D['wise_delta'] = 10

	def _relative_heading_and_direction(run_name):
		traj = D['runs'][run_name]['traj']
		traj['direction'] = []
		for i in range(len(traj['heading'])):
			xy = [traj['x'][i],traj['y'][i]]
			traj['relative_heading'][i] = angle_clockwise(traj['heading'][i],xy)
			if np.isnan(traj['relative_heading'][i]):
				if i > 0:
					traj['relative_heading'][i] = traj['relative_heading'][i-1]
				else:
					traj['relative_heading'][i] = 0
			relative_heading = traj['relative_heading'][i]
			wise_delta = D['wise_delta']
			if relative_heading > 360-wise_delta or relative_heading <= wise_delta or length(xy) < 1.0:
				direction = 'in'
			elif relative_heading > wise_delta and relative_heading <= 180-wise_delta:
				direction = 'counter-clockwise'
			elif relative_heading > 180+wise_delta and relative_heading <= 360-wise_delta:
				direction = 'clockwise'
			else:
				direction = 'out'
			traj['direction'].append(direction)

	def _load_run(N,run_name,bair_car_data_location):
		print("load run "+run_name)
		D['runs'][run_name] = {}
		R = D['runs'][run_name]
		ts,dat = data.utils.general.get_metadata(run_name,bair_car_data_location)
		traj = lo(opj(bair_car_data_location,'meta',run_name,'traj.pkl'))
		R['ts'] = array(ts)
		R['data'] = dat
		R['traj'] = traj
		R['list_of_other_car_trajectories'] = []	
		for other_run_name in N[car_name][run_name]['other_trajectories']:
			other_car_name = car_name_from_run_name(other_run_name)
			R['list_of_other_car_trajectories'].append( [other_car_name,other_run_name] )
		_relative_heading_and_direction(run_name)

	for run_name in N[car_name].keys():
		if len(gg(opj(bair_car_data_location,'meta',run_name,'*.pkl'))) < 6:
			continue
		_load_run(N,run_name,bair_car_data_location)
	print("""
		Remeber time to collision.
	""")


	def _rewind():
		D['near_i'] = 0
		D['near_t'] = 0
		D['near_t_prev'] = 0
		D['current_run_name'] = 'no run current'
	D['rewind'] = _rewind
	D['rewind']()


	def _establish_valid_time_and_index(run_name,t):
		traj = D['runs'][run_name]['traj']
		if t >= D['near_t']:
			A = D['near_i']
			B = len(traj['ts'])
			C = 1
		else:
			A = D['near_i']
			B = 0
			C = -1
		if t>traj['ts'][0] and t<traj['ts'][-1]:
			near_t = -1
			for i in range(A,B,C):
				if traj['ts'][i-1]<t and traj['ts'][i]>=t:
					near_t = traj['ts'][i]
					near_i = i
					break
			if near_t > 0:
				D['near_i'] = near_i
				D['near_t'] = near_t
				D['current_run_name'] = run_name
				return True
		return False
	D['establish_valid_time_and_index'] = _establish_valid_time_and_index


	def _current_xy():
		near_i = D['near_i']
		current_run_name = D['current_run_name']
		xy = []
		for c in ['x','y']:
			xy.append(D['runs'][current_run_name]['traj'][c][near_i])
		return array(xy)
	D['current_xy'] = _current_xy

	def _current_t():
		return near_t
	D['current_t'] = _current_t

	def _current_heading():
		near_i = D['near_i']
		current_run_name = D['current_run_name']
		return array(D['runs'][current_run_name]['traj']['heading'][near_i])
	D['current_heading'] = _current_heading

	def _current_velocity():
		near_i = D['near_i']
		current_run_name = D['current_run_name']
		return D['runs'][current_run_name]['traj']['t_vel'][near_i]
	D['current_velocity'] = _current_velocity

	def _current_relative_heading():
		near_i = D['near_i']
		current_run_name = D['current_run_name']
		return D['runs'][current_run_name]['traj']['relative_heading'][near_i]
	D['current_relative_heading'] = _current_relative_heading

	def _current_direction():
		near_i = D['near_i']
		current_run_name = D['current_run_name']
		return D['runs'][current_run_name]['traj']['direction'][near_i]
	D['current_direction'] = _current_direction


	print("created "+D['type']+": "+D['car_name'])
	return D





