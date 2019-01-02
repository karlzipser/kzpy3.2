from kzpy3.utils3 import *


exec(identify_file_str)

def State():
	"State"
	D = {}
	#D['depth'] += 1
	CLASS_TYPE = State.__doc__
	PARENT_TYPE = 'None'
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

	D['impossible source states'] = []
	D['possible source states'] = []
	D['impossible destination states'] = []
	D['possible destination states'] = []

	def f1(P):
		"Can this state can be entered?"

		doc = f1.__doc__
		#cy(D['regarding'],doc)
		cG(doc,fname(__file__))
		def parent(P):
			tup = ((PARENT_TYPE,doc))
			cg(d2s(tup,D[tup],__file__,' | '))
			return D[tup](P)
		if CLASS_TYPE == P['current state']:
			cb('\tAlready in',CLASS_STRING+', cannot reenter now.')
			return False
		if P['current state'] not in D['impossible source states']:
			if P['current state'] in D['possible source states'] or \
				len(D['possible source states']) == 0:
				cb('\t',CLASS_STRING,'can be entered.')
				return True
		cb('\tThis state cannot be entered now.')
		return False


	def f2(P):
		"Upon entry do this..."

		doc = f2.__doc__
		#cy(D['regarding'],doc)
		cG(doc,fname(__file__))
		def parent(P):
			tup = ((PARENT_TYPE,doc))
			cg(d2s(tup,D[tup],__file__,' | '))
			return D[tup](P)
		if not D["Can this state can be entered?"](P):
			return False
		P['current state'] = CLASS_TYPE
		if D['entry timer'] != None:
			D['entry timer'].reset()		
		cb('\tEntering state',CLASS_STRING+'.')
		return True


	def f3(P):
		"Is it time to exit?"

		doc = f3.__doc__
		#cy(D['regarding'],doc)
		cG(doc,fname(__file__))
		def parent(P):
			tup = ((PARENT_TYPE,doc))
			cg(d2s(tup,D[tup],__file__,' | '))
			return D[tup](P)
		if CLASS_TYPE != P['current state']:
			cb('\tNot in state',CLASS_TYPE+", so can't exit.")
			return False
		print (D['entry timer'].check(),D['entry timer'].time())
		if D['entry timer'].check():
			cb('\tIt is time to exit.')
			return True
		cb('\tIt is not time to exit.')
		return False


	def f4(P):
		"Upon exit do this..."

		doc = f4.__doc__
		#cy(D['regarding'],doc)
		cG(doc,fname(__file__))
		def parent(P):
			tup = ((PARENT_TYPE,doc))
			cg(d2s(tup,D[tup],__file__,' | '))
			return D[tup](P)
		if CLASS_TYPE != P['current state']:
			cb('\tNot in state',CLASS_STRING+", so can't exit.")
			return False
		if D['dst_state'] not in D['possible destination states']:
			cb("\t'"+D['dst_state']+"' is not a suitable destination for",CLASS_STRING+'.')
			return False
		if D['Is it time to exit?'](P):
			cb('\tLeaving state',CLASS_STRING,"for '"+D['dst_state']+"'.")
			P['current state'] = D['dst_state']
			return True
		cb('\tNot exiting yet.')
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
