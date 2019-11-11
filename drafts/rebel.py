from kzpy3.utils3 import *


Commands = {
    'Sit':{
        'body':'upward flat hand up toward sky with right hand',
        'situations':['dog is standing around',],
    },
    'Down':{
        'body':'open hand moves down toward ground right hand',
        'situations':[
            'dog is jumping on you',
            'dog is reaching for table',
        ],
    },
    'Stay':{
        'body':'open hand like stop sign pointing toward her, okay to release',
        'situations':[
            "you don't want dog to move",
        ]
    },
    'Drop it':{
        'body':'<none>',
        'situations':[
            'dog has leaf in mouth',
        ]
    },
    'Leave it':{
        'body':'<none>',
        'situations':[
            'Do approaches a small stone on the road',
        ],
    },
    'Come (loud)':{
        'body':'clap, maybe run other direction, great treat',
        'situations':['dog runs after a bird'],
    },
}
'Let’s go':
    'use when going want her to get going instead of sniffing',

'Pee':'go pee',

'Off':'not to jump up',

'Wait':
    'she should not go to eat, like',

'Yes':
    'when she does what she is supposed to do',

'Bravo':
    'when done with a training series',

'All done':
    'when done with a play session'
    }

while True:
    clear_screen()
    ky = a_key(Commands)
    val = Commands[ky]
    print val
    raw_enter()
    print ky
    raw_enter()

