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

if False:
	try:
		o = lo(opjD('state'))
	except:
		cr('state.pkl not loaded')
		o = {}
	o['last_ip'] = Arguments['start']
	so(opjD('state'),o)


mtime = 0

while True:
	if Arguments['rsync']:
		_,max_mtime = most_recent_py_file(return_mtime=True)
		if mtime < max_mtime:
			mtime = max_mtime
			update_TXs_range(
				Arguments['start'],
				Arguments['stop'],
				Arguments['base_ip'],
			)
	if Arguments['ssh'] or not Arguments['rsync']:
		#cr(0,ra=1)
		break
	time.sleep(Arguments['update_time'])

if Arguments['ssh']:
	host_str = d2n(Arguments['username'],'@',Arguments['base_ip'],'.',Arguments['start'])
	print host_str
	#cr(host_str,ra=2)
	os.system(d2s('ssh -X ',host_str))
	#cr(2,ra=2)
#EOF
