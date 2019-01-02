from kzpy3.utils3 import *

import State
exec(identify_file_str)

def NetworkPID():
	"NetworkPID"
	D = State.State()
	CLASS_TYPE = NetworkPID.__doc__
	PARENT_TYPE = 'State'
	dkeys = D.keys()
	for k in dkeys:
		if type(k) != tuple:
			tup = (PARENT_TYPE,k)
			D[tup] = D[k]
	D['entry timer'] = None
	codefilename = d2n('(',fname(__file__),')')
	print '';print ''
	cy('Class',CLASS_TYPE,codefilename)

	D['impossible source states'] = ['Calibrate0','Calibrate1']
	D['possible source states'] = ['HumanPID','Human']
	D['impossible destination states'] = ['Calibrate1','Calibrate2']
	D['possible destination states'] = ['Calibrate0','HumanPID','Human']


	def f1(P):
		"Upon entry do this..."

		doc = f1.__doc__
		def parent(P):
			tup = (PARENT_TYPE,doc)
			cg('		',tup,D[tup],codefilename)
			return D[tup](P)
		cm('	function',CLASS_TYPE+'::'+doc,codefilename)
			
		if not parent(P):
			return False
		D['entry timer'] = Timer(0)
		return True


	def f2(P):
		"Is it time to exit?"

		doc = f2.__doc__
		def parent(P):
			tup = (PARENT_TYPE,doc)
			cg('		',tup,D[tup],codefilename)
			return D[tup](P)
		cm('	function',CLASS_TYPE+'::'+doc,codefilename)
			
		if not parent(P):
			return False
		return True


	def f3(P):
		"Upon exit do this..."

		doc = f3.__doc__
		def parent(P):
			tup = (PARENT_TYPE,doc)
			cg('		',tup,D[tup],codefilename)
			return D[tup](P)
		cm('	function',CLASS_TYPE+'::'+doc,codefilename)
			
		if not parent(P):
			return False
		return True

	for f in [f1,f2,f3,]:
		D[f.__doc__] = f
	
	
	return D




	








if __name__ == '__main__':

	#clear_screen()

	P={}
	P['current state'] = 'none'
	P['now in calibration mode'] = True
	
	S = State()
	S['dst_state'] = 'next state'
	S['entry timer'] = Timer(0.1)
	S['possible destination states'] = ['next state']
	S["Upon entry do this..."](P)
	S["Upon exit do this..."](P)
	time.sleep(0.2)
	S["Upon entry do this..."](P)
	S["Upon exit do this..."](P)

	pprint(P)





#EOF
