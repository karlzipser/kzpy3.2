from kzpy3.utils2 import *
from kzpy3.Menu_app.menu import *

menu_path = opjh('.menu','network_node')

Topics = [
    ('servo_feedback_left',Int),
    ('servo_feedback_right',Int),
    ('servo_feedback_center',Int)
]

if __name__ == '__main__':
    menu(Topics,menu_path)
    
#EOF