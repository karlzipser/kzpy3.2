from kzpy3.utils3 import *

Q = {
    'CARS':{
        'j26June2019':{
            '--mode--':'bash',
            'arduino_node':'python kzpy3/Cars/j26June2019/nodes/arduino_node.py',
            'network_node':'python kzpy3/Cars/j26June2019/nodes/network_node.py',
            'control_node':'kzpy3/Cars/j26June2019/nodes/control_node.py',
            'menu2':'python kzpy3/Menu_app/menu2.py path kzpy3/Cars/j26June2019/nodes dic P', 
            'VT_net2__5April2019_2__18April2019_for_speed':'python kzpy3/VT_net2__5April2019_2__18April2019_for_speed/main.py',
            'ldr_img, show_image_from_ros':'show_image_from_ros.py topic ldr_img',
            'left, show_image_from_ros':'show_image_from_ros.py',
            'rosplay_menu.py':'rosplay_menu.py',
            'rosplay_menu.py task hz':'rosplay_menu.py task hz',
            'VT menu':'python kzpy3/Menu_app/menu2.py path kzpy3/VT_net2__5April2019_2__18April2019_for_speed dic _',
            'pgp':'cd ~/kzpy3; git pull; cd',
            'VT_net2__1June2019':'python kzpy3/VT_net2__1June2019/main.py',
            'VT_net2__1June2019 menu':'python kzpy3/Menu_app/menu2.py path kzpy3/VT_net2__1June2019 dic P',
        },
        'a2Apr19_16April2019_mess_with':{
            '--mode--':'bash',
            'network_node':'python kzpy3/Cars/a2Apr19_16April2019_mess_with/nodes/network_node.py',
            'control_node':'kzpy3/Cars/a2Apr19_16April2019_mess_with/nodes/control_node.py',
            'menu2':'python kzpy3/Menu_app/menu2.py path kzpy3/Cars/a2Apr19_16April2019_mess_with/nodes dic P', 
            'VT_net2__29April2019':'python kzpy3/VT_net2__29April2019/main.py',
            'ldr_img, show_image_from_ros':'show_image_from_ros.py topic ldr_img',
            'left, show_image_from_ros':'show_image_from_ros.py scale 4',
            'VT menu':'python kzpy3/Menu_app/menu2.py path kzpy3/VT_net2__29April2019 dic _',
            'play':"cd '/media/karlzipser/rosbags/new/Mr_Purple_23Apr19_19h20m40s'; rosbag play -s 300 *.bag",
        },

    },
    'Train_app':{
        '--mode--':'bash',
        'run':{
            '--mode--':'bash',
            'Sq120_ldr_output_4April2019':'python kzpy3/Train_app/Sq120_ldr_output_4April2019/trainloop.py',
            'Sq120_ldr_output_2nd_training_16April2019':'python kzpy3/Train_app/Sq120_ldr_output_2nd_training_16April2019/trainloop.py',
            'Sq120_ldr_output_32x1':'python kzpy3/Train_app/Sq120_ldr_output_32x1/trainloop.py',

        },
        'menu':{
            '--mode--':'bash',
            'Sq120_ldr_output_4April2019':'python kzpy3/Menu_app/menu2.py path kzpy3/Train_app/Sq120_ldr_output_4April2019 dic P',
            'Sq120_ldr_output_2nd_training_16April2019':'python kzpy3/Menu_app/menu2.py path kzpy3/Train_app/Sq120_ldr_output_2nd_training_16April2019 dic P',
            'Sq120_ldr_output_32x1':'python kzpy3/Menu_app/menu2.py path kzpy3/Train_app/Sq120_ldr_output_32x1 dic P',
        },
        'all':"gnome-terminal"+\
            " --tab -e 'python kzpy3/Train_app/Sq120_ldr_output_4April2019/trainloop.py'"+\
            " --tab -e 'python kzpy3/Train_app/Sq120_ldr_output_2nd_training_16April2019/trainloop.py'"+\
            " --tab -e 'python kzpy3/Train_app/Sq120_ldr_output_32x1/trainloop.py'"+\
            " --tab -e 'python kzpy3/Menu_app/menu2.py path kzpy3/Train_app/Sq120_ldr_output_4April2019 dic P'"+\
            " --tab -e 'python kzpy3/Menu_app/menu2.py path kzpy3/Train_app/Sq120_ldr_output_2nd_training_16April2019 dic P'"+\
            " --tab -e 'python kzpy3/Menu_app/menu2.py path kzpy3/Train_app/Sq120_ldr_output_32x1 dic P'",

    },
    'miscellaneous':{
        '--mode--':'bash',
        'pcal':     'python kzpy3/scripts/pcal',
        'test_Array':'python kzpy3/Array/test_Array.py',
        'menu test':'python kzpy3/Menu/_test.py',
        'pgp':'cd ~/kzpy3; git pull; cd',
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
    'some active data': {
        '--mode--':'active',
        'a':opjD('a'),
        'b':opjD('a'),
    },
    'W':{
        '--mode--':'extern',
        'A':opjk('Menu/A'),
        'B':opjk('Menu/B'),
    }
}


#EOF
