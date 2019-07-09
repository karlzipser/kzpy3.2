from kzpy3.utils3 import *
import kzpy3.drafts.Markov.markov as markov
import kzpy3.drafts.Markov.defaults as defaults


"""
def build_arrow_list():
    pass

arrow_list = [
    markov.Arrow(
        [
            {'name':'a','val':-10,'op':markov.less_than,},
            {'name':'b','val':-7,'op':markov.equals,},
        ],
        transition_probability = 0.15,
        destination = 'box_A',
    ),
    markov.Arrow(
        [
            {'name':'a','val':-10,'op':markov.less_than,},
            {'name':'b','val':-7,'op':markov.equals,},
        ],
        transition_probability = 0.25,
        destination = 'box_B',
    ),
]

#,a


#,a

Environment = {
    'a': 1,
    'b': -7,
}
"""
UP = 'UP'
DN = 'DN'
en_gt = 'encoder__greater_than'
en_lt = 'encoder__less_than'
mo_gt = 'motor__greater_than'
mo_lt = 'motor__less_than'

tc = 'time_constant'
dst = 'destination'
still = 'still'
slow_fwd = 'slow_forward'
fast_fwd = 'fast_forward'
slow_bkw = 'slow_backward'
fast_bkw = 'fast_backward'




k = 0.1
U = {
    still: {
        UP: { en_gt:.01, mo_gt: 50, tc:k, dst:slow_fwd },
        DN: { en_gt:.01, mo_lt: 48, tc:k, dst:slow_bkw },
    },
    slow_fwd: {
        UP: { en_gt:.1, mo_gt: 52, tc:k, dst:fast_fwd },
        DN: { en_lt:.1, mo_lt:50, tc:k, dst:still },
    },
    fast_fwd: {
        DN: { en_lt:.1, mo_lt: 52, tc:k, dst:slow_fwd },
    },
    slow_bkw: {
        UP: { en_lt:.01, mo_lt: 48, tc:k, dst:still },
        DN: { en_gt:.1, mo_lt: 46, tc:k, dst:fast_bkw },
    },
    fast_bkw: {
        UP: { en_lt:.1, mo_gt: 46, tc:k, dst:slow_bkw },
    },
}

box_list = []
for d in U.keys():
    arrow_list = []
    for u in U[d].keys(): 
        X = U[d][u]
        keys = X.keys()
        keys.remove(tc)
        keys.remove(dst)
        var_dic_list = []
        for k in keys:
            s = k.split('__')
            name = s[0]
            val = X[k]
            if s[1] == 'greater_than':
                op = markov.greater_than
            elif s[1] == 'less_than':
                op = markov.less_than
            var_dic_list.append({'name':name,'op':op,'val':val,})
        arrow_list.append(
            markov.Arrow(
                var_dic_list=var_dic_list,
                transition_probability=X[tc],
                destination=X[dst],
            )
        )
    box_list.append(
        markov.Box(d,arrow_list)
    )

#,b

markov.Arrow(
        [
            {'name':'a','val':-10,'op':markov.less_than,},
            {'name':'b','val':-7,'op':markov.equals,},
        ],
        transition_probability = 0.15,
        destination = 'box_A',
    )




#B = Box(arrow_list)
#B['evaluate'](Environment)

#,b


#EOF
