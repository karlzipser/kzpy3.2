from kzpy3.utils3 import *
"""
python kzpy3/kpy/adjust.py py kzpy3/kpy/States/py kpy kzpy3/kpy/States/kpy && python kzpy3/kpy/States/py/State.py
"""


exec(identify_file_str)

def State(D):
	"State"

	codefilename = d2n('(',fname(__file__),')')

	def f1(D,P):
		"Can this state can be entered?"
		if CLASS_TYPE == P['current state']:
			cb(CLASS_TYPE,': Already in',CLASS_TYPE+', cannot reenter now.')
			return False
		if P['current state'] not in D['impossible source states']:
			if P['current state'] in D['possible source states'] or \
				len(D['possible source states']) == 0:
				cb(CLASS_TYPE,': can be entered.')
				return True
		cb(CLASS_TYPE,': This state cannot be entered now.')
		return False

	def f2(D,P):
		"Upon exit do this..."
		doc = f2.__doc__
		if P['class type'] != P['current state']:
			cb(CLASS_TYPE,': Not in state',CLASS_TYPE+", so can't exit.")
			return False
		if D['dst state'] not in D['possible destination states']:
			cb(CLASS_TYPE,':',+D['dst state']+"' is not a suitable destination for",CLASS_TYPE+'.')
			return False
		if D['Is it time to exit?'](P):
			cb(CLASS_TYPE,': Leaving state',CLASS_TYPE,"for '"+D['dst state']+"'.")
			P['current state'] = D['dst state']
			return True
		cb(CLASS_TYPE,': Not exiting yet.')
		return False

	for f in [f1,f2,]:
		D[(CLASS_TYPE,f.__doc__)] = f
	
	return D




	








if __name__ == '__main__':

	#clear_screen()

	P={}
	P['current state'] = 'none'
	P['now in calibration mode'] = True
	
	S = State()
	S['D['dst state']'] = 'next state'
	S['entry timer'] = Timer(0.1)
	S['possible destination states'] = ['next state']
	S["Upon entry do this..."](P)
	S["Upon exit do this..."](P)
	time.sleep(0.2)
	S["Upon entry do this..."](P)
	S["Upon exit do this..."](P)

	pprint(P)





#EOF
