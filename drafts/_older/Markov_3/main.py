
from kzpy3.vis3 import *
import kzpy3.drafts.Markov_3.markov as markov
#import kzpy3.drafts.Markov.defaults as defaults


UP = markov.UP
DN = markov.DN
tc = markov.tc
dst = markov.dst
en_gt = 'encoder__greater_than'
en_lt = 'encoder__less_than'
mo_gt = 'motor__greater_than'
mo_lt = 'motor__less_than'
still = 'still'
slow_fwd = 'slow_forward'
fast_fwd = 'fast_forward'
slow_bkw = 'slow_backward'
fast_bkw = 'fast_backward'

k = 1.

Compact_notation = {
    still: {
        UP: { en_gt:.01, mo_gt: 51, tc:k, dst:slow_fwd },
        DN: { en_gt:.01, mo_lt: 41, tc:k, dst:slow_bkw },
    },
    slow_fwd: {
        UP: { en_gt:.5, mo_gt: 55, tc:k, dst:fast_fwd },
        DN: { en_lt:.1, mo_lt:51, tc:k, dst:still },
    },
    fast_fwd: {
        DN: { en_lt:.5, mo_lt: 55, tc:k, dst:slow_fwd },
    },
    slow_bkw: {
        UP: { en_lt:.01, mo_gt: 39, tc:k, dst:still },
        DN: { en_gt:.1, mo_lt: 35, tc:k, dst:fast_bkw },
    },
    fast_bkw: {
        UP: { en_lt:.1, mo_gt: 35, tc:k, dst:slow_bkw },
    },
}

Driving_direction_model = markov.Net(Compact_notation,still)


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
        #if D['motor'] < 49 and D['motor'] > 41:
        #    D['encoder'] = 0
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




#EOF
