
from kzpy3.utils3 import *

from kzpy3.drafts.FSM.defaults import *


def Finite_state_machine(Compact_notation,start):
    D = {}
    C = Compact_notation
    Boxes = {}
    for d in C.keys():
        arrow_list = []
        for u in C[d].keys(): 
            X = C[d][u]
            keys = X.keys()
            keys.remove(tc)
            keys.remove(dst)
            var_dic_list = []
            for k in keys:
                s = k.split('__')
                name = s[0]
                val = X[k]
                if s[1] == 'greater_than':
                    op = greater_than
                elif s[1] == 'less_than':
                    op = less_than
                var_dic_list.append({'name':name,'op':op,'val':val,})
            arrow_list.append(
                Arrow(
                    var_dic_list=var_dic_list,
                    transition_probability=X[tc],
                    destination=X[dst],
                )
            )
        Boxes[d] = Box(d,arrow_list)
    D['Boxes'] = Boxes
    assert start in D['Boxes']
    D['current_box'] = start
    def function_step(Environment):
        D['current_box'] = D['Boxes'][D['current_box']]['evaluate'](Environment)
        return D['current_box']
    D['step'] = function_step
    return D




def Box(name,arrow_list):
    D = {}
    D['name'] = name
    D['arrow_list'] = arrow_list
    D['timer'] = Timer()
    D['timer'].time_s = -1
    print_timer = Timer(0.05)
    def function_evaluate(Environment):
        print_timer.message(D['name'])
        np.random.shuffle(arrow_list)
        for A in arrow_list:
            destination = A['evaluate'](Environment)
            if destination != False:
                return destination
        return D['name'] # i.e., stay in same box
    D['evaluate'] = function_evaluate
    return D



def Arrow(var_dic_list,transition_probability,destination):
    D = {}
    D['transition_probability'] = transition_probability
    D['destination'] = destination
    D['Vars'] = {}
    for v in var_dic_list:
        D['Vars'][v['name']] = {'val':v['val'],'op':v['op']}
    def function_evaluate(Environment):
        if rnd() > D['transition_probability']:
            return False
        Vars = D['Vars']
        for n in Vars:
            val = Vars[n]['val']
            op = Vars[n]['op']
            f = op.func_name
            e = Environment[n]
            if not op(e,val):
                return False
        return D['destination']
    D['evaluate'] = function_evaluate
    return D



def less_than(a,b):
    if a < b:
        return True
    else:
        return False

def greater_than(a,b):
    return less_than(-a,-b)

def equals(a,b):
    if a == b:
        return True
    else:
        return False
        

#EOF
