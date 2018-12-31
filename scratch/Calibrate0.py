from kzpy3.utils3 import *
import State



def Calibrate0(entry_timer_time):
    "Calibrate0"
    D = State.State(entry_timer_time)
    cr(D['depth'])
    D['depth'] += 1
    cr(D['depth'])
    dkeys = D.keys()
    for k in dkeys:
        D['_'+k] = D[k]
        print "Calibrate0",'_'+k
    underscore_str = ''
    for i in range(D['depth']):
        underscore_str += '_'

    D['type'] = Calibrate0.__doc__
    D['state'] = d2n("'",D['type'],"'")
    D['regarding'] = d2s("Regarding",D['state'])
    cb(D['regarding'],'depth =',D['depth'])

       
    D['impossible source states'] = ['Calibrate0','Calibrate2']
    D['possible destination states'] = ['Calibrate1']

    def f1(P):
        "Upon entry do this..."
        doc = f1.__doc__; v = D['verbose']; re = D['regarding']

        result = D[underscore_str+doc](P)

        
        if result == False:
            return
        if v:cb("""
            P['Arduinos']['SOUND'].write(P['sound/calibrate tune'])
            P['calibrated'] = False
            P['servo_pwm_null'] = P['servo_pwm']
            P['motor_pwm_null'] = P['motor_pwm']""")
        return True

    def f2(P):
        "Can this state can be entered?"
        doc = f2.__doc__; v = D['verbose']; re = D['regarding']
        if v:cy(re,doc)
        cr('Calibrate0')
        if not P['now in calibration mode']:
            if v:cb('\t',"Cannot enter because P['now in calibration mode'] == False")
            return False
        else:
            if v:cb('\t',"Might be able to enter because P['now in calibration mode'] == True")
        result = D[underscore_str+doc](P)
        return result

    try:
        for f in [f1,f2]:
            D[f.__doc__] = f
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        CS_('Exception!',emphasis=True)
        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)

    return D




if __name__ == '__main__':
    clear_screen()
    P={}
    P['current state'] = 'none'
    P['now in calibration mode'] = True
    
    C = Calibrate0(0.1)
    C["Upon entry do this..."](P)
    C["Upon exit do this..."](P,'Calibrate_1')
    C["Can this state can be entered?"](P)
    C["Upon entry do this..."](P)
    C["Is it time to exit?"](P)
    C["Can this state can be entered?"](P)
    C["Upon exit do this..."](P,'random name')
    time.sleep(1)
    C["Upon exit do this..."](P,'random name')
    C["Upon exit do this..."](P,'Calibrate1')

    C["Is it time to exit?"](P)

    pprint(P)









#EOF