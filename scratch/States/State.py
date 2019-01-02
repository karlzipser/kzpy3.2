from kzpy3.utils3 import *


exec(identify_file_str)

def State():
	"State"
	D = {}
	D['depth'] = 0
	dkeys = D.keys()
	if D['depth'] > 0:
		for k in dkeys:
			D['_'+k] = D[k]
	underscore_str = ''
	for i in range(D['depth']+1):
		underscore_str += '_'
	D['type'] = State.__doc__
	D['state'] = d2n("'",D['type'],"'")
	D['regarding'] = d2s("Regarding",D['state'])
	D['entry timer'] = None
	cy(D['regarding'],'depth =',D['depth'])

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
			#cg("parent")
			return D[underscore_str+doc](P)
		if D['type'] == P['current state']:
			cb('\tAlready in',D['state']+', cannot reenter now.')
			return False
		if P['current state'] not in D['impossible source states']:
			if P['current state'] in D['possible source states'] or \
				len(D['possible source states']) == 0:
				cb('\t',D['state'],'can be entered.')
				return True
		cb('\tThis state cannot be entered now.')
		return False


	def f2(P):
		"Upon entry do this..."

		doc = f2.__doc__
		#cy(D['regarding'],doc)
		cG(doc,fname(__file__))
		def parent(P):
			#cg("parent")
			return D[underscore_str+doc](P)
		if not D["Can this state can be entered?"](P):
			return False
		P['current state'] = D['type']
		if D['entry timer'] != None:
			D['entry timer'].reset()		
		cb('\tEntering state',D['state']+'.')
		return True


	def f3(P):
		"Is it time to exit?"

		doc = f3.__doc__
		#cy(D['regarding'],doc)
		cG(doc,fname(__file__))
		def parent(P):
			#cg("parent")
			return D[underscore_str+doc](P)
		if D['type'] != P['current state']:
			cb('\tNot in state',D['type']+", so can't exit.")
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
			#cg("parent")
			return D[underscore_str+doc](P)
		if D['type'] != P['current state']:
			cb('\tNot in state',D['state']+", so can't exit.")
			return False
		if D['dst_state'] not in D['possible destination states']:
			cb("\t'"+D['dst_state']+"' is not a suitable destination for",D['state']+'.')
			return False
		if D['Is it time to exit?'](P):
			cb('\tLeaving state',D['state'],"for '"+D['dst_state']+"'.")
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
