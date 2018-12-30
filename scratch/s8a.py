
P={}
P['current state'] = 'none'
P['now in calibration mode'] = True


def State(entry_timer_time):
    "State"
    D = {}
    D['verbose'] = True
    D['impossible source states'] = []
    D['possible source states'] = []
    D['impossible destination states'] = []
    D['possible destination states'] = []
    D['type'] = State.__doc__
    D['entry timer'] = Timer(entry_timer_time)
    D['state'] = d2n("'",D['type'],"'")
    D['regarding'] = d2s("Regarding",D['state'])
    

    def f1(P):
        "Upon entry do this..."
        doc = f1.__doc__; v = D['verbose']; re = D['regarding']
        P['current state'] = D['type']
        D['entry timer'].reset()
        if v:
            cb(doc)
            cb('\tEntering state',D['type']+'.')
            cb('\tUpon entry:')
        pass

    def f2(P):
        "Can this state can be entered?"
        doc = f2.__doc__; v = D['verbose']; re = D['regarding']
        _
        if v:cy(re)
        if D['type'] == P['current state']:
            if v:cb('\tAlready in',D['state']+', cannot reenter now.')
            return False
        if P['now in calibration mode']:
            if P['current state'] not in D['impossible source states']:
                if v:cb(D['state'],'can be entered.')
                return True
        cb('\tThis state cannot be entered now.')
        return False

    def f3(P):
        "Is it time to exit?"
        doc = f3.__doc__; v = D['verbose']; re = D['regarding']
        if v:cy(re,'is it time to exit?')
        if D['type'] != P['current state']:
            if v:cb('\tNot in state',D['type']+", so can't exit.")
            return False
        if v:print D['entry timer'].check(),D['entry timer'].time()
        if D['entry timer'].check():
            if v:cb('\tIt is time to exit.')
            return True
        if v:cb('\tIt is not time to exit.')
        return False

    def f4(P,dst_state):
        "Upon exit do this..."
        doc = f4.__doc__; v = D['verbose']; re = D['regarding']
        if v:cy( 'upon exit try to do this...')

        if dst_state not in D['possible destination states']:
            if v:cb("\t'"+dst_state+"' is not a suitable destination for",D['state']+'.')
            return
        if D['Is it time to exit?'](P):
            if v:cb('\tLeaving state',D['type'],'for',dst_state+'.')
            P['current state'] = dst_state
            return
        if v:cb('\tNot exiting yet.')


    for f in [f1,f2,f3,f4]:
        D[f.__doc__] = f

    return D


C = State(2)
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











#EOF