from kzpy3.utils2 import *
from kzpy3.Menu_app.ros_strings import *


Topics = [
    ('/bair_car/servo_feedback',Int),
    ('/bair_car/motor',Int),
]

subscription_strs = get_ros_subscriber_strs(Topics)

for c in [rosimport_str,rospyinit_str]+subscription_strs:
    if using_linux(): exec(c)


Left_right_center = {}

timer = Timer(3.0)
while not timer.check():
    print R
    time.sleep(0.1)

R_avg = {}
ctr = 0
for t in R.keys():
    R_avg[t] = 0

for direction in ['left', 'right', 'center']:
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

"""
{'/bair_car/motor': 45.73737373737374, '/bair_car/servo_feedback': 371.34343434343435}
{'/bair_car/motor': 45.0, '/bair_car/servo_feedback': 371.6161616161616}

{'/bair_car/motor': 45.0, '/bair_car/servo_feedback': 190.17171717171718}
{'/bair_car/motor': 45.02020202020202, '/bair_car/servo_feedback': 189.5050505050505}

{'/bair_car/motor': 48.0, '/bair_car/servo_feedback': 266.1818181818182}
{'/bair_car/motor': 48.0, '/bair_car/servo_feedback': 265.1818181818182}
"""
#EOF
