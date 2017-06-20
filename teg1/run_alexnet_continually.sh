#!/bin/bash 
# Run this from caffe dir.

 COUNTER=0
 while [  $COUNTER -lt 100000 ]; do
     echo The counter is $COUNTER
     let COUNTER=COUNTER+1
     build/tools/caffe time --model=models/bvlc_alexnet/deploy.prototxt --gpu=0
 done