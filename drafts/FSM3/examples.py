from kzpy3.utils3 import *

def Subway():

    D = {}
    def locked_push(E):
        if E['push']:
            result = True
        else:
            result = False
        return result

    locked_push_fail = locked_push

    def locked_coin(E):
        if E['coin']:
            result = True
        else:
            result = False
        return result

    locked_coin_fail = locked_coin

    def unlocked_push(E):
        if E['push']:
            result = True
        else:
            result = False
        return result

    unlocked_push_fail = unlocked_push

    def unlocked_coin(E):
        if E['coin']:
            result = True
        else:
            result = False
        return result

    unlocked_coin_fail = unlocked_coin

    LOCKED = cf('locked','`wr')
    UNLOCKED = cf('unlocked','`wg')

    D['start'] = UNLOCKED

    D['Network_layout'] = {
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

    def function_Subway_environment():
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

    D['Environment'] = function_Subway_environment
    
    return D



#EOF
