#!/usr/bin/env python

from kzpy3.utils3 import *

mtime = os.path.getmtime(opjk('.git/FETCH_HEAD'))
print mtime,time.time()
while time.time() - mtime > 10:
	mtime = os.path.getmtime(opjk('.git/FETCH_HEAD'))
	cg('waiting for pull')
	time.sleep(1)
cy('pull occurred')


#EOF
