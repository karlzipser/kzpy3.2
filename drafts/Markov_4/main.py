
from kzpy3.vis3 import *
import kzpy3.drafts.Markov_4.markov as markov


def fun1(E):
    if rndn() > 0:
        return True
    else:
        return False
def fun2(E):
    return True
def fun3(E):
    return True
def fun4(E):
    return True



Network_layout = {
    'still': [
        { 'function':fun1, 'destination':'slow_forward' },
        { 'function':fun1, 'destination':'slow_backward' },
    ],
    'slow_forward': [
        { 'function':fun1, 'destination':'fast_forward' },
        { 'function':fun1, 'destination':'still' },
    ],
    'slow_backward': [
        { 'function':fun1, 'destination':'fast_backward' },
        { 'function':fun1, 'destination':'still' },
    ],
    'fast_forward': [
        { 'function':fun1, 'destination':'slow_forward' },
    ],
    'fast_backward': [
        { 'function':fun1, 'destination':'slow_backward' },
    ],
}

Driving_direction_model = markov.Net(
    Network_layout,
    'still',
)

while True:

    print Driving_direction_model['evaluate'](E)
    time.sleep(1)
"""
def Environment():
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

E = Environment()

timer = Timer(5)

if __name__ == '__main__':

    States = {still:[],slow_fwd:[],fast_fwd:[],slow_bkw:[],fast_bkw:[]}

    while True:
        Driving_direction_model['evaluate'](E['step']())
        kprint(E,ignore_keys=['motor_prev'],ignore_types=[type(kprint)],title=Driving_direction_model['current_box'])
        States[Driving_direction_model['current_box']].append([E['encoder'],E['motor']])
        clf()
        if timer.check():
            timer.reset()
            pts_plot(na(States[still]),'r','.')
            pts_plot(na(States[slow_fwd])+na([0,2]),'g','.')
            pts_plot(na(States[fast_fwd])+na([0,4]),'b','.')
            pts_plot(na(States[slow_bkw])+na([0,-2]),'y','.')
            pts_plot(na(States[fast_bkw])+na([0,-4]),'k','.')
            spause()
            #raw_enter()
        #time.sleep(0.25)#
"""



#EOF
