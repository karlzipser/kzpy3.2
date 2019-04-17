#!/usr/bin/env bash
if [ $# -eq 0 ]
  then
    echo "No arguments supplied. Supply path as arg."
else
find $1 -name '*.pyc' -delete
fi
