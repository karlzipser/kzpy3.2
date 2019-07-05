from kzpy3.utils3 import *
project_path = pname(__file__)

width = 300
height = 200

Q = {
    'times':{
        'show':1/30.,
        'shift': 0.0222,#1/180.,
        'baseline_ticks':1/10.,
        'thread_delay':0.001,
    },
    'window':{
        'height':height,
        'width':width,
    },
    'data':{
    
        'encoder':{
            'scale': 10.,
            'offset': 0.5,
            'color': [255,255,255],
            'value': None,
            'baseline': 0,
        },
        'd_heading':{
            'scale': 40,
            'offset': 0.75,
            'color': [255,0,0],
            'value': None,
            'baseline': 0,
        },

        'a':{
            'scale': 15.,
            'offset': 1/2.,
            'color': [255,255,0],
            'value': None,
            'baseline': 0,
        },
        'b':{
            'scale': 20.,
            'offset': 1/4.,
            'color': [0,255,0],
            'value': None,
            'baseline': 0,
        },
        'c':{
            'scale': 10.,
            'offset': 3.*1/4.,
            'color': [0,255,255],
            'value': None,
            'baseline': 0.5,
        },
    },
    'ABORT':False,
    'images2':{
        'test':rndn(100,200,3),
    },
}

P = {
    #'read_only':{
    #    'ABORT':False,
    #},
    'images':{
        'big':np.zeros((height,width,3),np.uint8),
        'small':np.zeros((height,1,3),np.uint8),
    },    
}