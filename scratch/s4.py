from kzpy3.utils3 import *

def Dictionary():
	D = {'1':'a'}
	def _function_ref(s):
		q = s.split('/')
		if len(q) == 1:
			return D[q[0]]
		else:
			return _(D[q[1:]])
	D['ref'] = _function_ref
	return D

T = Dictionary()
print T['ref']('1')

T/a/b/c/d/ = 10

T['a']['b']['c']['d'] = 10

s = 'T/a/b/c/d/ = 10'

s = 'P/human/servo pwm/ = 10'
l = s.split('/')
d = l[0]
ks = l[1:]
