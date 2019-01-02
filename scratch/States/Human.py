from kzpy3.utils3 import *

import State
exec(identify_file_str)

def NetworkPID():
	"NetworkPID"
	D = State.State()
	D['depth'] += 1
	dkeys = D.keys()
	if D['depth'] > 0:
		for k in dkeys:
			D['_'+k] = D[k]
	underscore_str = ''
	for i in range(D['depth']+1):
		underscore_str += '_'
	D['type'] = NetworkPID.__doc__
	D['state'] = d2n("'",D['type'],"'")
	D['regarding'] = d2s("Regarding",D['state'])
	D['entry timer'] = None
	cy(D['regarding'],'depth =',D['depth'])

	D['impossible source states'] = ['Calibrate0','Calibrate1']
	D['possible source states'] = ['HumanPID','NetworkPID']
	D['impossible destination states'] = ['Calibrate1','Calibrate2']
	D['possible destination states'] = ['Calibrate0','HumanPID','NetworkPID']


	def f1(P):
		"Upon entry do this..."

		doc = f1.__doc__
		#cy(D['regarding'],doc)
		cG(doc,fname(__file__))
		def parent(P):
			#cg("parent")
			return D[underscore_str+doc](P)
		if not parent(P):
			return False
		D['entry timer'] = Timer(0)
		return True


	def f2(P):
		"Is it time to exit?"

		doc = f2.__doc__
		#cy(D['regarding'],doc)
		cG(doc,fname(__file__))
		def parent(P):
			#cg("parent")
			return D[underscore_str+doc](P)
		if not parent(P):
			return False
		return True


	def f3(P):
		"Upon exit do this..."

		doc = f3.__doc__
		#cy(D['regarding'],doc)
		cG(doc,fname(__file__))
		def parent(P):
			#cg("parent")
			return D[underscore_str+doc](P)
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
