from Paths_Module import *
exec(identify_file_str)

for _name in [
	'IMAGES',
	'MASKS',
	'SCALE',
	'img',
	'img1',
	'img2',
	'mask'
	]:exec(d2n(_name,'=',"'",_name,"'"))

#

#EOF