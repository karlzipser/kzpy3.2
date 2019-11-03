
from kzpy3.vis3 import *
import kzpy3.drafts.FSM.fsm as fsm


if 'These are the transitions functions':

    failure_probability = 0.1


    def locked_push(E):
        name = 'locked_push'
        if E['push']:
            result = True
        else:
            result = False
        return failure(name,result,failure_probability)

    def locked_coin(E):
        name = 'locked_coin'
        if E['coin']:
            result = True
        else:
            result = False
        return failure(name,result,failure_probability)

    def unlocked_push(E):
        name = 'unlocked_push'
        if E['push']:
            result = True
        else:
            result = False
        return failure(name,result,failure_probability)

    def unlocked_coin(E):
        name = 'unlocked_coin'
        if E['coin']:
            result = True
        else:
            result = False
        return failure(name,result,failure_probability)


    def failure(name,result,prob):
        if rnd() < prob:
            clp('Oops!','`r-b',name,'`--u','failed!')
            return not result
        else:
            return result


Network_layout = {
    'locked': [
        { 'function':locked_push, 'destination':'locked' },
        { 'function':locked_coin, 'destination':'unlocked' },
    ],
    'unlocked': [
        { 'function':unlocked_push, 'destination':'locked' },
        { 'function':unlocked_coin, 'destination':'unlocked' },
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
    return D



if __name__ == '__main__':

    N = fsm.Net(
        Network_layout=Network_layout,
        start='unlocked',
    )

    E = Subway_environment()

    prev_box = None
    current_box = 'unlocked'
    while True:
        
        current_box = N['evaluate'](Environment=E)

        if E['coin']:
            action = 'coin'
        else:
            action = 'push'

        """
        kprint(
            item=E,
            title=current_box,
            ignore_keys=['motor_prev',],
            ignore_types=function_types,
        )
        """
        if prev_box != None:
            clp(prev_box,'--',action,'-->',current_box)
        prev_box = current_box

        E['step']()

        time.sleep(.5)


#EOF
