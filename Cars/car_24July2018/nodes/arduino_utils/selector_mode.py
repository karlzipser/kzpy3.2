from kzpy3.utils2 import *
exec(identify_file_str)

"""
[orientation][blink][color][_,symbol]
"""

A = {
    'behavioral_mode_choice':{
        'direct':   {'button':2,'min':40,'max':60,'led':1},
        'follow':   {'button':2,'min':0,'max':40,'led':2},
        'furtive':  {'button':2,'min':60,'max':80,'led':3},
        'play':     {'button':2,'min':80,'max':100,'led':4}
        },
    'agent_choice':{
        'human':    {'button':3,'min':40,'max':100,'led':17},
        'network':  {'button':3,'min':0,'max':40,'led':18}
        },
    'place_choice':{
        'local':    {'button':1,'min':40,'max':60,'led':8},
        'home':     {'button':1,'min':20,'max':40,'led':9},
        'Tilden':   {'button':1,'min':0,'max':20,'led':10},
        'campus':   {'button':1,'min':60,'max':80,'led':11},
        'arena':    {'button':1,'min':80,'max':90,'led':12},
        'other':    {'button':1,'min':90,'max':100,'led':13}
        }   
    }

def Selector_Mode(P):
    for theme in A.keys():
        P[theme] = False

    P['behavioral_mode_choice'] = 'direct'
    P['agent_choice'] = 'human'
    P['place_choice'] = 'local'
    P['selector_mode'] = 'menu_mode'
    P['LED_number']['current'] = 11315
    threading.Thread(target=_selector_run_loop,args=[P]).start()

def _selector_run_loop(P):
    CS_("_selector_run_loop","selector_mode.py")
    print_timer = Timer(0.1)
    frequency_timer = Timer(1)
    while P['ABORT'] == False:
        frequency_timer.freq(name='_selector_run_loop',do_print=P['print_selector_freq'])
        #print_timer.message(d2s(P['behavioral_mode_choice']))
        if 'Brief sleep to allow other threads to process...':
            time.sleep(0.1)
        if not P['calibrated']:#################################################
            if P['button_number'] == 4:
                if P['button_time'] < P['CALIBRATION_NULL_START_TIME']:
                    P['LED_number']['current'] = 11316
                elif P['button_time'] >= P['CALIBRATION_NULL_START_TIME']:
                    if P['button_time'] < P['CALIBRATION_START_TIME']:
                        P['LED_number']['current'] = 11105
                    else:
                        P['LED_number']['current'] = 11305
            elif P['button_number'] != 4:
                P['LED_number']['current'] = 11315
        elif P['calibrated']:####################################################
            if P['button_number'] == 4:
                if P['button_time'] < P['CALIBRATION_START_TIME']:
                    if P['human']['motor_percent'] < 10:
                        spd2s("P['human']['motor_percent'] < 10, ABORTING, SHUTTING DOWN!!!!!")
                        P['ABORT'] = True
                        time.sleep(0.01)
                        unix('sudo shutdown -h now')
                    elif P['human']['servo_percent'] < 10:
                        P['selector_mode'] = 'drive_mode'
                    elif P['human']['servo_percent'] > 90:
                        P['selector_mode'] = 'menu_mode'
                    if P['selector_mode'] == 'drive_mode':
                        P['LED_number']['current'] = 11306
                    elif P['selector_mode'] == 'menu_mode':
                        P['LED_number']['current'] = 11307
                elif P['button_time'] >= P['CALIBRATION_START_TIME']:
                    P['LED_number']['current'] = 11305
            elif P['button_number'] != 4:
                if P['selector_mode'] == 'menu_mode':
                    for theme in A.keys():
                        if P[theme] == False:
                            #print_timer.message(d2s(P['human']['motor_percent']))
                            for kind in A[theme].keys():
                                if P['button_number'] == A[theme][kind]['button']:
                                    if P['human']['servo_percent']>A[theme][kind]['min'] and P['human']['servo_percent']<A[theme][kind]['max']:
                                        if P['human']['motor_percent'] > 80:
                                            P[theme] = kind
                                        else:
                                            if P['agent_choice'] == False:
                                                agent_choice = 'human'
                                            else:
                                                agent_choice = P['agent_choice']
                                            if agent_choice == 'human':
                                                color = 100
                                            elif agent_choice == 'network':
                                                color = 200
                                            P['LED_number']['current'] = 11000+color+A[theme][kind]['led']
                        elif P[theme] != False:
                            kind = P[theme]
                            if P['button_number'] == A[theme][kind]['button']:
                                if P['human']['motor_percent'] < 20:
                                    P[theme] = False
                                else:
                                    if P['agent_choice'] == False:
                                        agent_choice = 'human'
                                    else:
                                        agent_choice = P['agent_choice']
                                if agent_choice == 'human':
                                    color = 100
                                elif agent_choice == 'network':
                                    color = 200
                                P['LED_number']['current'] = 10000+color+A[theme][kind]['led']
                elif P['selector_mode'] == 'drive_mode':
                    if P['button_number'] != 4:
                        all_themes_set = True
                        for theme in A.keys():
                            if P[theme] == False:
                                P['LED_number']['current'] = 11315
                                all_themes_set = False
                        if all_themes_set:
                            agent_choice = P['agent_choice']
                            if agent_choice == 'human':
                                color = 100
                            elif agent_choice == 'network':
                                color = 200
                            if P['button_number'] == 3:
                                orientation = 30000
                            elif P['button_number'] == 2:
                                orientation = 10000
                            elif P['button_number'] == 1:
                                orientation = 20000
                            P['LED_number']['current'] = orientation+color+A['behavioral_mode_choice'][P['behavioral_mode_choice']]['led']


