from kzpy3.utils3 import *

files = sggo(Arguements['path'],'*.too_small')

for f in files:
	print(d2s('mv',f,f.replace('.too_small','')))