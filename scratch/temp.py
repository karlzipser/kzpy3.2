from kzpy3.utils3 import *
import WWWWWWWW


##############################################
#
CLASS_STRING = """
def XXXXXXXX():
    "XXXXXXXX"
    D = WWWWWWWW.WWWWWWWW()
    D['depth'] += 1
    dkeys = D.keys()
    for k in dkeys:
        D['_'+k] = D[k]
    underscore_str = ''
    for i in range(D['depth']):
        underscore_str += '_'
    D['type'] = XXXXXXXX.__doc__
    D['state'] = d2n("'",D['type'],"'")
    D['regarding'] = d2s("Regarding",D['state'])
    cb(D['regarding'],'depth =',D['depth'])
"""

FUNCTION_STRING = """
    def f########(P):
"""

FUNCTION_AUTO_UTILS_STRING = """
        doc = f1.__doc__
        v = D['verbose']
        re = D['regarding']
        def parent(P):
            cg("parent")
            return D[underscore_str+doc](P)
"""

PUT_FUNCTIONS_INTO_D_STRING = """
        for f in [f1,f2]:
            D[f.__doc__] = f
"""
#
##############################################





[< Class,Calibrate1,Calibrate0,

    [< def_Function(P):
        "Upon entry do this..."
        [< function_auto-utils
        result = parent(P)
        if result == False:
            return
        cb("""s = P['HUMAN_SMOOTHING_PARAMETER_1']""")
        return True

    [< def_Function(P):
        "Can this state can be entered?"
        [< function_auto-utils

        if not P['now in calibration mode']:
            cb('\t',"Cannot enter because P['now in calibration mode'] == False")
            return False
        else:
            cb('\t',"Might be able to enter because P['now in calibration mode'] == True")
        
        result = parent(P)
        return result

    [<put_functions_into_D

    return D



if __name__ == '__main__':
    clear_screen()
    P={}
    P['current state'] = 'none'
    P['now in calibration mode'] = True
    
    C = Calibrate1(0.9)
    C["Upon entry do this..."](P)
    C["Upon exit do this..."](P,'Calibrate_1')
    C["Can this state can be entered?"](P)
    C["Upon entry do this..."](P)
    C["Is it time to exit?"](P)
    C["Can this state can be entered?"](P)
    C["Upon exit do this..."](P,'random name')
    time.sleep(1)
    C["Upon exit do this..."](P,'random name')
    C["Upon exit do this..."](P,'Calibrate2')

    C["Is it time to exit?"](P)

    pprint(P)




for a in c:
    if len(a)>0:
        if a[0] == '<':
            print a





#EOF

#EOF