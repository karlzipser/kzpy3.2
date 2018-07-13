

A = {
    'behavioral_mode':{
        'direct':   {'button':1,'min':20,'max':60,'led':1},
        'follow':   {'button':1,'min':0,'max':40,'led':2},
        'furtive':  {'button':1,'min':60,'max':80,'led':3},
        'play':     {'button':1,'min':80,'max':100,'led':4}
        },
    'agent':{
        'human':    {'button':2,'min':40,'max':100,'led':6*100},
        'network':  {'button':2,'min':0,'max':40,'led':7*100}
        },
    'place':{
        'local':    {'button':3,'min':40,'max':60,'led':8},
        'home':     {'button':3,'min':20,'max':40,'led':9},
        'Tilden':   {'button':3,'min':0,'max':20,'led':10},
        'campus':   {'button':3,'min':60,'max':80,'led':11},
        'arena':    {'button':3,'min':80,'max':100,'led':12},
        'other':    {'button':3,'min':80,'max':100,'led':13}
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
    print_timer = Timer(0.25)
    while P['ABORT'] == False:
        #print "_selector_run_loop"
        try:
            if 'Brief sleep to allow other threads to process...':
                time.sleep(0.0001)
            if RC['button_number'] == 4:
                #print 'a'
                if RC['button_time'] < 3.0:
                    #print 'b'
                    if P['servo_percent'] < 10:
                        #print 'c'
                        P['selector_mode'] = 'drive_mode'
                        spd2s("P['selector_mode'] = 'drive_mode'")
                        time.sleep(0.001)
                    elif P['servo_percent'] > 90:
                        #print 'd'
                        P['selector_mode'] = 'menu_mode'
                        spd2s("P['selector_mode'] = 'menu_mode'")
                        time.sleep(0.001)
            elif P['selector_mode'] == 'menu_mode':
                for theme in A.keys():
                    if P[theme] == False:
                        for kind in A[theme].keys():
                            if RC['button_number'] == A[theme][kind]['button']:
                                if P['servo_percent']>A[theme][kind]['min'] and P['servo_percent']<A[theme][kind]['max']:
                                    if P['motor_percent'] > 80:
                                        if print_timer.check():
                                            pd2s(kind,'selected')
                                            print_timer.reset()
                                        P[theme] = kind
                                    else:
                                        if print_timer.check():
                                            print(kind)
                                            print_timer.reset()
                    else:
                        a_kind = a_key(A[theme])
                        if RC['button_number'] == A[theme][a_kind]['button']:
                            if P['motor_percent'] < 20:
                                P[theme] = False
                if print_timer.check():
                    pprint(P)
                    print_timer.reset()
        except:
            pass        
    print 'end _calibrate_run_loop.'


