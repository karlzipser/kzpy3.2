from kzpy3.utils3 import *
from kzpy3.drafts.FSM.finite_state_machine import *



def y_function(E,D):
    cy(D['name'],int(D['timer'].time()))
    time.sleep(1)
def g_function(E,D):
    cg(D['name'],int(D['timer'].time()))
    time.sleep(1)
def r_function(E,D):
    cr(D['name'],int(D['timer'].time()))
    time.sleep(1)
def b_function(E,D):
    cb(D['name'],int(D['timer'].time()))
    time.sleep(1)

def function_t(Environment):
    if rnd() > Environment['transition_probability/function_t']:
        cr('fail')
        return False
    cg('success')
    return

def function_0_or_1(Environment):
	try:
	    i = input('enter zero or one: ')
	    if i:
	        return True
	    else:
	        return False
	except:
		return False

Environment = {
    'transition_probability/function_t':0.2,
}

Fsm = Finite_state_machine(
    [
        Box('in B1',
        	[
        		Arrow('exit B1',0.1,function_0_or_1)
        	],
        	y_function
        ),
        Box('exit B1',
        	[
            	Arrow('enter B2',0.1,function_t),
            	Arrow('in B1',0.1,function_t)
        	],
        	g_function
        ),
        Box('enter B2',[Arrow('in B2',0.1,function_true)],b_function),
        Box('in B2',[Arrow('in B1',0.1,function_true)],r_function),    
    ],
)

while True:
	Fsm['step'](Environment)

# ~ $ python kzpy3/drafts/FSM/main.py

#EOF
