#!/bin/bash

python kzpy3/Cars/f6Feb19/nodes/arduino_node.py &

python kzpy3/Cars/f6Feb19/nodes/network_node.py &

python kzpy3/Cars/f6Feb19/nodes/flex_network_node.py &

python kzpy3/Cars/f6Feb19/nodes/control_node.py &