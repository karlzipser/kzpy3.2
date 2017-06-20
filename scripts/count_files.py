#!/usr/bin/python
from kzpy3.utils_mini import *
#import os
#import glob
cwd = os.getcwd()
print (len(glob.glob(os.path.join(cwd,'*'))))
