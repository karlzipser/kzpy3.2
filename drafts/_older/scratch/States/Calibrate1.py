
from kzpy3.utils3 import *

import State
exec(identify_file_str)

def Calibrate1():
	"Calibrate1"
	D = State.State()
	#D['depth'] += 1
	CLASS_TYPE = Calibrate1.__doc__
	PARENT_TYPE = 'State'
	#if D['depth'] > 0:
	#	for k in dkeys:
	#		D['_'+k] = D[k]
	dkeys = D.keys()
	for k in dkeys:
		if type(k) != tuple:
			tup = (PARENT_TYPE,k)
			D[tup] = D[k]
			cr(tup,':',D[k])
	#underscore_str = ''
	#for i in range(D['depth']+1):
	#	underscore_str += '_'
	CLASS_STRING = d2n("'",CLASS_TYPE,"'")
	D['regarding'] = d2s("Regarding",CLASS_STRING)
	D['entry timer'] = None
	#cy(D['regarding'],'depth =',D['depth'])

	D['impossible source states'] = ['Calibrate1','Calibrate2']
	D['possible destination states'] = ['Calibrate2']
	D['possible source states'] = ['Calibrate0']
	D['impossible destination states'] = ['Calibrate0','Calibrate1']
	

	def f1(P):
		"Can this state can be entered?"
		if not P['now in calibration mode']:
			cr("\tnot P['now in calibration mode'], cannot enter",D['state'])
			return False

		doc = f1.__doc__
		#cy(D['regarding'],doc)
		cG(doc,fname(__file__))
		def parent(P):
			tup = ((PARENT_TYPE,doc))
			cg(d2s(tup,D[tup],__file__,' | '))
			return D[tup](P)
		result = parent(P)
		cr(result)
		return result


	def f2(P):
		"Upon entry do this..."

		doc = f2.__doc__
		#cy(D['regarding'],doc)
		cG(doc,fname(__file__))
		def parent(P):
			tup = ((PARENT_TYPE,doc))
			cg(d2s(tup,D[tup],__file__,' | '))
			return D[tup](P)
		result = parent(P)
		if result == False:
			return
		D['entry timer'] = Timer(1.0)
		cb("""
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
