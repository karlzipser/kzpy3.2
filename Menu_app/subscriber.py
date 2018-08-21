from kzpy3.utils2 import *
from kzpy3.Menu_app.ros_strings import *

Topics = [
    ('/bair_car/servo_feedback',Int),
    ('/bair_car/motor',Int),
]

dic_name = 'Parameters'

a = ros_start_strs = get_ros_start_strs(node_name)
b = subscription_strs = get_ros_subscriber_strs(Topics,dic_name)
c = get_ros_publisher_strs(Topics)

d = a+b+c

list_of_strings_to_txt_file(opjD('temp.py'),d)


for e in d:
    exec(e)



list_of_strings_to_txt_file(opjD('temp.py'),d)


Left_right_center = {}

timer = Timer(3.0)
while not timer.check():
    print R
    time.sleep(0.1)

for direction in ['left', 'right', 'center']:
    R_avg = {}
    ctr = 0
    for t in R.keys():
        R_avg[t] = 0
    raw_enter(d2n('Turn to ',direction,'. Ready to start? '))
    time.sleep(0.5)
    print('recording...')

    timer = Timer(1.0)
    while not timer.check():
        for t in R.keys():
            R_avg[t] += R[t]
        ctr += 1
        time.sleep(0.01)
    for t in R.keys():
        R_avg[t] /= (1.0*ctr)
        R_avg[t] = dp(R_avg[t],2)
    Left_right_center[direction] = R_avg
    print('done.')
    pprint(R_avg)
    raw_enter()
pprint(Left_right_center)
"""
{'/bair_car/motor': 45.73737373737374, '/bair_car/servo_feedback': 371.34343434343435}
{'/bair_car/motor': 45.0, '/bair_car/servo_feedback': 371.6161616161616}

{'/bair_car/motor': 45.0, '/bair_car/servo_feedback': 190.17171717171718}
{'/bair_car/motor': 45.02020202020202, '/bair_car/servo_feedback': 189.5050505050505}

{'/bair_car/motor': 48.0, '/bair_car/servo_feedback': 266.1818181818182}
{'/bair_car/motor': 48.0, '/bair_car/servo_feedback': 265.1818181818182}



{'center': {'/bair_car/motor': 46.0, '/bair_car/servo_feedback': 269.92},
 'left': {'/bair_car/motor': 45.63, '/bair_car/servo_feedback': 194.37},
 'right': {'/bair_car/motor': 45.64, '/bair_car/servo_feedback': 358.96}}

{'center': {'/bair_car/motor': 45.13, '/bair_car/servo_feedback': 269.74},
 'left': {'/bair_car/motor': 45.79, '/bair_car/servo_feedback': 193.18},
 'right': {'/bair_car/motor': 45.31, '/bair_car/servo_feedback': 357.79}}
 

"""
#EOF
