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
	for i in range(D['depth']):
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
		cy(D['regarding'],doc)
		def parent(P):
			cg("parent")
			return D[underscore_str+doc](P)

		if D['type'] == P['current state']:
			cb('\tAlready in',D['state']+', cannot reenter now.')
			cr('\t',False)
			return False
 
		if P['current state'] not in D['impossible source states']:
			if P['current state'] in D['possible source states'] or \
				len(D['possible source states']) == 0:

				cb('\t',D['state'],'can be entered.')
				cg('\t',True)
				return True

		cb('\tThis state cannot be entered now.')
		cr('\t',False)
		return False



	def f2(P):
		"Upon entry do this..."

		doc = f2.__doc__
		cy(D['regarding'],doc)
		def parent(P):
			cg("parent")
			return D[underscore_str+doc](P)
		
		if not D["Can this state can be entered?"](P):
			cr('\t',False)
			return False

		P['current state'] = D['type']
		D['entry timer'].reset()

		
		cb('\tEntering state',D['state']+'.')
		cb('\tUpon entry:')
		cg('\t',True)
		return True



	def f3(P):
		"Is it time to exit?"

		doc = f3.__doc__
		cy(D['regarding'],doc)
		def parent(P):
			cg("parent")
			return D[underscore_str+doc](P)
		
		if D['type'] != P['current state']:
			cb('\tNot in state',D['type']+", so can't exit.")
			cr('\t',False)
			return False
		print D['entry timer'].check(),D['entry timer'].time()
		if D['entry timer'].check():
			cb('\tIt is time to exit.')
			cg('\t',True)
			return True
		cb('\tIt is not time to exit.')
		cr('\t',False)
		return False


	def f4(P):
		"Upon exit do this..."

		doc = f4.__doc__
		cy(D['regarding'],doc)
		def parent(P):
			cg("parent")
			return D[underscore_str+doc](P)
		
		if D['type'] != P['current state']:
			cb('\tNot in state',D['state']+", so can't exit.")
			cr('\t',False)
			return False
		if D['dst_state'] not in D['possible destination states']:
			cb("\t'"+D['dst_state']+"' is not a suitable destination for",D['state']+'.')
			cr('\t',False)
			return False
		if D['Is it time to exit?'](P):
			cb('\tLeaving state',D['state'],"for '"+D['dst_state']+"'.")
			P['current state'] = D['dst_state']
			cg('\t',True)
			return True
		cb('\tNot exiting yet.')
		cr('\t',False)
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
