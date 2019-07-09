from kzpy3.utils3 import *



def Net(box_list):
    D = {}
    return D




def Box(name,arrow_list):
    D = {}
    D['name'] = name
    D['arrow_list'] = arrow_list
    D['timer'] = Timer()
    D['timer'].time_s = -1
    def function_evaluate(Environment):
        np.random.shuffle(arrow_list)
        for A in arrow_list:
            d = A['evaluate'](Environment)
            if d != False:
                cg(d)
                return d
        cr(False)
        return False
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
            cy(D['destination'],val,f,e, op(val,e))
            if not op(val,e):
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
