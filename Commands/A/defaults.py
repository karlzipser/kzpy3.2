from kzpy3.utils3 import *

Q = {
    'CARS':{
        'a2Apr19_16April2019':{
            '--mode--':'bash',
            'ls':                          'ls -al',
            'arduino_node':                'python kzpy3/Cars/a2Apr19_16April2019/nodes/arduino_node.py',
            'network_node':                'python kzpy3/Cars/a2Apr19_16April2019/nodes/network_node.py',
            'control_node':                'kzpy3/Cars/a2Apr19_16April2019/nodes/control_node.py',
            'menu2':                       'python kzpy3/Menu_app/menu2.py path kzpy3/Cars/a2Apr19_16April2019/nodes dic P', 
            'VT_net2__5April2019_2__18April2019_for_speed':\
                                            'python kzpy3/VT_net2__5April2019_2__18April2019_for_speed/main.py',
            'ldr_img, show_image_from_ros': 'show_image_from_ros.py topic ldr_img',
            'left, show_image_from_ros':    'show_image_from_ros.py',
            'rosplay_menu.py':              'rosplay_menu.py',
            'rosplay_menu.py task hz':      'rosplay_menu.py task hz',
        },
    },
    'Train_app':{
        'Sq120_ldr_output_4April2019':                          'python kzpy3/Train_app/Sq120_ldr_output_4April2019/trainloop.py',
        'Sq120_ldr_output_4April2019 menu':                     'python kzpy3/Menu_app/menu2.py path kzpy3/Train_app/Sq120_ldr_output_4April2019 dic P',
        'Sq120_ldr_output_2nd_training_16April2019':            'python kzpy3/Train_app/Sq120_ldr_output_2nd_training_16April2019/trainloop.py',
        'Sq120_ldr_output_2nd_training_16April2019 menu':       'python kzpy3/Menu_app/menu2.py path kzpy3/Train_app/Sq120_ldr_output_2nd_training_16April2019 dic P',
        '--mode--':'bash',
    },
    'miscellaneous':{
        '--mode--':'bash',
        'pcal':     'python kzpy3/scripts/pcal',
    },
    'tests': {
        'a': 3.3,
        'b': 99,
        'more': {
            'c': True,
            'more': {
                '--mode--':'const',
                'd':'abc',
                'e':[1],
            },
        },
    },
    'ZZZ': {
        '--extern--': opjk('Commands/Q.py'),
    },
    'some data':{
        '--active--': opjD('a'),
    },
}


#EOF
