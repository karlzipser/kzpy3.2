
from kzpy3.utils3 import *

import State
exec(identify_file_str)

def Calibrate1():
	"Calibrate1"
	D = State.State()
	CLASS_TYPE = Calibrate1.__doc__
	PARENT_TYPE = 'State'
	dkeys = D.keys()
	for k in dkeys:
		if type(k) != tuple:
			tup = (PARENT_TYPE,k)
			D[tup] = D[k]
	if PARENT_TYPE == 'None':
		D[(PARENT_TYPE,'depth')] = -1
	D['depth'] = D[(PARENT_TYPE,'depth')] + 1
	#print(CLASS_TYPE,D['depth'] )
	indent = d2n(' ',D['depth'],')',D['depth']*'  ')
	D['entry timer'] = None
	codefilename = d2n('(',fname(__file__),')')
	print '';print ''
	cy(indent+'Class',CLASS_TYPE,codefilename)

	D['impossible source states'] = ['Calibrate1','Calibrate2']
	D['possible destination states'] = ['Calibrate2']
	D['possible source states'] = ['Calibrate0']
	D['impossible destination states'] = ['Calibrate0','Calibrate1']
	

	def f1(P):
		"Can this state can be entered?"
		if not P['now in calibration mode']:
			cr(indent,"not P['now in calibration mode'], cannot enter",D['state'])
			return False

		doc = f1.__doc__
		def parent(P):
			tup = (PARENT_TYPE,doc)
			cg(indent,tup,D[tup],codefilename)
			return D[tup](P)
		cm(indent+'function',CLASS_TYPE+'::'+doc,codefilename)
			
		result = parent(P)
		return result


	def f2(P):
		"Upon entry do this..."

		doc = f2.__doc__
		def parent(P):
			tup = (PARENT_TYPE,doc)
			cg(indent,tup,D[tup],codefilename)
			return D[tup](P)
		cm(indent+'function',CLASS_TYPE+'::'+doc,codefilename)
			
		result = parent(P)
		if result == False:
			return
		D['entry timer'] = Timer(1.0)
		cb(indent,"""
			s = P['HUMAN_SMOOTHING_PARAMETER_1']
			P['servo_pwm_null'] = (1.0-s)*P['servo_pwm'] + s*P['servo_pwm_null']
			P['motor_pwm_null'] = (1.0-s)*P['motor_pwm'] + s*P['motor_pwm_null']
			P['servo_pwm_min'] = P['servo_pwm_null']
			P['servo_pwm_max'] = P['servo_pwm_null']
			P['motor_pwm_min'] = P['motor_pwm_null']
			P['motor_pwm_max'] = P['motor_pwm_null']
			P['servo_pwm_smooth'] = P['servo_pwm_null']
			P['motor_pwm_smooth'] = P['motor_pwm_null']
		""")
		return True





	for f in [f1,f2,]:
		D[f.__doc__] = f

	return D




	








if __name__ == '__main__':

	#clear_screen()

	P={}
	P['current state'] = 'Calibrate0'
	P['now in calibration mode'] = True
	
	S = Calibrate1()
	S['dst_state'] = 'next state'
	S['possible destination states'] = ['next state']
	S["Upon entry do this..."](P)
	S["Upon exit do this..."](P)
	time.sleep(2)
	S["Upon entry do this..."](P)
	S["Upon exit do this..."](P)

	pprint(P)





#EOF
