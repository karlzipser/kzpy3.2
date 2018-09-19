#!/usr/bin/env python

from kzpy3.utils2 import *


host_file_path = opjh('hosts')
host = os.environ['COMPUTER_NAME']

#base_ip = '192.168.1.'
base_ip = '172.20.10.'
host_ip_dic = {
	'Mr_Plain':101,
	'Mr_New':103,
	'Mr_Black':11,
	'Mr_Blue':121,
	'Mr_Blue_Back':2,
	'laptop':50,
	'Mr_Purple':106,
	'Mr_PurpleB0':12,
}

alias_list = []
host_list = [
	"# this file generated by make_hosts.py via kzpy3/bashrc. Manual changes will be overwritten.",
	d2s('#',time_str()),
	d2s('127.0.0.1','localhost'),
	d2s(base_ip+str(host_ip_dic[host]),host)
	]

for h in sorted(host_ip_dic.keys()):
	if h != host:
		host_list.append(d2s(base_ip+str(host_ip_dic[h]),h))
		alias_list.append(d2n("alias ",h,"='ssh ", base_ip+str(host_ip_dic[h]),"'"))
#print host_list
list_of_strings_to_txt_file(host_file_path,host_list)
list_of_strings_to_txt_file(opjh('ssh_aliases'),alias_list)
#unix(d2s('more',host_file_path))
#print ""
#for h in host_list:
#	print h
#print ""
#pd2s("make_hosts.py saved 'hosts' to",host_file_path,'\b.\n')