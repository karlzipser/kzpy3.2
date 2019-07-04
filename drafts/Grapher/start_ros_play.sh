#!/bin/bash

roscore &

sleep 3

cd /media/nvidia/rosbags/processed_20Jun19_15h14m12s/tegra-ubuntu_13Mar19_17h52m59s

rosbag play *.bag

#EOF