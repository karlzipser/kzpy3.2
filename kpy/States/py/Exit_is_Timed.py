from kzpy3.utils3 import *
"""
python kzpy3/kpy/adjust.py py kzpy3/kpy/States/py kpy kzpy3/kpy/States/kpy && python kzpy3/kpy/States/py/State.py
"""

import State
exec(identify_file_str)

def Exit_is_Timed():
	"Exit_is_Timed"
	D = State.State()
	CLASS_TYPE = Exit_is_Timed.__doc__
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

	D['impossible source states'] = []
	D['possible source states'] = []
	D['impossible destination states'] = []
	D['possible destination states'] = []


	def f1(P):
		"Is it time to exit?"

		doc = f1.__doc__
		def parent(P):
			tup = (PARENT_TYPE,doc)
			#cg(indent,tup,D[tup],codefilename)
			return D[tup](P)
		cw(indent+CLASS_TYPE+'::'+doc,codefilename)
			
		if CLASS_TYPE != P['current state']:
			cb(indent+CLASS_TYPE,': Not in state',CLASS_TYPE+", so can't exit.")
			return False
		cb(indent+"entry timer check: ",D['entry timer'].check(),D['entry timer'].time())
		if D['entry timer'].check():
			cb(indent+CLASS_TYPE,': It is time to exit.')
			return True
		cb(indent+CLASS_TYPE,': It is not time to exit.')
		return False


	def f2(P):
		"Upon entry do this..."

		doc = f2.__doc__
		def parent(P):
			tup = (PARENT_TYPE,doc)
			#cg(indent,tup,D[tup],codefilename)
			return D[tup](P)
		cw(indent+CLASS_TYPE+'::'+doc,codefilename)
			
		D['entry timer'] = Timer(0.1)
		return True
		
	for f in [f1,f2,]:
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
