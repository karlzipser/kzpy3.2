
from kzpy3.utils3 import *


exec(identify_file_str)

def Calibrate0(D):
	"Calibrate0"
	CLASS_TYPE = Calibrate0.__doc__
	D['depth'] = D[(PARENT_TYPE,'depth')] + 1
	indent = ''
	codefilename = d2n('(',fname(__file__),')')

	D['impossible source states'] = ['Calibrate0','Calibrate1','Calibrate2']
	D['possible destination states'] = ['Calibrate1']
	D['possible source states'] = []
	D['impossible destination states'] = ['Calibrate0','Calibrate2']
	

	def f1(D,P):
		"Can this state can be entered?"
		if not P['now in calibration mode']:
			cr(indent+CLASS_TYPE+"\tnot P['now in calibration mode'], cannot enter",D['state'])
			return False

		doc = f1.__doc__
		cw(indent+CLASS_TYPE+'::'+doc,codefilename)
			
		result = parent(P)
		return result


	def f2(D,P):
		"Upon entry do this..."

		doc = f2.__doc__
		cw(indent+CLASS_TYPE+'::'+doc,codefilename)
			
		
		if not D["Can this state can be entered?"](P):
			return False
		result = parent(P)
		if result == False:
			return False
		P['current state'] = CLASS_TYPE		
		cb(indent+CLASS_TYPE,': Entering state',CLASS_TYPE+'.')
		return True



		cr(indent+CLASS_TYPE,"""
		P['calibrated'] = False
		P['servo_pwm_null'] = P['servo_pwm']
		P['motor_pwm_null'] = P['motor_pwm']
		D['entry timer'] = Timer(1.1)
			""")
		return True



	def f3(D,P):
		"Is it time to exit?"

		doc = f3.__doc__
		cw(indent+CLASS_TYPE+'::'+doc,codefilename)
			
		result = parent(P)
		return result



	def f4(D,P):
		"Upon exit do this..."

		doc = f4.__doc__
		cw(indent+CLASS_TYPE+'::'+doc,codefilename)
			
		result = parent(P)
		return result

	for f in [f1,f2,f3,f4,]:
		D[(CLASS_TYPE,f.__doc__)] = f

	return D




	








if __name__ == '__main__':

	#clear_screen()

	P={}
	P['current state'] = 'none'
	P['now in calibration mode'] = True
	
	S = Calibrate0()
	S['dst_state'] = 'next state'
	S['possible destination states'] = ['next state']
	S["Upon entry do this..."](P)
	S["Upon exit do this..."](P)
	time.sleep(0.2)
	S["Upon entry do this..."](P)
	S["Upon exit do this..."](P)

	pprint(P)





#EOF
