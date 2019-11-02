
from kzpy3.vis3 import *
import kzpy3.drafts.FSM2.fsm as fsm
import inspect

if 'These are the transitions functions':

    failure_probability = 0.1


    def locked_push(E):
        #name = inspect.stack()[0][3];print(name)
        if E['push']:
            #print(name)
            result = True
        else:
            result = False
        return result

    locked_push_fail = locked_push

    def locked_coin(E):
        #name = inspect.stack()[0][3];print(name)
        if E['coin']:
            result = True
        else:
            result = False
        return result

    locked_coin_fail = locked_coin

    def unlocked_push(E):
        #name = inspect.stack()[0][3];print(name)
        if E['push']:
            result = True
        else:
            result = False
        return result

    unlocked_push_fail = unlocked_push

    def unlocked_coin(E):
        #name = inspect.stack()[0][3];print(name)
        if E['coin']:
            result = True
        else:
            result = False
        return result

    unlocked_coin_fail = unlocked_coin





LOCKED = cf('locked','`wr')
UNLOCKED = cf('unlocked','`wg')

Network_layout = {
    LOCKED: [
        { 'function':'locked_push',       'destination':LOCKED,     'p':0.9 },
        { 'function':'locked_push_fail',  'destination':UNLOCKED,    'p':0.1 },
        { 'function':'locked_coin',       'destination':UNLOCKED,   'p':0.9 },
        { 'function':'locked_coin_fail',  'destination':LOCKED,     'p':0.1 },
    ],
    UNLOCKED: [
        { 'function':'unlocked_push', 'destination':LOCKED,  'p':.9},
        { 'function':'unlocked_push_fail', 'destination':UNLOCKED,  'p':.1},
        { 'function':'unlocked_coin', 'destination':UNLOCKED, 'p':.9},
        { 'function':'unlocked_coin_fail', 'destination':LOCKED, 'p':.1},
    ],
}



def Subway_environment():
    D = {}
    D['push'] = False
    D['coin'] = False
    def function_step():
        D['push'] = rndchoice([True,False])
        D['coin'] = not D['push']
        return {
            'push':D['push'],
            'coin':D['coin'],
        }
    D['step'] = function_step
    D['functions'] = {
        'locked_push':          locked_push,
        'locked_push_fail':     locked_push_fail,
        'locked_coin':          locked_coin,
        'locked_coin_fail':     locked_coin_fail,
        'unlocked_push':        unlocked_push,
        'unlocked_push_fail':   unlocked_push_fail,
        'unlocked_coin':        unlocked_coin,
        'unlocked_coin_fail':   unlocked_coin_fail,
    }
    return D



if __name__ == '__main__':

    N = fsm.Net(
        Network_layout=Network_layout,
        #Functions=Functions,
        start=UNLOCKED,
    )

    E = Subway_environment()

    prev_box = None
    current_box = 'unlocked'
    while True:
        
        R = N['evaluate'](Environment=E)
        #kprint(R)

        if E['coin']:
            input_ = 'coin'
        else:
            input_ = 'push'

        if R['function'] != None:
            if prev_box != None and prev_box != R['destination']:
                X = '`y'
                Y = '`g'
                if 'fail' in R['function']:
                    Z = '`wm' 
                else:
                    Z = '`--r'
                clp(prev_box,X,'--',Y,input_,'`','--',Y,R['function'],Z,'-->',Y,R['destination'],X)
                time.sleep(2)
        prev_box = R['destination']

        E['step']()

        


#EOF
