from kzpy3.utils2 import *
#import std_msgs.msg
#import geometry_msgs.msg
#import rospy


Int = 'std_msgs.msg.Int32'
Rostopics = {'cmd/steer':{'type':Int},
    'cmd/motor':{'type':Int},
    'cmd/motor':{'type':Int},
    'cmd/motor':{'type':Int},
    'cmd/motor':{'type':Int}
    }

callback_strs = []
subscriber_strs = []
for name in Rostopics.keys():
    if 'extra' in Rostopics[name].keys():
        extra = Rostopics[name]['extra']
    else:
        extra = ''
    callback_name = 'callback_'+get_safe_name(name)
    callback_strs.append(d2n("def ",callback_name,"(msg):",extra,"\n\tP['",name,"'] = msg\n"))
    subscriber_strs.append(d2n("rospy.Subscriber('",name,"', ",Rostopics[name]['type'],", callback=",callback_name,')\n'))

rospyinit_str = "rospy.init_node('rostopics',anonymous=True)"

print "\n################\n#"
print rospyinit_str
for c in callback_strs:
    print c
for s in subscriber_strs:
    print s
print "#\n################"