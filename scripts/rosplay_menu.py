from kzpy3.utils2 import *

if HAVE_ROS:
	os.system('rostopic list > '+opjD('rostopic_list.txt'))
else:
	os.system('ls > '+opjD('rostopic_list1.txt'))

rl = txt_file_to_list_of_strings(opjD('rostopic_list1.txt'))

for i in range(len(rl)):
	pd2s(i,')',rl[i])

n = input('select number--> ')
print n
assert type(n) == int
assert n >= 0
assert n < len(rl)

if HAVE_ROS:
	print 'linux'
	os.system(d2s('rostopic echo',rl[n]))
else:
	os.system(d2s('ls -al',rl[n]))
