#!/usr/bin/env python
from kzpy3.utils3 import *
import default_values

cr("\nproject path =",default_values.P['project_path'],"\nMake sure this is correct.\n")
raw_enter()
timer = Timer(4*7*24*3600)

files = sggo('/home/karlzipser/Desktop/Data/Network_Predictions_projected/*.net_projections.h5py')
GOOD_LIST = []
for f in files:
    GOOD_LIST.append(fname(f).split('.')[0])
GOOD_LIST = ['tegra-ubuntu_15Nov18_20h53m56s']
for r in GOOD_LIST:
    #sys_str = 'ulimit -Sn 65000; python ~/kzpy3/Train_app/Train_SqueezeNet_15Sept2018_1Nov_14Nov/Main.py'
    sys_str = d2s('ulimit -Sn 65000; python',opj(default_values.P['project_path'],'Main.py'))#,'run',r)
    cg(sys_str)
    os.system(sys_str)

cg("\n",__file__,"complete.\n")

#EOF
