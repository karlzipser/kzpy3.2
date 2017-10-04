import threading
from kzpy3.utils2 import *
import std_msgs.msg
import rospy
import runtime_parameters as rp



lock = threading.Lock()

os.environ['STOP'] = 'False'


def mse_write_publish(M,Arduinos,steer_pwm,motor_pwm):
	write_str = d2n( '(', int(steer_pwm), ',', int(motor_pwm+10000), ')')
	M['Arduinos_MSE_write'](write_str)
	steer_percent = pwm_to_percent(M,M['steer_null'],steer_pwm,M['steer_max'],M['steer_min'])
	motor_percent = pwm_to_percent(M,M['motor_null'],motor_pwm,M['motor_max'],M['motor_min'])
	M['steer_pub'].publish(std_msgs.msg.Int32(steer_percent))
	M['motor_pub'].publish(std_msgs.msg.Int32(motor_percent))
	M['state_pub'].publish(std_msgs.msg.Int32(M['current_state'].number))
	#M['potential_collision_pub'].publish(std_msgs.msg.Int32(M['potential_collision']))

class State():
	def __init__(self,name,number,button_pwm_peak,M,Arduinos):
		self.name = name
		self.number = number
		self.button_pwm_peak = button_pwm_peak
		self.Arduinos = Arduinos
		self.state_transition_timer = None
		self.M = M
	def enter(self):
		print('Entering '+self.name)
		self.state_transition_timer = Timer(0)
	def process(self):
		pass
	def leave(self):
		self.state_transition_timer = None


class Run_State(State):
	def __init__(self,name,number,button_pwm_peak,M,Arduinos):
		State.__init__(self,name,number,button_pwm_peak,M,Arduinos)
	def enter(self):
		self.led()
		State.enter(self)
	def led(self):
		LED_signal = d2n('(',self.number,')')
		if 'SIG' in self.Arduinos.keys():
			self.Arduinos['SIG'].write(LED_signal)


class Human_Control(Run_State):
	def __init__(self,name,number,button_pwm_peak,M,Arduinos):
		Run_State.__init__(self,name,number,button_pwm_peak,M,Arduinos)
	def process(self):
		mse_write_publish(self.M,self.Arduinos,self.M['smooth_steer'],self.M['smooth_motor'])



class Calibration_State(Run_State):
	def __init__(self,name,number,button_pwm_peak,M,Arduinos):
		Run_State.__init__(self,name,number,button_pwm_peak,M,Arduinos)
	def leave(self):
		Run_State.leave(self)
		self.M['steer_pwm_lst'] = [self.M['steer_null']]
		self.M['motor_pwm_lst'] = [self.M['motor_null']]



class Net_Steer_Net_Motor(Run_State):
	def process(self):
		self.M['caffe_steer_pwm'] = percent_to_pwm(self.M['caffe_steer'],self.M['steer_null'],self.M['steer_max'],self.M['steer_min'])
		self.M['caffe_motor_pwm'] = percent_to_pwm(self.M['caffe_motor'],self.M['motor_null'],self.M['motor_max'],self.M['motor_min'])
		mse_write_publish(self.M,self.Arduinos,self.M['caffe_steer_pwm'],self.M['caffe_motor_pwm'])







def buttons_to_state(Arduinos,M,BUTTON_DELTA):

	if np.abs(M['smooth_button'] - M['state_four'].button_pwm_peak) < BUTTON_DELTA:
		if M['current_state'] == None:
			M['current_state'] = M['state_four']
			M['current_state'].enter()
			return
		if M['current_state'] == M['state_four']:
			return
		M['previous_state'] = M['current_state']
		M['current_state'] = M['state_four']
		M['current_state'].enter()
		M['previous_state'].leave()
		return

	if M['current_state'] == None:
		return

	for s in [M['state_one'],M['state_two'],M['state_six']]:
		if np.abs(M['smooth_button'] - s.button_pwm_peak) < BUTTON_DELTA:  
			if M['current_state'] == s:
				return
			M['previous_state'] = M['current_state']
			M['current_state'] = s
			M['current_state'].enter()
			M['previous_state'].leave()
			return






##############################################################3
#
def setup(M,Arduinos):

	if not rp.require_Arudinos_MSE:
		spd2s('NOTE: rp.require_Arudinos_MSE == False, using dummy MSE values')
		def dummy_write(_nothing_):
			return
		def dummy_read():
			return ('mse',1450,1450,1450,2.0)
		M['Arduinos_MSE_write'] = dummy_write
		M['Arduinos_MSE_readline'] = dummy_read
	else:
		M['Arduinos_MSE_write'] = Arduinos['MSE'].write
		M['Arduinos_MSE_readline'] = Arduinos['MSE'].readline
	"""
	M['n_avg_steer'] = 20
	M['n_avg_motor'] = 20
	M['n_avg_button'] = 15
	M['n_avg_encoder'] = 100
	"""
	M['steer_null'] = 1400
	M['motor_null'] = 1500
	M['steer_percent'] = 49
	M['motor_percent'] = 49
	M['steer_max'] = M['steer_null']+1
	M['motor_max'] = M['motor_null']+1
	M['steer_min'] = M['motor_null']-1
	M['motor_min'] = M['motor_null']-1
	M['set_null'] = False


	for q in ['button_pwm_lst',
		'steer_pwm_lst',
		'motor_pwm_lst',
		'steer_pwm_write_lst',
		'motor_pwm_write_lst',
		'encoder_lst']:
		M[q] = []

	M['previous_state'] = None
	M['calibrated'] = False
	M['PID'] = [-1,-1]

	M['state_one'] = Human_Control('state 1',1,1700,M,Arduinos)
	M['state_two'] = Human_Control('state 2',2,1424,M,Arduinos)
	M['state_six'] = Net_Steer_Net_Motor('state 6',6,1900,M,Arduinos)
	M['state_four'] = Calibration_State('state 4',4,870,M,Arduinos)

	M['current_state'] = None
	M['caffe_steer'] = 49
	M['caffe_steer_pwm'] = M['steer_null']
	M['caffe_motor'] = 49
	M['caffe_motor_pwm'] = M['motor_null']
	M['n_lst_steps'] = 10

	print("MSE setup.")

calibration_signal_timer = Timer(0.01)
#        
##############################################################3
#


def run_loop(Arduinos,M,BUTTON_DELTA=50,):

	lock = threading.Lock()
	if 'MSE' not in Arduinos:
		M['Stop_Arduinos'] = True
		stop_ros()
		return


	if True:#try:
		if os.environ['STOP'] == 'True':
			assert(False)
		while M['Stop_Arduinos'] == False or not rospy.is_shutdown():
			
			if not serial_data_to_messages(Arduinos,M):
				continue

			M['smooth_motor'] = np.median(na(M['motor_pwm_lst'][-M['n_lst_steps']:]))
			M['smooth_steer'] = np.median(na(M['steer_pwm_lst'][-M['n_lst_steps']:]))
			M['smooth_button'] = np.median(na(M['button_pwm_lst'][-M['n_lst_steps']:]))

			buttons_to_state(Arduinos,M,BUTTON_DELTA)

			if M['current_state'] == None:
				continue

			manage_list_lengths(M)

			
			if M['current_state'] == M['state_four']:
				process_state_4(M)
				M['state_pub'].publish(std_msgs.msg.Int32(M['current_state'].number))
				continue
			else:
				if not calibrated(Arduinos,M):
					continue

			M['steer_percent'] = pwm_to_percent(M,M['steer_null'],M['smooth_steer'],M['steer_max'],M['steer_min'])
			M['motor_percent'] = pwm_to_percent(M,M['motor_null'],M['smooth_motor'],M['motor_max'],M['motor_min'])

			M['raw_write_str'] = d2n( '(', int(M['smooth_steer']), ',', int(M['smooth_motor']+10000), ')')

			M['current_state'].process()

			M['state_pub'].publish(std_msgs.msg.Int32(M['current_state'].number))

	else:#except Exception as e:
		print("********** def run_loop(Arduinos,M,BUTTON_DELTA=50,): Exception ***********************")
		print(e.message, e.args)
		os.environ['STOP'] = 'True'
		M['Stop_Arduinos'] = True
		rospy.signal_shutdown(d2s(e.message,e.args))
		LED_signal = d2n('(10000)')
		if 'SIG' in Arduinos.keys():
			Arduinos['SIG'].write(LED_signal)

#        
##############################################################3
#


def calibrated(Arduinos,M):
	if not M['calibrated']:
		if calibration_signal_timer.check():
			s = np.random.choice([1,2,3,5,6,7,9])
			LED_signal = d2n('(',s,')')
			if 'SIG' in Arduinos.keys():
				Arduinos['SIG'].write(LED_signal)
			calibration_signal_timer.reset()
		return False
	return True



def serial_data_to_messages(Arduinos,M):
	read_str = M['Arduinos_MSE_readline']()
	try:
		exec('mse_input = list({0})'.format(read_str))
	except:
		return False
	if len(mse_input) == 5 and mse_input[0] == 'mse':
		lock.acquire()
		M['button_pwm_lst'].append(mse_input[1])
		M['steer_pwm_lst'].append(mse_input[2])
		M['motor_pwm_lst'].append(mse_input[3])
		M['encoder_lst'].append(mse_input[4])
		M['encoder_pub'].publish(std_msgs.msg.Float32(M['encoder_lst'][-1]))
		lock.release()
		return True
	else:
		return False

	
	 

def manage_list_lengths(M):
	lock.acquire()
	for k in M:
		if type(M[k]) == list:        
			if len(M[k]) > 2 * M['n_lst_steps']:
				M[k] = M[k][-M['n_lst_steps']:]
	lock.release() 



def process_state_4(M):
	M['calibrated'] = False
	if M['current_state'].state_transition_timer.time() < 0.5:
		M['set_null'] = False
	else:
		if M['set_null'] == False:
			M['steer_null'] = np.median(na(M['steer_pwm_lst'][-M['n_lst_steps']:]))
			M['motor_null'] = np.median(na(M['motor_pwm_lst'][-M['n_lst_steps']:]))
			M['set_null'] = True
			M['steer_max'] = M['steer_null']
			M['motor_max'] = M['motor_null']
			M['steer_min'] = M['steer_null']
			M['motor_min'] = M['motor_null']
		else:
			if M['smooth_steer'] > M['steer_max']:
				M['steer_max'] = M['smooth_steer']
			if M['smooth_motor'] > M['motor_max']:
				M['motor_max'] = M['smooth_motor']
			if M['smooth_steer'] < M['steer_min']:
				M['steer_min'] = M['smooth_steer']
			if M['smooth_motor'] < M['motor_min']:
				M['motor_min'] = M['smooth_motor']

	if np.abs(M['steer_max']-M['steer_min']) > 700 and np.abs(M['motor_max']-M['motor_min']) > 600:
		print M['steer_max']-M['steer_min'],M['motor_max']-M['motor_min']
		M['calibrated'] = True

	 

def pwm_to_percent(M,null_pwm,current_pwm,max_pwm,min_pwm):
	current_pwm -= null_pwm
	max_pwm -= null_pwm
	min_pwm -= null_pwm
	if np.abs(min_pwm)<10 or np.abs(min_pwm)<10:
		M['calibrated'] = False
		return 49
	if current_pwm >= 0:
		p = int(99*(1.0 + current_pwm/max_pwm)/2.0)
	else:
		p = int(99*(1.0 - current_pwm/min_pwm)/2.0)
	if p > 99:
		p = 99
	if p < 0:
		p = 0      
	return p


def percent_to_pwm(percent,null_pwm,max_pwm,min_pwm):
	if percent >= 49:
		p = (percent-50)/50.0 * (max_pwm-null_pwm) + null_pwm
	else:
		p = (percent-50)/50.0 * (null_pwm-min_pwm) + null_pwm
	return p







#        
##############################################################3
#EOF

