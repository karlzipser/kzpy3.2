from kzpy3.utils3 import *

project_path = pname(opjh(__file__))

Q = {
    'other_parameters':{

        'graphics_timer_time':1,
        'abort':False,
        'graphics_ylim':[-0.1,1.],
        'meo_num':64,
    },
    'network_parameters': {
        'NET_TYPE':'XOR',# 'Runs_Values',
		'BATCH_SIZE':64,
		'NUM_LOSSES_TO_AVERAGE':5,
        'RESUME':True,
        'NETWORK_OUTPUT_FOLDER':opjD('Networks',fname(project_path)),
        'NET_SAVE_TIMER_TIME':60*5,
        'GPU':-1, # -1->no GPU, 999->choose least used GPU
    }
}



#EOF
