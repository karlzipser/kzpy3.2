from kzpy3.utils3 import *

project_path = pname(opjh(__file__))

Q = {
    'other_parameters':{

        'graphics_timer_time':1,
        'abort':False,
        'graphics_ylim':[-0.1,1.],
        'meo_num':8,
    },
    'network_parameters': {
		'NUM_INPUT_CHANNELS':2,
		'NUM_OUTPUTS':1,
		'NUM_METADATA_CHANNELS':0,
		'INPUT_WIDTH':168,
		'INPUT_HEIGHT':94,
		'METADATA_WIDTH':41,
		'METADATA_HEIGHT':23,
		'BATCH_SIZE':64,
		'NUM_LOSSES_TO_AVERAGE':1,
        'RESUME':False,
        'NETWORK_OUTPUT_FOLDER':opjD('Networks',fname(project_path)),
        'NET_SAVE_TIMER_TIME':60,
        'GPU':1, # -1->no GPU, 999->choose least used GPU
    }
}



#EOF
