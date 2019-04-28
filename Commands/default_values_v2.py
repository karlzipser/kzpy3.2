
P = {

    'commands':{
        'Cars':{
            'a2Apr19_16April2019':{
                'arduino_node':     ('bash','python kzpy3/Cars/a2Apr19_16April2019/nodes/arduino_node.py'),
                'network_node':     ('bash','python kzpy3/Cars/a2Apr19_16April2019/nodes/network_node.py'),
                'control_node':     ('bash','kzpy3/Cars/a2Apr19_16April2019/nodes/control_node.py'),
                'menu2':            ('bash','python kzpy3/Menu_app/menu2.py path kzpy3/Cars/a2Apr19_16April2019/nodes dic P'), 
                'VT_net2__5April2019_2__18April2019_for_speed': ('bash','python kzpy3/VT_net2__5April2019_2__18April2019_for_speed/main.py'),
                'ldr_img, show_image_from_ros': ('bash','show_image_from_ros.py topic ldr_img'),
                'left, show_image_from_ros':    ('bash','show_image_from_ros.py'),
                'rosplay_menu.py':              ('bash','rosplay_menu.py'),
                'rosplay_menu.py task hz':      ('bash','rosplay_menu.py task hz'),
            },

        },
        'Train_app':{
            'Sq120_ldr_output_4April2019':                      ('bash','python kzpy3/Train_app/Sq120_ldr_output_4April2019/trainloop.py'),
            'Sq120_ldr_output_4April2019 menu':                 ('bash','python kzpy3/Menu_app/menu2.py path kzpy3/Train_app/Sq120_ldr_output_4April2019 dic P'),
            'Sq120_ldr_output_2nd_training_16April2019':        ('bash','python kzpy3/Train_app/Sq120_ldr_output_2nd_training_16April2019/trainloop.py'),
            'Sq120_ldr_output_2nd_training_16April2019 menu':   ('bash','python kzpy3/Menu_app/menu2.py path kzpy3/Train_app/Sq120_ldr_output_2nd_training_16April2019 dic P'),
        },
        'miscellaneous':{
            'pcal':     ('bash','@ python kzpy3/scripts/pcal.py wait True'),
            'pcal2':    ('bash','python kzpy3/scripts/pcal.py wait True'),
        },
        'tests': {
            'a':('set value',3.3),
            'b':('set value',99),
            'c':('set value',True),
        }

    },
}

#EOF
