#!/usr/bin/env python
from kzpy3.utils3 import *
import Menu.main

"""
setup_Default_Arguments(
	{
		'choice': 1,
	}
)
"""

import kzpy3.Menu.quick.defaults as defaults
Q = defaults.Q
#pprint(defaults.Q)
#cr(Arguments['choice'])
sys_str = d2s(Q[sorted(Q.keys())[Arguments['choice']]])
cg(sys_str)
os.system(sys_str)

#EOF
