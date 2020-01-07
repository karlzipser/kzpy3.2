#!/usr/bin/env bash
#echo "*** Running clean_pycs.sh ***"
if [ $# -eq 0 ]
  then
    echo "No arguments supplied. Assume path = ~/kzpy3"
    find ~/kzpy3 -name '*.pyc' -delete
else
find $1 -name '*.pyc' -delete
fi
