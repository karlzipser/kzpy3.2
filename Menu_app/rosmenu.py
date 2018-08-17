from kzpy3.utils2 import *
from kzpy3.Menu_app.ros_strings import *
import_str = "import kzpy3.Cars.car_24July2018.nodes.default_values as default_values"
CS_(import_str,say_comment=False)
exec(import_str)

R = {}

Rostopics_to_publish = [
    ('network_smoothing_parameter',Float),
    ('network_output_sample',Int),
    ('network_motor_offset',Int),
    ('network_steer_gain',Float),
    ('network_motor_gain',Float),
    ('servo_pwm_smooth_manual_offset',Int)
]

if True:
    print "\n################\n#"
    if using_linux(): exec(rosimport_str)
    print rosimport_str
    if using_linux(): exec(rospyinit_str)
    print rospyinit_str
    print "#\n################"

    pub_setup_strs,pub_publish_strs = get_ros_publisher_strs(Rostopics_to_publish,R,default_values.Network,initalize_Rs=True)
    print "\n################\n#"
    for p in pub_setup_strs:
        if using_linux(): exec(p)
        print p
    print "#\n################"
    print "\n################\n#"
    for c in pub_publish_strs:
        if using_linux(): exec(c)
        print c
    print "#\n################"

def clear_screen():
    print(chr(27) + "[2J")

def menu(Topics):
    message = False
    choice_number = 0
    while choice_number != 1:
        try:
            
            clear_screen()

            ctr = 1

            print d2n(ctr,') ','exit')

            for topic in Topics:

                ctr += 1

                name = topic[0]

                if topic[1] == Int:
                    print d2n(ctr,') ',name,': ',int(R[name]))

                else:
                    print d2n(ctr,') ',name,': ',dp(R[name],2))

            if message:
                print message

            choice_number = input('#? ')

            if not is_number(choice_number):
                message = "bad option"

            elif choice_number == 1: # see "while choice_number != 1:" above
                pass

            else:
                message = False
                index_number = int(choice_number)-2
                name = Topics[index_number][0]
                current_val = R[name]
                val = num_from_str(raw_input(d2n(name,'(',current_val,') new value > ')))
                if is_number(val):
                    R[name] = val
                    if Topics[index_number][1] == Int:
                        R[name] = int(R[name])
            pub_setup_strs,pub_publish_strs = get_ros_publisher_strs(Topics,R,default_values.Network)
            for c in pub_publish_strs:
                if using_linux(): exec(c)

        except Exception as e:
            print("********** rosmenu.py Exception ***********************")
            print(e.message, e.args)

    clear_screen()

if __name__ == '__main__':
    menu(Rostopics_to_publish)
#EOF