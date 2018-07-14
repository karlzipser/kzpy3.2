from kzpy3.utils2 import *
import threading

BUTTON_4 = 2
STRAIGHT = 1
LEFT = 2
RIGHT = 3
SELECTED = 1
NOT_SELECTED = 2


DIRECT = 1
FOLLOW = 2
FURTIVE = 3
PLAY = 4

CALIBRATE = 5
DRIVE_MODE = 15
SELECT_MODE = 16


HUMAN = 6
NETWORK = 7

LOCAL = 8
HOME = 9
TILDEN = 10
CAMPUS = 11
ARENA = 12
OTHER = 13

AGENT = 14

A = {
    'behavioral_mode_choice':{
        'direct':   {'button':1,'min':20,'max':60,'led':DIRECT},
        'follow':   {'button':1,'min':0,'max':40,'led':FOLLOW},
        'furtive':  {'button':1,'min':60,'max':80,'led':FURTIVE},
        'play':     {'button':1,'min':80,'max':100,'led':PLAY}
        },
    'agent_choice':{
        'human':    {'button':2,'min':40,'max':100,'led':HUMAN},
        'network':  {'button':2,'min':0,'max':40,'led':NETWORK}
        },
    'place_choice':{
        'local':    {'button':3,'min':40,'max':60,'led':LOCAL},
        'home':     {'button':3,'min':20,'max':40,'led':HOME},
        'Tilden':   {'button':3,'min':0,'max':20,'led':TILDEN},
        'campus':   {'button':3,'min':60,'max':80,'led':CAMPUS},
        'arena':    {'button':3,'min':80,'max':90,'led':ARENA},
        'other':    {'button':3,'min':90,'max':100,'led':OTHER}
        }   
    }

def Selector_Mode(RC,P):
    D = {}
    for theme in A.keys():
        P[theme] = False
    threading.Thread(target=_selector_run_loop,args=[D,RC,P]).start()
    return D

def _selector_run_loop(D,RC,P):
    print "_selector_run_loop"
    print_timer = Timer(0.1)
    while P['ABORT'] == False:
        if True:#try:
            if 'Brief sleep to allow other threads to process...':
                time.sleep(0.01)
            P['LED_number']['previous'] = P['LED_number']['current']
            if RC['button_number'] == 4:
                if RC['button_time'] < 3.0:
                    if P['servo_percent'] < 10:
                        P['selector_mode'] = 'drive_mode'
                        time.sleep(0.001)
                    elif P['servo_percent'] > 90:
                        P['selector_mode'] = 'menu_mode'
                        time.sleep(0.001)
            elif P['selector_mode'] == 'menu_mode':
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
                                        if theme == 'place_choice' or theme == 'behavioral_mode_choice':
                                            P['LED_number']['current'] = 10000*NOT_SELECTED+100*A['agent_choice'][agent_choice]['led']+A[theme][kind]['led']
                                        elif theme == 'agent_choice':
                                            P['LED_number']['current'] = 10000*NOT_SELECTED+100*A['agent_choice'][kind]['led']+AGENT       
                    else:
                        kind = P[theme]
                        if RC['button_number'] == A[theme][kind]['button']:
                            if P['motor_percent'] < 20:
                                P[theme] = False
                            else:
                                if P['agent_choice'] == False:
                                    agent_choice = 'human'
                                else:
                                    agent_choice = P['agent_choice']
                                if theme == 'place_choice' or theme == 'behavioral_mode_choice':
                                    P['LED_number']['current'] = 10000*SELECTED+100*A['agent_choice'][agent_choice]['led']+A[theme][kind]['led']
                                elif theme == 'agent_choice':
                                    P['LED_number']['current'] = 10000*SELECTED+100*A['agent_choice'][kind]['led']+AGENT
            elif P['selector_mode'] == 'drive_mode':
                pass
            if print_timer.check():
                print(P['LED_number']['current'])
                print_timer.reset()
        else:#except Exception as e:
            print("********** _selector_run_loop Exception ***********************")
            print(e.message, e.args)       
    print 'end _selector_run_loop.'

