from kzpy3.utils3 import *

def State(entry_timer_time):
    "State"
    D = {}
    D['depth'] = 0
    D['verbose'] = True
    D['impossible source states'] = []
    D['possible source states'] = []
    D['impossible destination states'] = []
    D['possible destination states'] = []
    D['type'] = State.__doc__
    D['entry timer'] = Timer(entry_timer_time)
    D['state'] = d2n("'",D['type'],"'")
    D['regarding'] = d2s("Regarding",D['state'])
    cb(D['regarding'],'depth =',D['depth'])
    

    def f1(P):
        "Upon entry do this..."
        doc = f1.__doc__; v = D['verbose']; re = D['regarding']
        
        
        if not D["Can this state can be entered?"](P):
            if v:cr('\t',False)
            return False
        P['current state'] = D['type']
        D['entry timer'].reset()
        if v:
            cy(re,doc)
            cb('\tEntering state',D['state']+'.')
            cb('\tUpon entry:')
        if v:cg('\t',True)
        return True

    def f2(P):
        "Can this state can be entered?"
        cr('State')
        doc = f2.__doc__; v = D['verbose']; re = D['regarding']
        
        if v:cy(re,doc)
        if D['type'] == P['current state']:
            if v:cb('\tAlready in',D['state']+', cannot reenter now.')
            if v:cr('\t',False)
            return False
 
        if P['current state'] not in D['impossible source states']:
            if P['current state'] in D['possible source states'] or len(D['possible source states']) == 0:
                if v:cb('\t',D['state'],'can be entered.')
                if v:cg('\t',True)
                return True

        cb('\tThis state cannot be entered now.')
        if v:cr('\t',False)
        return False

    def f3(P):
        "Is it time to exit?"
        doc = f3.__doc__; v = D['verbose']; re = D['regarding']
        if v:cy(re,doc)
        if D['type'] != P['current state']:
            if v:cb('\tNot in state',D['type']+", so can't exit.")
            if v:cr('\t',False)
            return False
        if v:print D['entry timer'].check(),D['entry timer'].time()
        if D['entry timer'].check():
            if v:cb('\tIt is time to exit.')
            if v:cg('\t',True)
            return True
        if v:cb('\tIt is not time to exit.')
        if v:cr('\t',False)
        return False

    def f4(P,dst_state):
        "Upon exit do this..."
        doc = f4.__doc__; v = D['verbose']; re = D['regarding']
        if v:cy(re,doc)
        if D['type'] != P['current state']:
            if v:cb('\tNot in state',D['state']+", so can't exit.")
            if v:cr('\t',False)
            return False
        if dst_state not in D['possible destination states']:
            if v:cb("\t'"+dst_state+"' is not a suitable destination for",D['state']+'.')
            if v:cr('\t',False)
            return False
        if D['Is it time to exit?'](P):
            if v:cb('\tLeaving state',D['state'],"for '"+dst_state+"'.")
            P['current state'] = dst_state
            if v:cg('\t',True)
            return True
        if v:cb('\tNot exiting yet.')
        if v:cr('\t',False)
        return False


    for f in [f1,f2,f3,f4]:
        D[f.__doc__] = f

    return D

if __name__ == '__main__':
    clear_screen()
    P={}
    P['current state'] = 'none'
    #P['now in calibration mode'] = True
    
    C = State(0.5)
    C["Upon entry do this..."](P)
    C["Upon exit do this..."](P,'Calibrate_1')
    C["Can this state can be entered?"](P)
    C["Upon entry do this..."](P)
    C["Is it time to exit?"](P)
    C["Can this state can be entered?"](P)
    C["Upon exit do this..."](P,'random name')
    time.sleep(1)
    C["Upon exit do this..."](P,'random name')
    C["Upon exit do this..."](P,'Calibrate_1')

    C["Is it time to exit?"](P)

    pprint(P)









#EOF