#!/usr/bin/env bash

OPTIONS="t c"
COLUMNS=12
echo 'main menu'
select opt in $OPTIONS; do
   COLUMNS=12
   if [ "$opt" = "t" ]; then
    gnome-terminal --geometry 40x30+100+200
   elif [ "$opt" = "c" ]; then
    gnome-terminal --geometry 40x30+100+200 -x cmd.py
   else

    echo "bad option"
   fi
done
fi