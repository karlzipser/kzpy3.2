from kzpy3.utils3 import *


def Net(Network_layout,start):
    D = {}
    D['type'] = 'Net'
    Boxes = {}
    for box in Network_layout.keys():
        arrow_list = []
        for arrow in Network_layout[box]:
            arrow_list.append(
                Arrow(
                    function=arrow['function'],
                    destination=arrow['destination'],
                )
            )
        Boxes[box] = Box(box,arrow_list)
    D['Boxes'] = Boxes
    assert start in D['Boxes']
    D['current_box'] = start
    def function_evaluate(Environment):
        D['current_box'] = D['Boxes'][D['current_box']]['evaluate'](Environment)
        assert D['current_box'] in Network_layout.keys()
        return D['current_box']
    D['evaluate'] = function_evaluate
    return D




def Box(name,arrow_list):
    D = {}
    D['type'] = 'Box'
    D['name'] = name
    D['arrow_list'] = arrow_list
    def function_evaluate(Environment):
        np.random.shuffle(arrow_list)
        for A in arrow_list:
            destination = A['evaluate'](Environment)
            if destination != False:
                return destination
        return D['name'] # i.e., stay in same box
    D['evaluate'] = function_evaluate
    return D



def Arrow(function,destination):
    D = {}
    D['type'] = 'Arrow'
    D['function'] = function
    D['destination'] = destination
    def function_evaluate(Environment):
        if D['function'](Environment):
            return D['destination']
        else:
            return False
    D['evaluate'] = function_evaluate
    return D


        

#EOF
