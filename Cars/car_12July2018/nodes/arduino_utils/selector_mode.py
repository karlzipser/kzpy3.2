from kzpy3.utils2 import *
import threading

"""
[orientation][blink][color][_,symbol]
"""

A = {
    'behavioral_mode_choice':{
        'direct':   {'button':1,'min':20,'max':60,'led':1},
        'follow':   {'button':1,'min':0,'max':40,'led':2},
        'furtive':  {'button':1,'min':60,'max':80,'led':3},
        'play':     {'button':1,'min':80,'max':100,'led':4}
        },
    'agent_choice':{
        'human':    {'button':2,'min':40,'max':100,'led':17},
        'network':  {'button':2,'min':0,'max':40,'led':18}
        },
    'place_choice':{
        'local':    {'button':3,'min':40,'max':60,'led':8},
        'home':     {'button':3,'min':20,'max':40,'led':9},
        'Tilden':   {'button':3,'min':0,'max':20,'led':10},
        'campus':   {'button':3,'min':60,'max':80,'led':11},
        'arena':    {'button':3,'min':80,'max':90,'led':12},
        'other':    {'button':3,'min':90,'max':100,'led':13}
        }   
    }

def Selector_Mode(RC,P):
    D = {}
    for theme in A.keys():
        P[theme] = False
    P['selector_mode'] = 'menu_mode'
    P['LED_number']['current'] = 11315
    threading.Thread(target=_selector_run_loop,args=[D,RC,P]).start()
    return D

def _selector_run_loop(D,RC,P):
    print "_selector_run_loop"
    print_timer = Timer(0.1)
    frequency_timer = Timer(1)
    while P['ABORT'] == False:
        frequency_timer.freq(name='_selector_run_loop',do_print=P['print_selector_freq'])
        if 'Brief sleep to allow other threads to process...':
            time.sleep(0.1)
        if not P['calibrated']:#################################################
            if RC['button_number'] == 4:
                if RC['button_time'] < P['CALIBRATION_NULL_START_TIME']:
                    P['LED_number']['current'] = 11316
                elif RC['button_time'] >= P['CALIBRATION_NULL_START_TIME']:
                    if RC['button_time'] < P['CALIBRATION_START_TIME']:
                        P['LED_number']['current'] = 11105
                    else:
                        P['LED_number']['current'] = 11305
            elif RC['button_number'] != 4:
                P['LED_number']['current'] = 11315
        elif P['calibrated']:####################################################
            if RC['button_number'] == 4:
                if RC['button_time'] < P['CALIBRATION_START_TIME']:
                    if P['servo_percent'] < 10:
                        P['selector_mode'] = 'drive_mode'
                    elif P['servo_percent'] > 90:
                        P['selector_mode'] = 'menu_mode'
                    if P['selector_mode'] == 'drive_mode':
                        P['LED_number']['current'] = 11306
                    elif P['selector_mode'] == 'menu_mode':
                        P['LED_number']['current'] = 11307
                elif RC['button_time'] >= P['CALIBRATION_START_TIME']:
                    P['LED_number']['current'] = 11305
            elif RC['button_number'] != 4:
                if P['selector_mode'] == 'menu_mode':
                    for theme in A.keys():
                        if P[theme] == False:
                            for kind in A[theme].keys():
                                if RC['button_number'] == A[theme][kind]['button']:
                                    if P['servo_percent']>A[theme][kind]['min'] and P['servo_percent']<A[theme][kind]['max']:
                                        if P['motor_percent'] > 80:
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
                            if RC['button_number'] == A[theme][kind]['button']:
                                if P['motor_percent'] < 20:
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
                    if RC['button_number'] != 4:
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
                            if RC['button_number'] == 1:
                                orientation = 30000
                            elif RC['button_number'] == 3:
                                orientation = 10000
                            elif RC['button_number'] == 2:
                                orientation = 20000
                            P['LED_number']['current'] = orientation+color+A['behavioral_mode_choice'][P['behavioral_mode_choice']]['led']


