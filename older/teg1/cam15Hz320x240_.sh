#!/bin/bash

# This code commands the webcam to save frames at 15Hz in the directory in which it is called.

echo "Camera: 320x240, 15 Hz"

gst-launch -e v4l2src ! video/x-raw-yuv,format=\(fourcc\)YUY2,width=320,height=240,framerate=15/1 ! ffmpegcolorspace ! videorate ! video/x-raw-rgb,framerate=15/1 ! ffmpegcolorspace ! jpegenc ! multifilesink location="frame%05d.jpeg" &