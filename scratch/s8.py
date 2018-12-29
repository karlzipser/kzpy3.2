
P={}
P['current state'] = 'none'
P['now in calibration mode'] = True


def Calibrate_0():
    "Calibrate_0"
    D = {}
    D['not possible source states'] = ['Calibrate_0','Calibrate_1','Calibrate_2']
    D['possible destination states'] = ['Calibrate_1']
    D['type'] = 'Calibrate_0'
    D['Since-entry timer:'] = Timer(0.1)

    def function_upon_entry(P):

        "Upon entry do this..."

        P['current state'] = D['type']
        cb('\tEntering state',D['type']+'.')
        D['Since-entry timer:'].reset()
        cb('\tUpon entry:')
        cr("\t\tSay 'hi!'")

    def function_can_enter(P):

        "Can this state can be entered?"

        cy('Regarding',D['type']+', can this state can be entered?')
        if D['type'] == P['current state']:
            cb('\tAlready in state',D['type']+', cannot reenter now.')
            return False
        if P['now in calibration mode']:
            if P['current state'] not in D['not possible source states']:
                cb('\tState',D['type'],'can be entered.')
                return True
        cb('\tThis state cannot be entered now.')
        return False

    def function_time_to_exit(P):

        "Is it time to exit?"

        cy('Regarding',D['type']+', is it time to exit?')
        if D['type'] != P['current state']:
            cb('\tNot in state',D['type']+", so can't exit.")
            return False
        print D['Since-entry timer:'].check(),D['Since-entry timer:'].time()
        if D['Since-entry timer:'].check():
            cb('\tIt is time to exit.')
            return True
        cb('\tIt is not time to exit.')
        return False

    def function_upon_exit(P,dst_state):

        "Upon exit do this..."

        cy('Regarding',D['type']+', upon exit try to do this...')

        if dst_state not in D['possible destination states']:
            cb("\t'"+dst_state+"'is not a suitable destination for",D['type']+'.')
            return
        if D['Is it time to exit?'](P):
            cb('\tLeaving state',D['type'],'for',dst_state+'.')
            P['current state'] = dst_state
            return
        cb('\tNot exiting yet.')


    for f in [
        function_time_to_exit,
        function_can_enter,
        function_upon_entry,
        function_upon_exit, ]:
        D[f.__doc__] = f

    return D


C = Calibrate_0()
C['Upon exit do this...'](P,'Calibrate_1')
C['Can this state can be entered?'](P)
C['Upon entry do this...'](P)
C['Is it time to exit?'](P)
C['Can this state can be entered?'](P)
C['Upon exit do this...'](P,'random name')
time.sleep(1)
C['Upon exit do this...'](P,'random name')
C['Upon exit do this...'](P,'Calibrate_1')

C['Is it time to exit?'](P)

