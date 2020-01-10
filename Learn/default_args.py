from kzpy3.utils3 import *

Default_Arguments = { # top key is selected by required_arguments[0]

    'XOR':{
	    'RESUME':0,
	    'GPU':-1,
	    'MOMENTUM':0.001,
	    'LR':0.01,
	    'BATCH_SIZE':8,
	    'NUM_LOSSES_TO_AVERAGE':5,
	    'NET_SAVE_TIMER_TIME':30,
	},

    'ConDecon_test':{
	    'RESUME':1,
	    'GPU':-1,
	    'MOMENTUM':0.001,
	    'LR':0.01,
	    'BATCH_SIZE':8,
	    'NUM_LOSSES_TO_AVERAGE':5,
	    'NET_SAVE_TIMER_TIME':30,
	},

	'ConDecon_test2':{
	    'RESUME':1,
	    'GPU':999,
	    'MOMENTUM':0.001,
	    'LR':0.01,
	    'BATCH_SIZE':512,
	    'NUM_LOSSES_TO_AVERAGE':25,
	    'NET_SAVE_TIMER_TIME':5*minutes,
	},

	'ConDecon_Fire3':{
	    'RESUME':1,
	    'GPU':999,
	    'MOMENTUM':0.001,
	    'LR':0.01,
	    'BATCH_SIZE':512,
	    'BACKWARDS':True,
	    'NUM_LOSSES_TO_AVERAGE':25,
	    'NET_SAVE_TIMER_TIME':5*minutes,
	},
	
	'Runs_Values':{
	    'RESUME':1,
	    'GPU':999,
	    'MOMENTUM':0.001,
	    'LR':0.01,
	    'BATCH_SIZE':64,
	    'NUM_LOSSES_TO_AVERAGE':100,
	    'NET_SAVE_TIMER_TIME':5*minutes,
	}
}




#EOF
