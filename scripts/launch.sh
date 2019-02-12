#!/bin/bash

rm -r ~/.ros/log/* &
roslaunch bair_car bair_car.launch use_zed:=true record:=true &
python kzpy3/Cars/f6Feb19/nodes/arduino_node.py &
python kzpy3/Cars/f6Feb19/nodes/network_node.py &
python kzpy3/Cars/f6Feb19/nodes/flex_network_node.py &
python kzpy3/Cars/f6Feb19/nodes/control_node.py &