#!/bin/bash

rla &

python kzpy3/Cars/f6Feb19/nodes/arduino_node.py &

python kzpy3/Cars/f6Feb19/nodes/network_node.py &

python kzpy3/Cars/f6Feb19/nodes/flex_network_node.py &

python kzpy3/Cars/f6Feb19/nodes/control_node.py &

gnome-terminal --geometry 40x30+100+200 -x python kzpy3/Menu_app/menu2.py path kzpy3/Cars/f6Feb19/nodes dic P 

#python kzpy3/Menu_app/menu2.py path kzpy3/Cars/f6Feb19/nodes dic P 




#python kzpy3/Cars/a2Apr19_16April2019/nodes/arduino_node.py &

#python kzpy3/Cars/a2Apr19_16April2019/nodes/network_node.py &

#python kzpy3/Cars/a2Apr19_16April2019/nodes/flex_network_node.py &

#python kzpy3/Cars/a2Apr19_16April2019/nodes/control_node.py &


rla &

python kzpy3/Cars/a2Apr19_16April2019/nodes/arduino_node.py &

python kzpy3/Cars/a2Apr19_16April2019/nodes/network_node.py &

python kzpy3/Cars/a2Apr19_16April2019/nodes/flex_network_node.py &

python kzpy3/Cars/a2Apr19_16April2019/nodes/control_node.py &

python kzpy3/Menu_app/menu2.py path kzpy3/Cars/a2Apr19_16April2019/nodes dic P 

python kzpy3/VT_net2__5April2019_2__18April2019_for_speed/main.py





Commands = {

    'a2Apr19_16April2019':{
        'arduino_node':'python kzpy3/Cars/a2Apr19_16April2019/nodes/arduino_node.py',
        'rla':'rla',
        'network_node':'python kzpy3/Cars/a2Apr19_16April2019/nodes/network_node.py',
        'flex_network_node':'python kzpy3/Cars/a2Apr19_16April2019/nodes/flex_network_node.py',
        'control_node':'kzpy3/Cars/a2Apr19_16April2019/nodes/control_node.py',
        'menu2':'python kzpy3/Menu_app/menu2.py path kzpy3/Cars/a2Apr19_16April2019/nodes dic P', 
        'VT_net2__5April2019_2__18April2019_for_speed':'python kzpy3/VT_net2__5April2019_2__18April2019_for_speed/main.py',
    },

}