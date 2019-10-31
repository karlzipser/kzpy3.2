
from kzpy3.utils3 import *
import kzpy3.drafts.Markov2.markov as markov
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




if __name__ == '__main__':
    
    def environment():
        return {
            'encoder': max(0,0.1+0.1*rndn()),
            'motor': int(max(0,49+10*rndn())),
        }

    while True:
        Driving_direction_model['step'](environment())
        raw_enter()




#EOF
