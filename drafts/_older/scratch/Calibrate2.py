from kzpy3.utils3 import *
import State

def Calibrate2(entry_timer_time):
    "Calibrate2"
    D = State.State(entry_timer_time)
    dkeys = D.keys()
    for k in dkeys:
        if k[0] != '_':
            D['_'+k] = D[k]
    D['impossible source states'] = ['Calibrate0','Calibrate2']
    D['possible destination states'] = ['random name']
    D['type'] = Calibrate2.__doc__
    D['state'] = d2n("'",D['type'],"'")
    D['regarding'] = d2s("Regarding",D['state'])

    def f1(P):
        "Upon entry do this..."
        doc = f1.__doc__; v = D['verbose']; re = D['regarding']
        
        result = D['_'+doc](P)
        
        if result == False:
            return
        if v:cb("""
            start.message('Calibrate now.')
            if P['servo_pwm_max'] < P['servo_pwm']:
                P['servo_pwm_max'] = P['servo_pwm']
            if P['servo_pwm_min'] > P['servo_pwm']:
                P['servo_pwm_min'] = P['servo_pwm']
            if P['motor_pwm_max'] < P['motor_pwm']:
                P['motor_pwm_max'] = P['motor_pwm']
            if P['motor_pwm_min'] > P['motor_pwm']:
                P['motor_pwm_min'] = P['motor_pwm']
            if P['servo_pwm_max'] - P['servo_pwm_min'] > 300:
                if P['motor_pwm_max'] - P['motor_pwm_min'] > 300:
                    P['calibrated'] = True""")
        return True


    def f2(P):
        "Can this state can be entered?"
        print '!!!!!!!!!!!!!!!2'
        doc = f2.__doc__; v = D['verbose']; re = D['regarding']
        if v:cy(re,doc)
        cr('Calibrate0')
        if not P['now in calibration mode']:
            if v:cb('\t',"Cannot enter because P['now in calibration mode'] == False")
            return False
        else:
            if v:cb('\t',"Might be able to enter because P['now in calibration mode'] == True")
        result = D['_'+doc](P)
        return result


    def f3(P):
        "Is it time to exit?"
        print '!!!!!!!!!!!!!!!3'
        doc = f3.__doc__; v = D['verbose']; re = D['regarding']
        if v:cy(re,doc) 
        result = D['_'+doc](P)
        if result == False:
            return False
        if P['now in calibration mode']:
            if v:cb('\t',"Cannot exit because P['now in calibration mode'] == True")
        else:
            if v:cb('\t',"Can exit because P['now in calibration mode'] == False")
        return not P['now in calibration mode']

    
    try:
        for f in [f1,f2,f3]:
            D[f.__doc__] = f
            print f
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
    
    C = Calibrate2(1)
    C["Upon entry do this..."](P)
    C["Upon exit do this..."](P,'Calibrate1')
    C["Can this state can be entered?"](P)
    C["Upon entry do this..."](P)
    C["Is it time to exit?"](P)
    C["Can this state can be entered?"](P)
    C["Upon exit do this..."](P,'random name')
    time.sleep(1)
    C["Upon exit do this..."](P,'random name')
    time.sleep(1)
    P['now in calibration mode'] = False
    C["Upon exit do this..."](P,'random name')
    

    C["Upon exit do this..."](P,'none')

    C["Is it time to exit?"](P)

    pprint(P)









#EOF