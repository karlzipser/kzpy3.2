from kzpy3.utils3 import *
project_path = pname(__file__)

width = 300
height = 200

Q = {
    'times':{
        'show':1/30.,
        'shift': 0.0222,#1/180.,
        'baseline_ticks':1/10.
    },
    'window':{
        'height':height,
        'width':width,
    },
    'data':{
        'encoder':{
            'scale': 15.,
            'offset': 1/2.,
            'color': [255,255,255],
            'value': None,
            'baseline': 0,
        },
        'd_heading':{
            'scale': .1,
            'offset': 0.55,
            'color': [255,0,0],
            'value': None,
            'baseline': 0,
        },
        'a':{
            'scale': -15.,
            'offset': 1/2.,
            'color': [255,255,0],
            'value': 0.2,
            'baseline': 0,
        },
        'b':{
            'scale': 20.,
            'offset': 1/4.,
            'color': [0,255,0],
            'value': 0,
        },
        'c':{
            'scale': 75.,
            'offset': 3.*1/4.,
            'color': [0,0,255],
            'value': 0,
        },
    },
    'params':{
        'thread_delay':0.001,
        'ABORT':False,
    },
    'images2':{
        'test':rndn(100,200,3),
    },
}

P = {
    'read_only':{
        'ABORT':False,
    },
    'images':{
        'big':np.zeros((height,width,3),np.uint8),
        'small':np.zeros((height,1,3),np.uint8),
    },    
}