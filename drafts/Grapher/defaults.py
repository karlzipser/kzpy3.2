from kzpy3.utils3 import *
project_path = pname(__file__)

# Mr_Purple_28Jun19_13h35m10s

width = 400
height = 400

Q = {
    'ABORT': False,
    'CLEAR': False,
    'pAUSE': False,
    'times': {
        'show':1/30.,
        'shift': 1/20.,
        'baseline_ticks':1/10.,
        'thread_delay':0.001,
    },
    'window': {
        'height':height,
        'width':width,
        'shift_top':100,
        'shift_bottom':height-0,
    },
    'parameters': {
        'smooth_color':[255,255,255],
    },
    #'topics': ['encoder','d_heading','human/steer'],
    'topics': ['encoder','cmd/motor'],
    'image_topics': ['left_image','right_image'],
    'data':{
        'encoder':{
            'scale': 10.,
            'offset': 200,
            'color': [0,255,255],
            'value': None,
            'baseline': 0,
            's': 0.99,
        },
        'd_heading':{
            'scale': 40.,
            'offset': 0.75,
            'color': [255,0,0],
            'value': None,
            'baseline': 0,
        },
        'human/motor':{
            'scale': 1,
            'offset': 0.5,
            'color': [0,255,255],
            'value': None,
            'baseline': 49,
        },
        'drive_direction':{
            'scale': 20.,
            'offset': 170,
            'color': [0,0,255],
            'value': None,
            'baseline': 0.,
        },
        'cmd/motor':{
            'scale': 5.,
            'offset': 300,
            'color': [0,255,0],
            'value': None,
            'baseline': 49,
            's': 0.99,
        },
        'human/steer':{
            'scale': 1.,
            'offset': 0.5,
            'color': [255,255,0],
            'value': None,
            'baseline': 49,
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

    'images':{
        'left_image':{
            'scale': 0.25,
            'y_offset': 3,
            'x_offset': 25+-60,
            'x_align': 'right',
            'y_align': 'top',
            'value': None,
        },
        'right_image':{
            'scale': 0.25,
            'y_offset': 3,
            'x_offset': 25+0,
            'x_align': 'left',
            'y_align': 'top',
            'value': None,
        },      
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