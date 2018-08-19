#!/bin/bash

alias ssx=''
alias ssy='screen -S SY'
alias ssz='screen -S SZ'
alias srx=''
alias sry='screen -r SY'
alias srz='screen -r SZ'

OPTIONS="exit ssx ssy ssz srx sry srz"
COLUMNS=12
echo 'screens menu:'
select opt in $OPTIONS; do
  echo 'screens menu:'
   COLUMNS=12
   if [ "$opt" = "ssx" ]; then
    screen -S SX
   elif [ "$opt" = "ssy" ]; then
    screen -S SY
   elif [ "$opt" = "ssz" ]; then
    screen -S SZ
   elif [ "$opt" = "srx" ]; then
    screen -r SX
   elif [ "$opt" = "sry" ]; then
    screen -r SY
   elif [ "$opt" = "srz" ]; then
    screen -r SZ
   elif [ "$opt" = "exit" ]; then
    break 
   else
    echo bad option
   fi

done