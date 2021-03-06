from kzpy3.vis3 import *
import kzpy3.drafts.FSM2.fsm as fsm
import kzpy3.Menu.main



Q = kzpy3.Menu.main.start_Dic(
    dic_project_path=opjk('drafts','FSM2'), 
    Arguments={
        'menu':False,
        'read_only':True,
    }
)
P = Q['Q']










if 'These are the transitions functions':

    failure_probability = 0.1


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


if 'This is the subway network layout':
    LOCKED = cf('locked','`wr')
    UNLOCKED = cf('unlocked','`wg')

    Subway_network_layout = {
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



if 'This is the subway network layout 2':
    LOCKED = cf('locked','`wr')
    UNLOCKED = cf('unlocked','`wg')

    Subway_network_layout2 = {
        LOCKED: [
            { 'function':'locked_push',       'destination':LOCKED,     'p':0.1 },
            { 'function':'locked_push_fail',  'destination':UNLOCKED,    'p':0.9 },
            { 'function':'locked_coin',       'destination':UNLOCKED,   'p':0.1 },
            { 'function':'locked_coin_fail',  'destination':LOCKED,     'p':0.9 },
        ],
        UNLOCKED: [
            { 'function':'unlocked_push', 'destination':LOCKED,  'p':.1},
            { 'function':'unlocked_push_fail', 'destination':UNLOCKED,  'p':.9},
            { 'function':'unlocked_coin', 'destination':UNLOCKED, 'p':.1},
            { 'function':'unlocked_coin_fail', 'destination':LOCKED, 'p':.9},
        ],
    }



if 'This is the subway envrionment':
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
        Network_layout=Subway_network_layout2,
        start=UNLOCKED,
    )
    E = Subway_environment()

    prev_box = None 

    while True:
        if 'Menu data processing':
            if Q['load']():
                pass

            if P['aBORT']:
                clp('aBORT ==',True)
                break

            if P['pAUSE']:
                clp('pAUSE ==',True)
                time.sleep(P['pause_sleep_time'])
                continue

            if P['cLEAR']:
                clp('cLEAR ==',True)
                clear_screen()

        R = N['evaluate'](Environment=E)

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
                time.sleep(P['sleep_time'])

        prev_box = R['destination']

        E['step']()

        


#EOF
