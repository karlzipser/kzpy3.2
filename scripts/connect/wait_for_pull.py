#!/usr/bin/env python

from kzpy3.utils3 import *

mtime = os.path.getmtime(opjk('.git/FETCH_HEAD'))

while time.time() - mtime > 30:
	cg('waiting for pull')
	time.sleep(1)

#EOF
