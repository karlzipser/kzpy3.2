from kzpy3.utils3 import *


Default_Arguments = { # top key is selected by required_arguments[0]

	'--default--':{
	    'resume':1,
	    'GPU':999,
	    'momentum':0.001,
	    'LR':0.01,
	    'batch_size':64,
	    'backwards':True,
	    'losses_to_average':25,
	    'save_timer_time':5*minutes,
	    'runs':'train',
	},

    'XOR':{
	    'GPU':-1,
	    'batch_size':8,
	    'losses_to_average':5,
	    'save_timer_time':30,
	},

	'ConDecon_test2':{
	    'batch_size':512,
	},

	'ConDecon_Fire':{
	},
	
	'Runs_Values':{
	}
}

for k in Default_Arguments:
	if k != '--default--':
		for l in Default_Arguments['--default--']:
			if l not in Default_Arguments[k].keys():
				Default_Arguments[k][l] = Default_Arguments['--default--'][l]

#kprint(Default_Arguments)

#EOF