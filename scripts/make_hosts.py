#!/usr/bin/env python

from kzpy3.utils2 import *

os.environ['COMPUTER_NAME'] = 'Mr_Plain'

host_file_path = opjh('hosts')
host = os.environ['COMPUTER_NAME']

base_ip = '192.168.1.'
host_ip_dic = {
	'Mr_Plain':101,
	'Mr_New':103,
	'Mr_Black':11,
	'Mr_Blue':121,
	'Mr_Blue_Back':120
}


host_list = [
	d2s('127.0.0.1','localhost'),
	d2s(base_ip+str(host_ip_dic[host]),host)
	]

for h in sorted(host_ip_dic.keys()):
	if h != host:
		host_list.append(d2s(base_ip+str(host_ip_dic[h]),h))

list_of_strings_to_txt_file(host_file_path,host_list)
unix(d2s('more',host_file_path))

for h in host_list:
	print h
pd2s("Saved 'hosts' to",host_file_path,'. Make sure to ln -s it to /etc/hosts.')