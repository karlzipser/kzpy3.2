#!/usr/bin/env python
from kzpy3.utils3 import *
import default_values

cr("\nproject path =",default_values.P['project_path'],"\nMake sure this is correct.\n")
raw_enter()
timer = Timer(4*7*24*3600)

while not timer.check():
    #sys_str = 'ulimit -Sn 65000; python ~/kzpy3/Train_app/Train_SqueezeNet_15Sept2018_1Nov_14Nov/Main.py'
    sys_str = d2s('ulimit -Sn 65000; python',opj(default_values.P['project_path'],'Main.py'))
    cg(sys_str)
    os.system(sys_str)

cg("\ntrainloop complete.\n")

#EOF
