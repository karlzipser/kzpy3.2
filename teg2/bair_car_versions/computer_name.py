# This should be place in ~ (home dir).
# This is used to specifiy caffe mode and data file name information

from kzpy3.utils import time_str

computer_name = 'Mr_Orange'
Direct = 0.
Follow = 1.
Play = 0.
Furtive = 0.
Caf = 1.0
Location = 'campus'

if Direct == 1:
	task = 'direct'
elif Play == 1:
	task = 'play'
elif Follow == 1:
	task = 'follow'
elif Furtive == 1:
	task = 'furtive'
else:
	assert(False)


foldername = ''
if Follow == 1:
	foldername = 'follow_'

if Caf == 1:
	foldername = foldername + 'caffe_z2_'

foldername = foldername + task + '_'

foldername = foldername + Location + '_'

foldername = foldername + time_str() + '_'

foldername = foldername + computer_name






