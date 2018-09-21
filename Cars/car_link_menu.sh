#!/bin/bash

OPTIONS="exit ls car_15Agu2018 car_24July2018 car_24July2018_no_camera car_16July2018_stable"
COLUMNS=12
echo 'car_link_menu:'
select opt in $OPTIONS; do
   COLUMNS=12
   if [ "$opt" = "car_24July2018" ]; then
    rm ~/catkin_ws/src/bair_car
    ln -s ~/kzpy3/Cars/car_24July2018 ~/catkin_ws/src/bair_car
    ls -al ~/catkin_ws/src/bair_car
   elif [ "$opt" = "car_24July2018_no_camera" ]; then
    rm ~/catkin_ws/src/bair_car
    ln -s ~/kzpy3/Cars/car_24July2018_no_camera ~/catkin_ws/src/bair_car
    ls -al ~/catkin_ws/src/bair_car
   elif [ "$opt" = "car_16July2018_stable" ]; then
    rm ~/catkin_ws/src/bair_car
    ln -s ~/kzpy3/Cars/car_16July2018_stable ~/catkin_ws/src/bair_car
    ls -al ~/catkin_ws/src/bair_car
   elif [ "$opt" = "car_15Agu2018" ]; then
    rm ~/catkin_ws/src/bair_car
    ln -s ~/kzpy3/Cars/car_15Agu2018 ~/catkin_ws/src/bair_car
    ls -al ~/catkin_ws/src/bair_car
   elif [ "$opt" = "ls" ]; then
    ls -al ~/kzpy3/Cars 
   elif [ "$opt" = "exit" ]; then
    break 
   else
    echo bad option
   fi

done