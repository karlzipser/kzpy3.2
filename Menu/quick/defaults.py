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

current_car = 'j26June2019'
ssh_str = d2s('ssh -X',d2n(user,'@',ip))

Q = {
    '--mode--':'bash',
    'a tx_connect_2.py': d2s('python',opjk('scripts/connect/tx_connect_2.py')),
    'b Grapher/main.py': d2s('python',opjk('Grapher/main.py')),
    'c arduino_node.py':	d2s('python',opjk('Cars',current_car,'nodes','arduino_node.py')),
    'd control_node.py':	d2s('python',opjk('Cars',current_car,'nodes','control_node.py')),
    'e network_node.py':	d2s('python',opjk('Cars',current_car,'nodes','network_node.py')),
    'f car menu':	d2s('python',opjk('Menu_app/menu2.py'),'--path',opjk('Cars',current_car,'nodes'),'--dic P'),
	#'g Mr_New 169.254.131.242':'ssh -X nvidia@169.254.131.242',
	#'h Mr_Purple 169.254.131.243':'ssh -X nvidia@169.254.131.243',
    'g ssh': ssh_str,
}
if use_ssh:
    for k in Q.keys():
        if Q[k] != ssh_str:
            Q[k] = d2n(ssh_str," '",Q[k],"'")
#for k in sorted(Q.keys()):
#	cg(Q[k])

#EOF
