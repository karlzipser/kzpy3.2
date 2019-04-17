#!/bin/bash

python kzpy3/Cars/f6Feb19/nodes/arduino_node.py &

python kzpy3/Cars/f6Feb19/nodes/network_node.py &

python kzpy3/Cars/f6Feb19/nodes/flex_network_node.py &

python kzpy3/Cars/f6Feb19/nodes/control_node.py &


#python kzpy3/Cars/a2Apr19_16April2019/nodes/arduino_node.py &

#python kzpy3/Cars/a2Apr19_16April2019/nodes/network_node.py &

#python kzpy3/Cars/a2Apr19_16April2019/nodes/flex_network_node.py &

#python kzpy3/Cars/a2Apr19_16April2019/nodes/control_node.py &