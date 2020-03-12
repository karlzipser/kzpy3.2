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
car_path = 'kzpy3/Cars/j26June2019/nodes'
Q = {
    '--mode--':'bash',
    'tx_connect_2 O': d2s('tx_connect_2.py'),
    'Grapher'+SSH: d2s('python','kzpy3/Grapher/main.py'),
    'control_node U'+SSH:    d2s('python',opj('kzpy3/Cars',current_car,'nodes','control_node.py')),
    'arduino_node U'+SSH:    d2s('python',opj('kzpy3/Cars',current_car,'nodes','arduino_node.py')),
    'network_node U'+SSH:    d2s('python',opj('kzpy3/Cars',current_car,'nodes','network_node.py')),
    'car menu U'+SSH:	d2s('python','kzpy3/Menu_app/menu2.py','--path',opj('kzpy3/Cars',current_car,'nodes'),'--dic P'),
	#'g Mr_New 169.254.131.242':'ssh -X nvidia@169.254.131.242',
	#'h Mr_Purple 169.254.131.243':'ssh -X nvidia@169.254.131.243',
    'Menu': 'python kzpy3/Menu/main.py',
    'ssh O': ssh_str,
    'roscore;rla U': 'roscore_rla.sh',

    'VT_net2__5April2019_2__18April2019_for_speed':'python kzpy3/VT_net2__5April2019_2__18April2019_for_speed/main.py',
    'ldr_img, show_image_from_ros':'show_image_from_ros.py --topic ldr_img',
    'rosplay_menu.py':'rosplay_menu.py',
    'VT_net2__1June2019':'python kzpy3/VT_net2__1June2019/main.py',

    'All car run commands': "gnome-terminal"+\
    " --tab -e 'python "+car_path+"/arduino_node.py'"+\
    " --tab -e 'python "+car_path+"/network_node.py'"+\
    " --tab -e 'python kzpy3/VT_net2__5April2019_2__18April2019_for_speed/main.py'"+\
    " --tab -e 'show_image_from_ros.py --topic ldr_img'"+\
    #" --tab -e 'python kzpy3/VT_net2__1June2019/main.py'"+\
    #" --tab -e 'python kzpy3/Grapher/main.py'"+\
    " --tab -e 'python "+car_path+"/control_node.py'",

    'All car MENUs': "gnome-terminal"+\
    " --tab -e 'python kzpy3/Menu_app/menu2.py --path "+car_path+" --dic P'"+\
    #" --tab -e 'python kzpy3/Menu_app/menu2.py --path kzpy3/VT_net2__1June2019 --dic P'"+\
    " --tab -e 'python kzpy3/Menu_app/menu2.py --path kzpy3/VT_net2__5April2019_2__18April2019_for_speed --dic P'"+\
    #" --tab -e 'python kzpy3/Menu/main.py --path kzpy3/Grapher'"+\
    ""   
}
if use_ssh:
    for k in Q.keys():
        if 'SSH' in k:
            Q[k] = d2n(ssh_str," '",'source .bashrc;source kzpy3/bashrc;',Q[k],"'")
for k in Q.keys():
    if k[-1] == 'O':
        if username == 'nvidia':
            del(Q[k])
    elif k[-1] == 'U':
        if username != 'nvidia':
            del(Q[k])
for k in Q.keys():
    if k[-1] in ['U','O']:
        l = k[:-1]
        Q[l] = Q[k]
        del Q[k]

#for k in sorted(Q.keys()):
#	cg(Q[k])

#EOF
