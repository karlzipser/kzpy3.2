#!/usr/bin/env python

from kzpy3.utils3 import *

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

print_Arguments()