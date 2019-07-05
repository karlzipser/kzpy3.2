#!/usr/bin/env python
from kzpy3.utils3 import *

setup_Default_Arguments({
	'start': 242,
	'stop': None,
	'base_ip': '169.254.131',
	'update_time':1.,
	})

print_Arguments()

mtime = 0

while True:
	_,max_mtime = most_recent_py_file(return_mtime=True)
	if mtime < max_mtime:
		mtime = max_mtime
		update_TXs_range(
			Arguments['start'],
			Arguments['stop'],
			Arguments['base_ip'],
		)
	time.sleep(Arguments['update_time'])

#EOF
