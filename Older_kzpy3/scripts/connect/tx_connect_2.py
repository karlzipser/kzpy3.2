#!/usr/bin/env python
from kzpy3.utils3 import *
import Menu.main

Q_state = Menu.main.start_Dic()
State = Q_state['Q']['State']
Q_state['load'](noisy=False)

ip = State['ssh']['ip_prefex']+State['ssh_ip_suffix']
update_time = 1
mtime = 0

ssh_date_time(ip)

while True:
	_,max_mtime = most_recent_py_file(return_mtime=True)
	if mtime < max_mtime:
		mtime = max_mtime
		update_TXs([ip])
	time.sleep(update_time)
		
#EOF
