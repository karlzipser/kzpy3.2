#!/bin/bash

roscore &

sleep 3

#cd /media/nvidia/rosbags/processed_20Jun19_15h14m12s/tegra-ubuntu_13Mar19_17h52m59s
#cd /media/nvidia/rosbags/processed_05Jul19_13h06m04s/Mr_Purple_28Jun19_13h35m10s
cd /media/nvidia/rosbags/processed_05Jul19_13h06m04s/Mr_Purple_25Jun19_19h54m47s

rosbag play *.bag

#EOF