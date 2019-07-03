from kzpy3.utils3 import *
project_path = pname(__file__)

Q = {
    'timers':{
        'show':1/30.,
        'shift':1/180.,
    },
    'window':{
        'height':400,
        'width':1200,
    },
    'data':{
        'a':{
            'scale': 80.,
            'offset': 1/2.,
            'color': [255,255,255],
            'value': 0,
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
            'color': [255,0,255],
            'value': 0,
        },
    },  
}