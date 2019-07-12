#!/usr/bin/env python
from kzpy3.utils3 import *
import Menu.main
print Arguments
import kzpy3.Menu.quick.defaults as defaults
Q = defaults.Q
sys_str = d2s(Q[sorted(Q.keys())[Arguments['choice']]])
cg('running',sys_str)
os.system(sys_str)

#EOF
