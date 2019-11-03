
from kzpy3.vis3 import *
import kzpy3.drafts.Markov_4.markov as markov


if 'These are the transitions functions':

    def still_to_slow_forward(E):
        if E['encoder'] > 0.2 and E['motor'] > 51:
            return True
        else:
            return False

    def still_to_slow_backward(E):
        if E['encoder'] > 0.2 and E['motor'] < 47:
            return True
        else:
            return False

    def slow_forward_to_still(E):
        if E['encoder'] < 0.2 and E['motor'] > 49:
            return True
        else:
            return False

    def slow_backward_to_still(E):
        if E['encoder'] < 0.2 and E['motor'] <= 49:
            return True
        else:
            return False





Network_layout = {
    'still': [
        { 'function':still_to_slow_forward, 'destination':'slow_forward' },
        { 'function':still_to_slow_backward, 'destination':'slow_backward' },
    ],
    'slow_forward': [
        { 'function':slow_forward_to_still, 'destination':'still' },
    ],
    'slow_backward': [
        { 'function':slow_backward_to_still, 'destination':'still' },
    ],
}



def Driving_environment():
    D = {}
    D['encoder'] = 0
    D['motor'] = 49
    s = 0.9
    def function_step():
        D['motor_prev'] = D['motor']
        D['motor'] = D['motor'] + 10.*rndn()
        D['motor'] = (1-s)*D['motor'] + s*D['motor_prev']
        D['encoder'] = 0.*rndn() + np.abs(D['motor']-49)/3.
        D['motor'] = dp(bound_value(D['motor'],0,99))
        D['encoder'] = dp(bound_value(D['encoder'],0,20))
        return {
            'encoder':D['encoder'],
            'motor':D['motor'],
        }
    D['step'] = function_step
    return D



if __name__ == '__main__':

    N = markov.Net(
        Network_layout=Network_layout,
        start='still',
    )

    E = Driving_environment()

    function_types = [type(sorted),type(opj)]

    while True:
        current_box = N['evaluate'](Environment=E)
        kprint(
            item=E,
            title=current_box,
            ignore_keys=['motor_prev',],
            ignore_types=function_types,
        )
        E['step']()
        time.sleep(.5)


#EOF
