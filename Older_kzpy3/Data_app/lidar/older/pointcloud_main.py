#!/usr/bin/env python
from kzpy3.vis3 import *

import kzpy3.Data_app.lidar.python_pointclouds6g as python_pointclouds6hh

Output = python_pointclouds6h.Output

#threading.Thread(target=python_pointclouds6h.pointcloud_thread,args=[]).start()

timer = Timer(5)

len_prev = 0

while not timer.check():
    len_o = len(Output)
    if len_o > len_prev:
        mi(Output['e'].transpose(1,0));spause()#;raw_enter()
    len_prev = len_o


#EOF