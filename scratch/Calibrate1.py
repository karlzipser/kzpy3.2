from kzpy3.utils3 import *
import State

def Calibrate1(entry_timer_time):
    "Calibrate1"
    D = State.State(entry_timer_time)
    dkeys = D.keys()
    for k in dkeys:
        if k[0] != '_':
            D['_'+k] = D[k]
    D['impossible source states'] = ['Calibrate0','Calibrate1']
    D['possible destination states'] = ['Calibrate2']
    D['type'] = Calibrate1.__doc__
    D['state'] = d2n("'",D['type'],"'")
    D['regarding'] = d2s("Regarding",D['state'])

    def f1(P):
        "Upon entry do this..."
        doc = f1.__doc__; v = D['verbose']; re = D['regarding']
        cr(0)
        result = D['_'+doc](P)
        cr(1)
        if result == False:
            return
        if v:cb("""
            s = P['HUMAN_SMOOTHING_PARAMETER_1']
            P['servo_pwm_null'] = (1.0-s)*P['servo_pwm'] + s*P['servo_pwm_null']
            P['motor_pwm_null'] = (1.0-s)*P['motor_pwm'] + s*P['motor_pwm_null']
            P['servo_pwm_min'] = P['servo_pwm_null']
            P['servo_pwm_max'] = P['servo_pwm_null']
            P['motor_pwm_min'] = P['motor_pwm_null']
            P['motor_pwm_max'] = P['motor_pwm_null']
            P['servo_pwm_smooth'] = P['servo_pwm_null']
            P['motor_pwm_smooth'] = P['motor_pwm_null']""")
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
        result = D['_'+doc](P)
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









#EOF