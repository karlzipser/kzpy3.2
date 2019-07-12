#!/usr/bin/env python
from kzpy3.utils3 import *
import Menu.main

Q = Menu.main.start_Dic(
    dic_project_path=opjk(),
    Dics={},
    Arguments={
        'menu':False,
        'read_only':False,
    }
)
T = Q['Q']
Q['load']()

#user = T['State']['default_ssh_user']
ip = T['State']['default_ssh_ip_prefex']+T['State']['default_ssh_ip_suffix']
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
