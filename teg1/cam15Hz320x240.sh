#!/bin/bash

echo "Camera: 320x240, 15 Hz"

## this is for the Jetson TK1
# gst-launch -e v4l2src ! video/x-raw-yuv,format=\(fourcc\)YUY2,width=320,height=240,framerate=15/1 ! ffmpegcolorspace ! videorate ! video/x-raw-rgb,framerate=15/1 ! ffmpegcolorspace ! jpegenc ! multifilesink location="frame%05d.jpeg" &

## this is for the Jetson TX1
gst-launch-1.0 -e v4l2src ! video/x-raw,width=320,height=240! videorate ! video/x-raw,framerate=15/1 ! jpegenc ! multifilesink location="frame%05d.jpeg"
