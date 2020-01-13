from kzpy3.utils3 import *

Default_Arguments = { # top key is selected by required_arguments[0]

    'XOR':{
	    'resume':0,
	    'GPU':-1,
	    'momentum':0.001,
	    'LR':0.01,
	    'batch_size':8,
	    'backwards':True,
	    'losses_to_average':5,
	    'save_timer_time':30,
	},

    'ConDecon_test':{
	    'resume':1,
	    'GPU':-1,
	    'momentum':0.001,
	    'LR':0.01,
	    'batch_size':8,
	    'backwards':True,
	    'losses_to_average':5,
	    'save_timer_time':30,
	},

	'ConDecon_test2':{
	    'resume':1,
	    'GPU':999,
	    'momentum':0.001,
	    'LR':0.01,
	    'batch_size':512,
	    'backwards':True,
	    'losses_to_average':25,
	    'save_timer_time':5*minutes,
	},

	'ConDecon_Fire3':{
	    'resume':1,
	    'GPU':999,
	    'momentum':0.001,
	    'LR':0.01,
	    'batch_size':512,
	    'backwards':True,
	    'losses_to_average':25,
	    'save_timer_time':5*minutes,
	},
	

	'ConDecon_Fire':{
	    'resume':1,
	    'GPU':999,
	    'momentum':0.001,
	    'LR':0.01,
	    'batch_size':512,
	    'backwards':True,
	    'losses_to_average':25,
	    'save_timer_time':5*minutes,
	},
	
	'Runs_Values':{
	    'resume':1,
	    'GPU':999,
	    'momentum':0.001,
	    'LR':0.01,
	    'batch_size':64,
	    'backwards':True,
	    'losses_to_average':100,
	    'save_timer_time':5*minutes,
	}
}




#EOF
