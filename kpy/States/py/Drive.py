from kzpy3.utils3 import *

import State
exec(identify_file_str)

def Drive():
	"Drive"
	D = State.State()
	CLASS_TYPE = Drive.__doc__
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

	D['impossible source states'] = ['Calibrate0','Calibrate1',]
	D['possible source states'] = []
	D['impossible destination states'] = ['Calibrate1','Calibrate2',]
	D['possible destination states'] = []

	for f in []:
		D[f.__doc__] = f
	print "DRIVE"
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
