from kzpy3.utils3 import *

project_path = pname(opjh(__file__))

Q = {
    'other_parameters':{
        'RESUME':False,
        'NETWORKS_FOLDER':opjD('Networks',fname(project_path)),
        'graphics_timer_time':1,
        'abort':False,
        'graphics_ylim':[-0.1,30.],
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
    }
}

#EOF
