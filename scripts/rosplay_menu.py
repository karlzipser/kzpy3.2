#!/usr/bin/env python
from kzpy3.utils3 import *
do_limit = False
task = 'echo'
if 'Arguments' in locals():
	if 'task' in Arguments:
		task = Arguments['task']
	if 'limit' in Arguments:
		if Arguments['limit'] in ['t','T',1]:
			do_limit = True

print task

from kzpy3.utils3 import *

if HAVE_ROS:
	os.system('rostopic list > '+opjD('rostopic_list.txt'))
else:
	os.system('ls > '+opjD('rostopic_list1.txt'))

rl = txt_file_to_list_of_strings(opjD('rostopic_list.txt'))

if_in_expose = ['FC','FL','FR',
	'acc','button','cmd','drive','encoder','gyro','motor','steer','image','points'
]

done = False
while not done:
	pd2s('1 ) exit')
	for i in range(len(rl)):
		if do_limit:
			show = False
			for e in if_in_expose:
				if e in rl[i]:
					show = True
					break
		if show or not do_limit:
			pd2s(i+2,')',rl[i])
	try:
		n = input('select number--> ')
		assert type(n) == int
		assert n > 0
		assert n < len(rl)+2
		if n == 1:
			done = True
		else:
			if HAVE_ROS:
				os.system(d2s('rostopic',task,rl[n-2]))
			else:
				os.system(d2s('ls -al',rl[n-2]))
	except:
		print('bad option')
#EOF

