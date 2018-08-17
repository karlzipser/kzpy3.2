from kzpy3.utils2 import *
from kzpy3.Menu_app.ros_strings import *


Topics = [
    ('/bair_car/servo_feedback',Int),
    ('/bair_car/motor',Int),
]

subscription_strs = get_ros_subscriber_strs(Topics)

for c in [rosimport_str,rospyinit_str]+subscription_strs:
    if using_linux(): exec(c)

R_avg = {}
ctr = 0
for t in R.keys():
    R_avg[t] = 0



raw_enter('Eeady to start? Hit enter...')
time.sleep(0.5)
print('recording...')

timer = Timer(1.0)
while not timer.check():
    for t in R.keys():
        R_avg[t] += R[t]
    ctr += 1
for t in R.keys():
    R_avg[t] /= (1.0*ctr)

print('done.')
pprint(R)

raw_enter()


#EOF
