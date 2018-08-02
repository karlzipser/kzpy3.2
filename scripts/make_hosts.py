#!/usr/bin/env python

from kzpy3.utils2 import *

base_ip = '192.168.1.'
host_ip_dic = {
	'Mr_Plain':101,
	'Mr_New':103
}

host = os.environ('COMPUTER_NAME')

host_list = [
	('127.0.0.1','localhost'),
	(base_ip+str(host_ip_dic[host]),host)
	]

for h in sorted(host_ip_dic.keys()):
	if h != host:
		host_list.append(host_ip_dic[host],host)

pprint(host_list)