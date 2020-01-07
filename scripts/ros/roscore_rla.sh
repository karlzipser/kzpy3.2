#!/bin/bash
source .bashrc
source kzpy3/bashrc

roscore &
sleep 5
rlog;roslaunch bair_car bair_car.launch use_zed:=true record:=true
#rla &


