#!/usr/bin/env python

from kzpy3.utils import *

host_ip_dic = {
	'Mr_Plain':101,
	'Mr_New':103
}

host = 'Mr_Plain'

host_list = [
	(127.0.0.1,'localhost'),
	(host_ip_dic[host],host)
	]

for h in sorted(host_ip_dic.keys()):
	if h != host:
		host_list.append(host_ip_dic[host],host)