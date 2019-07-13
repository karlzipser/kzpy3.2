#!/usr/bin/env python
from kzpy3.utils3 import *
import Menu.main
import kzpy3.Menu.quick.defaults as defaults
Q = defaults.Q
sorted_keys = sorted(Q.keys())
for i in rlen(sorted_keys):
	k = sorted_keys[i]
	if k[0] == '-':
		continue
	pd2s(i,k)

#EOF
