from kzpy3.utils3 import *

Default_Arguments = {

    'XOR':{
	    'RESUME':True,
	    'GPU':-1,
	    'MOMENTUM':0.001,
	    'LR':0.01,
	    'BATCH_SIZE':8,
	    'NUM_LOSSES_TO_AVERAGE':5,
	    'NET_SAVE_TIMER_TIME':30,
	},

    'ConDecon_test':{
	    'RESUME':True,
	    'GPU':-1,
	    'MOMENTUM':0.001,
	    'LR':0.01,
	    'BATCH_SIZE':8,
	    'NUM_LOSSES_TO_AVERAGE':5,
	    'NET_SAVE_TIMER_TIME':30,
	},

	'ConDecon_test2':{
	    'RESUME':True,
	    'GPU':999,
	    'MOMENTUM':0.001,
	    'LR':0.01,
	    'BATCH_SIZE':512,
	    'NUM_LOSSES_TO_AVERAGE':25,
	    'NET_SAVE_TIMER_TIME':5*minutes,

	},
	'Runs_Values':{
	    'RESUME':True,
	    'GPU':999,
	    'MOMENTUM':0.001,
	    'LR':0.01,
	    'BATCH_SIZE':64,
	    'NUM_LOSSES_TO_AVERAGE':100,
	    'NET_SAVE_TIMER_TIME':5*minutes,
	}
}