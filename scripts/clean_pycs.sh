#!/usr/bin/env bash
echo "Running clean_pycs.sh"
if [ $# -eq 0 ]
  then
    echo "No arguments supplied. Supply path as arg. E.g., clean_pycs.sh ~/kzpy3"
else
find $1 -name '*.pyc' -delete
fi
