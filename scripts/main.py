#!/usr/bin/env python

from kzpy3.utils3 import *
clp('test','`b',fline())
print(fline())
setup_Default_Arguments(
	{
		'start': 242,
		'stop': None,
		'base_ip': '169.254.131',
		'update_time':1.,
		'ssh': False,
		'username': 'nvidia',
		'rsync': True,
	}
)
time.sleep(3)
print(fline())
print(fline())
print_Arguments()
print(fline())
print(fline())
clp(fline(),'`','test','`r',)
print(fline())
kprint(range(10),d2s('test',fline()))
#EOF