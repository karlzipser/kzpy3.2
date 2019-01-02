
from kzpy3.utils3 import *

import Calibrate1
exec(identify_file_str)

def Calibrate2():
	"Calibrate2"
	D = Calibrate1.Calibrate1()
	CLASS_TYPE = Calibrate2.__doc__
	PARENT_TYPE = 'Calibrate1'
	dkeys = D.keys()
	for k in dkeys:
		if type(k) != tuple:
			tup = (PARENT_TYPE,k)
			D[tup] = D[k]
	D['entry timer'] = None
	codefilename = d2n('(',fname(__file__),')')
	print '';print ''
	cy('Class',CLASS_TYPE,codefilename)

	D['impossible source states'] = ['Calibrate0','Calibrate2']
	D['possible destination states'] = ['HumanPID']
	D['possible source states'] = ['Calibrate1']
	D['impossible destination states'] = ['Calibrate0','Calibrate1','Calibrate2']
	

	def f1(P):
		"Can this state can be entered?"
		if not P['now in calibration mode']:
			cr("\tnot P['now in calibration mode'], cannot enter",D['state'])
			return False

		doc = f1.__doc__
		def parent(P):
			tup = (PARENT_TYPE,doc)
			cg('		',tup,D[tup],codefilename)
			return D[tup](P)
		cm('	function',CLASS_TYPE+'::'+doc,codefilename)
			
		result = parent(P)
		#cr(result)
		return result


	def f2(P):
		"Upon entry do this..."

		doc = f2.__doc__
		def parent(P):
			tup = (PARENT_TYPE,doc)
			cg('		',tup,D[tup],codefilename)
			return D[tup](P)
		cm('	function',CLASS_TYPE+'::'+doc,codefilename)
			
		result = parent(P)
		if result == False:
			return
		D['entry timer'] = Timer(0)
		cb("""
            start.message('Calibrate now.')
            if P['servo_pwm_max'] < P['servo_pwm']:
                P['servo_pwm_max'] = P['servo_pwm']
            if P['servo_pwm_min'] > P['servo_pwm']:
                P['servo_pwm_min'] = P['servo_pwm']
            if P['motor_pwm_max'] < P['motor_pwm']:
                P['motor_pwm_max'] = P['motor_pwm']
            if P['motor_pwm_min'] > P['motor_pwm']:
                P['motor_pwm_min'] = P['motor_pwm']
            if P['servo_pwm_max'] - P['servo_pwm_min'] > 300:
                if P['motor_pwm_max'] - P['motor_pwm_min'] > 300:
                    P['calibrated'] = True
		""")
		return True



	def f3(P):
		"Is it time to exit?"

		doc = f3.__doc__
		def parent(P):
			tup = (PARENT_TYPE,doc)
			cg('		',tup,D[tup],codefilename)
			return D[tup](P)
		cm('	function',CLASS_TYPE+'::'+doc,codefilename)
			
		result = parent(P)
		if not result:
			return False
		if P['now in calibration mode']:
			cr("still in menu set P['now in calibration mode'], cannot exit.")
			return False
		if not P['calibrated']:
			cr("P['calibrated'] == False, cannot exit.")
			return False
		return True

	for f in [f1,f2,f3,]:
		D[f.__doc__] = f

	return D





if __name__ == '__main__':

	#clear_screen()

	P={}
	P['current state'] = 'Calibrate1'
	P['now in calibration mode'] = True
	P['calibrated'] = True
	S = Calibrate2()
	S['dst_state'] = 'HumanPID'
	S['possible destination states'] = ['HumanPID']
	S["Upon entry do this..."](P)
	S["Upon exit do this..."](P)
	time.sleep(2)
	S["Upon entry do this..."](P)
	S["Upon exit do this..."](P)
	P['calibrated'] = True
	time.sleep(1)
	P['now in calibration mode'] = False
	S["Upon exit do this..."](P)

	pprint(P)





#EOF
