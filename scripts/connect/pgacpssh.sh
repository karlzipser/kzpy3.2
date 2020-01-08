#!/usr/bin/env bash
if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
else
echo "gpacp..."
cd ~/kzpy3
git add .;git commit -m 'gacp';git push origin master
echo "nvidia@192.168.1.$1 git pull..."
ssh nvidia@192.168.1.$1 "cd kzpy3;git pull"
echo "done."
fi
