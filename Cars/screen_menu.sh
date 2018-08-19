#!/bin/bash

OPTIONS="exit ssx ssy ssz srx sry srz"
COLUMNS=12
echo 'car_link_menu:'
select opt in $OPTIONS; do
   COLUMNS=12
   if [ "$opt" = "ssx" ]; then
    ssx
   elif [ "$opt" = "ssy" ]; then
    ssy
   elif [ "$opt" = "ssz" ]; then
    ssz
   elif [ "$opt" = "srx" ]; then
    srx
   elif [ "$opt" = "sry" ]; then
    sry
   elif [ "$opt" = "srz" ]; then
    srz
   elif [ "$opt" = "exit" ]; then
    break 
   else
    echo bad option
   fi

done