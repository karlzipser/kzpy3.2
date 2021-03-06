from kzpy3.utils3 import *

project_path = pname(opjh(__file__))

Q = {
    'other_parameters':{
        'RESUME':False,
        'NETWORKS_FOLDER':opjD('Networks',fname(project_path)),
    },
    'network_parameters': {
		'NUM_INPUT_CHANNELS':2,
		'NUM_OUTPUTS':1,
		'NUM_METADATA_CHANNELS':0,
		'INPUT_WIDTH':168,
		'INPUT_HEIGHT':94,
		'METADATA_WIDTH':41,
		'METADATA_HEIGHT':23,
		'NUM_IN_BATCH':64,
    }
}

#EOF
