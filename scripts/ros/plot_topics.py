#!/usr/bin/env python
"""
python kzpy3/scripts/temp.py topics headings_left,headings_right,headings_direct colors red,green,blue
"""

from kzpy3.vis3 import *
assert HAVE_ROS
import rospy
import std_msgs.msg
import geometry_msgs.msg
from std_msgs.msg import Int32MultiArray
from sensor_msgs.msg import Image
import cv_bridge
bridge = cv_bridge.CvBridge()
if 'falloff' not in Arguments:
    Arguments['falloff'] = 0.1
else:
    Arguments['falloff'] = float(Arguments['falloff'])
cg(Arguments['topics'])
cb(Arguments['colors'])
topics = Arguments['topics'].split(',')
cb('topics =')
for t in topics:
    cg(d2n("'",t,"'"))

colors = Arguments['colors'].split(',')
assert len(topics) == len(colors)
cb('colors =',colors)
Topic_colors = {}
for i in rlen(topics):
    Topic_colors[topics[i]] = colors[i]
    print topics[i],colors[i]

Prediction2D_plot = CV2Plot(height_in_pixels=120,
    width_in_pixels=10,
    pixels_per_unit=1,
    x_origin_in_pixels=0,
    y_origin_in_pixels=60
)
"""
Prediction2D_plot = CV2Plot(height_in_pixels=Arguments['height_in_pixels'],
    width_in_pixels=Arguments['width_in_pixels'],
    pixels_per_unit=Arguments['pixels_per_unit'],
    x_origin_in_pixels=Arguments['x_origin_in_pixels']
    y_origin_in_pixels=Arguments['y_origin_in_pixels']
)
"""
Prediction2D_plot['verbose'] = False


S = {}

for topic in topics:
    s = """
def TOPIC_callback(data):
    S['TOPIC'] = na(data.data).astype(float)/1000.

rospy.Subscriber('/TOPIC',std_msgs.msg.Int32MultiArray, callback= TOPIC_callback,queue_size=1)


        """
    s = s.replace('TOPIC',topic)
    print s
    exec(s)

rospy.init_node('main',anonymous=True)


timer = Timer(10)

Colors = {'blue':(0,0,255),'green':(0,255,0),'red':(255,0,0)}


while True:

    try:
        for topic in topics:
            xys = []
            for i in rlen(S[topic]):
                xys.append([i,S[topic][i]])
            xys = na(xys)

            #Prediction2D_plot['clear']()
            img = Prediction2D_plot['image'].astype(float)
            img *= Arguments['falloff']
            Prediction2D_plot['image'] = img.astype(np.uint8)

            Prediction2D_plot['pts_plot'](xys,Colors[Topic_colors[topic]])

            k = Prediction2D_plot['show'](delay=33,title='image',fx=4*12,fy=4*1)

            if k == ord('q'):
                sys.exit()
    
    except KeyboardInterrupt:
        cr('\n\n*** KeyboardInterrupt ***\n')
        sys.exit()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        CS_('Exception!',emphasis=True)
        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno,'\t',time.time()),emphasis=False)
        time.sleep(1)
    





#EOF



















