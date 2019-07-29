#,a
from kzpy3.utils3 import *
from kzpy3.drafts.FSM.defaults import *


def Arrow(destination_name,Environment,Host_Box,function=function_true):
    D = {}
    def function_evaluate():
        if not function(Environment,Host_Box):
            return False
        else:
            return destination_name
    D['evaluate'] = function_evaluate
    return D



def Box(name,arrow_list,local_function=function_pass):
    D = {}
    D['name'] = name
    D['arrow_list'] = arrow_list
    D['local_function'] = local_function
    D['timer'] = None
    def function_evaluate(Environment):
        if D['timer'] == None:
            D['timer'] = Timer()
        D['local_function'](Environment,D)
        np.random.shuffle(arrow_list)
        for Arrow_ in arrow_list:
            destination_name = Arrow_['evaluate'](Environment)
            if destination_name != False:
                D['timer'] = None
                return destination_name
        return D['name']
    D['evaluate'] = function_evaluate
    return D



def Finite_state_machine(Box_list,start_name=None):
    D = {}
    if start_name == None:
        start_name = Box_list[0]['name']
    D['Boxes'] = {}
    for B in Box_list:
        D['Boxes'][B['name']] = B

    assert start_name in D['Boxes']
    D['current_name'] = start_name
    def function_step(Environment={}):
        destination_name = D['Boxes'][D['current_name']]['evaluate'](Environment)
        assert(destination_name)
        if destination_name != D['current_name']:
            D['current_name'] = destination_name
            
        return D['current_name']
    D['step'] = function_step
    return D




        
#,b
#EOF
