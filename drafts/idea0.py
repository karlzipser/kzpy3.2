#,a
from kzpy3.utils3 import *

print '(' + sys.stdin.read() + ')'

dargs = set_Defaults
# add required, kprint option

def a(**p):

	print('')
	kprint(p,title='p in')
	print('')

	dargs({
		'rest':'required',
		'1':'a',
		'2':[1,2,3],
		'3':'c',
		},
		p)

	print('')
	kprint(p,title='p modified')
	print('')

if __name__ == '__main__':
	a(**Arguments)

#,b

