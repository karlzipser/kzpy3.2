from kzpy3.utils3 import *

files = sggo(Arguments['path'],'*.too_small')

for f in files:
	system_string = d2s('mv',f,f.replace('.too_small',''))
	print(system_string)
	os.system(system_string)