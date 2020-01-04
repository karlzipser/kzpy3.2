from kzpy3.utils3 import *

Default_Arguments = {
    'XOR':{
	    'resume':True,
	    'gpu':-1,
	    'momentum':0.001,
	    'lr':0.01,
	    'batch_size':8,
	    'num_losses_to_average':5,
	    'save_time':30,
	},
    'ConDecon_test':{
	    'resume':True,
	    'gpu':-1,
	    'momentum':0.001,
	    'lr':0.01,
	    'batch_size':8,
	    'num_losses_to_average':5,
	    'save_time':30,
	},
	'Runs_Values':{
	    'resume':True,
	    'gpu':999,
	    'momentum':0.001,
	    'lr':0.01,
	    'batch_size':64,
	    'num_losses_to_average':100,
	    'save_time':5*minutes,
	}
}