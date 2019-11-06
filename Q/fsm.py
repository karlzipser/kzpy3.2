from kzpy3.utils3 import *



def eg_run(N,E,Q):

    P = Q['Q']

    prev_box = None 

    while True:
        if 'Menu data processing':
            if Q['load']():
                pass

            if P['aBORT']:
                clp('aBORT ==',True)
                break

            if P['pAUSE']:
                clp('pAUSE ==',True)
                time.sleep(P['pause_sleep_time'])
                continue

            if P['cLEAR']:
                clp('cLEAR ==',True)
                clear_screen()

        R = N['evaluate'](Environment=E)


        if R['function'] != None:
            if prev_box != None:# and prev_box != R['destination']:
                X = '`y'
                Y = '`g'
                if 'fail' in R['function']:
                    Z = '`wm'
                    print(fline())
                else:
                    Z = '`--r'
                clp(prev_box,X,'--',Y,'`','--',Y,R['function'],Z,'-->',Y,R['destination'],X)
                time.sleep(P['sleep_time'])

        prev_box = R['destination']

        E['step']()


def Net(Network_layout,start):
    D = {}
    D['type'] = 'Net'
    Boxes = {}
    for box in Network_layout.keys():
        arrow_list = []
        for A in Network_layout[box]:
            kprint(A,box)
            if 'p' not in A:
                A['p'] = 1.
            arrow_list.append(
                Arrow(
                    function=A['function'],
                    destination=A['destination'],
                    p=A['p'],
                )
            )
        Boxes[box] = Box(box,arrow_list)
    D['Boxes'] = Boxes
    assert start in D['Boxes']
    D['current_box'] = start
    def function_evaluate(Environment):
        R = D['Boxes'][D['current_box']]['evaluate'](Environment)
        D['current_box'] = R['destination']
        assert D['current_box'] in Network_layout.keys()
        return R
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
            R = A['evaluate'](Environment)
            if R['destination'] != False:
                return R
        return {'destination':D['name'],'function':None} # i.e., stay in same box
    D['evaluate'] = function_evaluate
    return D



def Arrow(function,destination,p):
    D = {}
    D['type'] = 'Arrow'
    def function_evaluate(Environment):
        Fail = {'destination':False,'function':None}
        r = rnd()
        if r > p:
            return Fail
        if Environment['functions'][function](Environment):
            return {'destination':destination,'function':function}
        else:
            return Fail
    D['evaluate'] = function_evaluate
    return D


        

#EOF
