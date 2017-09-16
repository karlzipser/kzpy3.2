#!/bin/bash

OPTIONS="exit ls bdd_car_rewrite_SD2 bdd_car_rewrite_SD2_LCR bdd_car_rewrite_SD2_LCR_net 
  robot_car_6Aug2017 robot_car_22Aug2017 robot_car_23Aug2017 robot_car_28Aug2017 robot_car_29Aug2017_debug
  robot_car_1Sept2017 robot_car_observer1
  aruco_driver_9Sept2017 aruco_driver_16Sept2017"
COLUMNS=12
echo 'car_link_menu:'
select opt in $OPTIONS; do
   COLUMNS=12
   if [ "$opt" = "reboot" ]; then
    echo "Rebooting . . ."
    sudo reboot
   elif [ "$opt" = "shutdown" ]; then
    echo "Shutting down . . ."
    ssd
   elif [ "$opt" = "rla" ]; then
    rla
   elif [ "$opt" = "robot_car_6Aug2017" ]; then
    rm ~/catkin_ws/src/bair_car
    ln -s ~/kzpy3/Cars/robot_car_6Aug2017 ~/catkin_ws/src/bair_car
    ls -al ~/catkin_ws/src/bair_car
   elif [ "$opt" = "robot_car_22Aug2017" ]; then
    rm ~/catkin_ws/src/bair_car
    ln -s ~/kzpy3/Cars/robot_car_22Aug2017 ~/catkin_ws/src/bair_car
    ls -al ~/catkin_ws/src/bair_car
   elif [ "$opt" = "robot_car_23Aug2017" ]; then
    rm ~/catkin_ws/src/bair_car
    ln -s ~/kzpy3/Cars/robot_car_23Aug2017 ~/catkin_ws/src/bair_car
    ls -al ~/catkin_ws/src/bair_car
   elif [ "$opt" = "robot_car_28Aug2017" ]; then
    rm ~/catkin_ws/src/bair_car
    ln -s ~/kzpy3/Cars/robot_car_28Aug2017 ~/catkin_ws/src/bair_car
    ls -al ~/catkin_ws/src/bair_car
   elif [ "$opt" = "aruco_driver_9Sept2017" ]; then
    rm ~/catkin_ws/src/bair_car
    ln -s ~/kzpy3/Cars/aruco_driver_9Sept2017 ~/catkin_ws/src/bair_car
    ls -al ~/catkin_ws/src/bair_car

   elif [ "$opt" = "aruco_driver_16Sept2017" ]; then
    rm ~/catkin_ws/src/bair_car
    ln -s ~/kzpy3/Cars/aruco_driver_16Sept2017 ~/catkin_ws/src/bair_car
    ls -al ~/catkin_ws/src/bair_car

   elif [ "$opt" = "robot_car_29Aug2017_debug" ]; then
    rm ~/catkin_ws/src/bair_car
    ln -s ~/kzpy3/Cars/robot_car_29Aug2017_debug ~/catkin_ws/src/bair_car
    ls -al ~/catkin_ws/src/bair_car
   elif [ "$opt" = "robot_car_1Sept2017" ]; then
    rm ~/catkin_ws/src/bair_car
    ln -s ~/kzpy3/Cars/robot_car_1Sept2017 ~/catkin_ws/src/bair_car
    ls -al ~/catkin_ws/src/bair_car
   elif [ "$opt" = "robot_car_observer1" ]; then
    rm ~/catkin_ws/src/bair_car
    ln -s ~/kzpy3/Cars/robot_car_observer1 ~/catkin_ws/src/bair_car
    ls -al ~/catkin_ws/src/bair_car
   elif [ "$opt" = "bdd_car_rewrite_SD2" ]; then
    rm ~/catkin_ws/src/bair_car
    ln -s ~/kzpy3/teg2/bdd_car_versions/bdd_car_rewrite_SD2/bair_car ~/catkin_ws/src/bair_car
    ls -al ~/catkin_ws/src/bair_car
   elif [ "$opt" = "bdd_car_rewrite_SD2_LCR" ]; then
    rm ~/catkin_ws/src/bair_car
    ln -s ~/kzpy3/teg2/bdd_car_versions/bdd_car_rewrite_SD2_LCR/bair_car ~/catkin_ws/src/bair_car
    ls -al ~/catkin_ws/src/bair_car
   elif [ "$opt" = "bdd_car_rewrite_SD2_LCR_net" ]; then
    rm ~/catkin_ws/src/bair_car
    ln -s ~/kzpy3/teg2/bdd_car_versions/bdd_car_rewrite_SD2_LCR_net/bair_car ~/catkin_ws/src/bair_car
    ls -al ~/catkin_ws/src/bair_car
   elif [ "$opt" = "ls" ]; then
    ls -al ~/kzpy3/Cars 
   elif [ "$opt" = "exit" ]; then
    break 
   else
    echo bad option
   fi

done