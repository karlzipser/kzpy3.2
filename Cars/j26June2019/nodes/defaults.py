from kzpy3.utils3 import *
project_path = pname(__file__)
#cg(project_path,ra=1)
Q = {
    '--mode--':'bash',
    'arduino_node':'python '+project_path+'/arduino_node.py',
    'network_node':'python '+project_path+'/network_node.py',
    'control_node':''+project_path+'/control_node.py',
    'menu2':'python kzpy3/Menu_app/menu2.py --path '+project_path+' --dic P', 
    'VT_net2__5April2019_2__18April2019_for_speed':'python kzpy3/VT_net2__5April2019_2__18April2019_for_speed/main.py',
    'ldr_img, show_image_from_ros':'show_image_from_ros.py --topic ldr_img',
    'left, show_image_from_ros':'show_image_from_ros.py',
    'rosplay_menu.py':'rosplay_menu.py',
    'rosplay_menu.py task hz':'rosplay_menu.py --task hz',
    'VT menu':'python kzpy3/Menu_app/menu2.py --path kzpy3/VT_net2__5April2019_2__18April2019_for_speed --dic _',
    'pgp':'cd ~/kzpy3; git pull; cd',
    'VT_net2__1June2019':'python kzpy3/VT_net2__1June2019/main.py',
    'VT_net2__1June2019 menu':'python kzpy3/Menu_app/menu2.py --path kzpy3/VT_net2__1June2019 --dic P',

    
}







#EOF
