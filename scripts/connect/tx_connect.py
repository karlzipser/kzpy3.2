#!/usr/bin/env python

from kzpy3.utils3 import *

setup_Default_Arguments(
	{
		'start': 243,
		'stop': None,
		'base_ip': '169.254.131',
		'update_time':1.,
		'ssh': False,
		'username': 'nvidia',
		'rsync': True,
	}
)

print_Arguments()

mtime = 0

ssh_ip = d2n(Arguments['base_ip'],'.',Arguments['start'])
ssh_date_time(ssh_ip)

while True:
	if Arguments['rsync']:
		_,max_mtime = most_recent_py_file(return_mtime=True)
		if mtime < max_mtime:
			mtime = max_mtime
			if False:
				update_TXs_range(
					Arguments['start'],
					Arguments['stop'],
					Arguments['base_ip'],
				)
			update_TXs([ssh_ip,])
	if Arguments['ssh'] or not Arguments['rsync']:
		break
	time.sleep(Arguments['update_time'])


if False:
	if Arguments['ssh']:
		host_str = d2n(Arguments['username'],'@',Arguments['base_ip'],'.',Arguments['start'])
		print host_str
		#cr(host_str,ra=2)
		os.system(d2s('ssh -X ',host_str))
		#cr(2,ra=2)
		
		
#EOF
