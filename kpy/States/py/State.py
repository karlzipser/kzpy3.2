from kzpy3.utils3 import *
"""
python kzpy3/kpy/adjust.py py kzpy3/kpy/States/py kpy kzpy3/kpy/States/kpy && python kzpy3/kpy/States/py/State.py
"""


exec(identify_file_str)

def State():
	"State"
	D = {}
	CLASS_TYPE = State.__doc__
	PARENT_TYPE = 'None'
	dkeys = D.keys()
	for k in dkeys:
		if type(k) != tuple:
			tup = (PARENT_TYPE,k)
			D[tup] = D[k]
	D['entry timer'] = None
	codefilename = d2n('(',fname(__file__),')')
	print '';print ''
	cy('Class',CLASS_TYPE,codefilename)

	D['impossible source states'] = []
	D['possible source states'] = []
	D['impossible destination states'] = []
	D['possible destination states'] = []

	def f1(P):
		"Can this state can be entered?"

		doc = f1.__doc__
		def parent(P):
			tup = (PARENT_TYPE,doc)
			cg('		',tup,D[tup],codefilename)
			return D[tup](P)
		cm('	function',CLASS_TYPE+'::'+doc,codefilename)
			

		if CLASS_TYPE == P['current state']:
			cb("\t\t",CLASS_TYPE,': Already in',CLASS_TYPE+', cannot reenter now.')
			return False
		if P['current state'] not in D['impossible source states']:
			if P['current state'] in D['possible source states'] or \
				len(D['possible source states']) == 0:
				cb("\t\t",CLASS_TYPE,': can be entered.')
				return True
		cb("\t\t",CLASS_TYPE,': This state cannot be entered now.')
		return False


	def f2(P):
		"Upon entry do this..."

		doc = f2.__doc__
		def parent(P):
			tup = (PARENT_TYPE,doc)
			cg('		',tup,D[tup],codefilename)
			return D[tup](P)
		cm('	function',CLASS_TYPE+'::'+doc,codefilename)
			
		
		if not D["Can this state can be entered?"](P):
			return False
		P['current state'] = CLASS_TYPE
		if D['entry timer'] != None:
			D['entry timer'].reset()		
		cb("\t\t",CLASS_TYPE,': Entering state',CLASS_TYPE+'.')
		return True


	def f3(P):
		"Is it time to exit?"

		doc = f3.__doc__
		def parent(P):
			tup = (PARENT_TYPE,doc)
			cg('		',tup,D[tup],codefilename)
			return D[tup](P)
		cm('	function',CLASS_TYPE+'::'+doc,codefilename)
			
		if CLASS_TYPE != P['current state']:
			cb("\t\t",CLASS_TYPE,': Not in state',CLASS_TYPE+", so can't exit.")
			return False
		cw("\t\tentry timer check: ",D['entry timer'].check(),D['entry timer'].time())
		if D['entry timer'].check():
			cb("\t\t",CLASS_TYPE,': It is time to exit.')
			return True
		cb("\t\t",CLASS_TYPE,': It is not time to exit.')
		return False


	def f4(P):
		"Upon exit do this..."

		doc = f4.__doc__
		def parent(P):
			tup = (PARENT_TYPE,doc)
			cg('		',tup,D[tup],codefilename)
			return D[tup](P)
		cm('	function',CLASS_TYPE+'::'+doc,codefilename)
			
		if CLASS_TYPE != P['current state']:
			cb("\t\t",CLASS_TYPE,': Not in state',CLASS_TYPE+", so can't exit.")
			return False
		if D['dst_state'] not in D['possible destination states']:
			cb("\t\t",CLASS_TYPE,':',+D['dst_state']+"' is not a suitable destination for",CLASS_TYPE+'.')
			return False
		if D['Is it time to exit?'](P):
			cb("\t\t",CLASS_TYPE,': Leaving state',CLASS_TYPE,"for '"+D['dst_state']+"'.")
			P['current state'] = D['dst_state']
			return True
		cb("\t\t",CLASS_TYPE,': Not exiting yet.')
		return False

	for f in [f1,f2,f3,f4,]:
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
