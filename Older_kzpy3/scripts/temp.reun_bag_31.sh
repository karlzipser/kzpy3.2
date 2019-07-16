#!/usr/bin/env bash

roscore &
sleep 5
cd /media/nvidia/rosbags/new/Mr_Purple_07Jul19_16h01m55s
rosbag play -l *31.bag
