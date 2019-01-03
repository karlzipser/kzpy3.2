
from kzpy3.utils3 import *

import State
exec(identify_file_str)

def Calibrate0():
	"Calibrate0"
	D = State.State()
	CLASS_TYPE = Calibrate0.__doc__
	PARENT_TYPE = 'State'
	dkeys = D.keys()
	for k in dkeys:
		if type(k) != tuple:
			tup = (PARENT_TYPE,k)
			D[tup] = D[k]
	if PARENT_TYPE == 'None':
		D[(PARENT_TYPE,'depth')] = -1
	D['depth'] = D[(PARENT_TYPE,'depth')] + 1
	indent = d2n(D['depth'],')','  '*(3-D['depth']))
	indent = ''
	indent = d2n('  '*(3-D['depth']))
	D['entry timer'] = None
	codefilename = d2n('(',fname(__file__),')')
	#print '';print ''
	#cy(indent+'Class',CLASS_TYPE,codefilename)

	D['impossible source states'] = ['Calibrate0','Calibrate1','Calibrate2']
	D['possible destination states'] = ['Calibrate1']
	D['possible source states'] = []
	D['impossible destination states'] = ['Calibrate0','Calibrate2']
	

	def f1(P):
		"Can this state can be entered?"
		if not P['now in calibration mode']:
			cr(indent+CLASS_TYPE+"\tnot P['now in calibration mode'], cannot enter",D['state'])
			return False

		doc = f1.__doc__
		def parent(P):
			tup = (PARENT_TYPE,doc)
			#cg(indent,tup,D[tup],codefilename)
			return D[tup](P)
		cw(indent+CLASS_TYPE+'::'+doc,codefilename)
			
		result = parent(P)
		return result


	def f2(P):
		"Upon entry do this..."

		doc = f2.__doc__
		def parent(P):
			tup = (PARENT_TYPE,doc)
			#cg(indent,tup,D[tup],codefilename)
			return D[tup](P)
		cw(indent+CLASS_TYPE+'::'+doc,codefilename)
			
		result = parent(P)
		if result == False:
			return
		D['entry timer'] = Timer(0.1)

		cr(indent+CLASS_TYPE,"""
		P['calibrated'] = False
		P['servo_pwm_null'] = P['servo_pwm']
		P['motor_pwm_null'] = P['motor_pwm']
		D['entry timer'] = Timer(1.1)
			""")
		return True



	def f3(P):
		"Is it time to exit?"

		doc = f3.__doc__
		def parent(P):
			tup = (PARENT_TYPE,doc)
			#cg(indent,tup,D[tup],codefilename)
			return D[tup](P)
		cw(indent+CLASS_TYPE+'::'+doc,codefilename)
			
		result = parent(P)
		return result



	def f4(P):
		"Upon exit do this..."

		doc = f4.__doc__
		def parent(P):
			tup = (PARENT_TYPE,doc)
			#cg(indent,tup,D[tup],codefilename)
			return D[tup](P)
		cw(indent+CLASS_TYPE+'::'+doc,codefilename)
			
		result = parent(P)
		return result

	for f in [f1,f2,f3,f4,]:
		D[f.__doc__] = f

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
