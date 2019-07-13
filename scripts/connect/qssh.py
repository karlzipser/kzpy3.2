#!/usr/bin/env python

from kzpy3.utils3 import *
import Menu.main

R = Menu.main.start_Dic(
    dic_project_path=opjk(),
    Dics={},
    Arguments={
        'menu':False,
        'read_only':False,
    }
)
T = R['Q']
R['load']()

user = T['State']['default_ssh_user']
ip = T['State']['default_ssh_ip_prefex']+T['State']['default_ssh_ip_suffix']
use_ssh = T['State']['use ssh for quick commands']
if use_ssh:
    SSH = 'SSH'
else:
    SSH = ''
current_car = 'j26June2019'
ssh_str = d2s('ssh -X',d2n(user,'@',ip))
cg('attempt',ssh_str)

os.system(ssh_str)


#EOF
