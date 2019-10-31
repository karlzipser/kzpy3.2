from kzpy3.utils3 import *


UP = 'UP'
DN = 'DN'
tc = 'time_constant'
dst = 'destination'


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
        #kprint(arrow_list,title=box)
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
    #D['timer'] = Timer()
    #D['timer'].time_s = -1
    #print_timer = Timer(0.05)
    def function_evaluate(Environment):
        #print_timer.message(D['name'])
        np.random.shuffle(arrow_list)
        for A in arrow_list:
            destination = A['evaluate'](Environment)
            if destination != False:
                #cy(destination)
                return destination
        #cb(D['name'])
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
