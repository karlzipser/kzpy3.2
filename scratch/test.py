from kzpy3.utils3 import *

import test_base

def test():
    "test"
    D = test_base.test_base()
    D['depth'] += 1
    dkeys = D.keys()
    for k in dkeys:
        D['_'+k] = D[k]
    underscore_str = ''
    for i in range(D['depth']):
        underscore_str += '_'
    D['type'] = test.__doc__
    D['state'] = d2n("'",D['type'],"'")
    D['regarding'] = d2s("Regarding",D['state'])
    cb(D['regarding'],'depth =',D['depth'])



    def f1(P):
        "Upon entry do this..."

        doc = f1.__doc__
        v = D['verbose']
        re = D['regarding']
        def parent(P):
            cg("parent")
            return D[underscore_str+doc](P)
        result = parent(P)
        if result == False:
            return
        cb("""s = P['HUMAN_SMOOTHING_PARAMETER_1']""")
        return True


    def f2(P):
        "Can this state can be entered?"

        doc = f1.__doc__
        v = D['verbose']
        re = D['regarding']
        def parent(P):
            cg("parent")
            return D[underscore_str+doc](P)

        if not P['now in calibration mode']:
            cb('\t',"Cannot enter because P['now in calibration mode'] == False")
            return False
        else:
            cb('\t',"Might be able to enter because P['now in calibration mode'] == True")
        
        result = parent(P)
        return result

	for f in [f1,f2,]:
		D[f.__doc__] = f
    cr('State')
    return D


#EOF
