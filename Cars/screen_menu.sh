#!/bin/bash

OPTIONS="exit screen_1 resume_screen_1 screen_2 resume_screen_2"
COLUMNS=12
echo 'screen_menu:'
select opt in $OPTIONS; do
   COLUMNS=12
   if [ "$opt" = "screen_1" ]; then
    screen -S screen_1
   elif [ "$opt" = "screen_2" ]; then
    screen -S screen_2
   elif [ "$opt" = "resume_screen_1" ]; then
    screen -r screen_1
   elif [ "$opt" = "resume_screen_2" ]; then
    screen -r screen_2
   elif [ "$opt" = "exit" ]; then
    break 
   else
    echo bad option
   fi

done