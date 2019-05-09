from kzpy3.vis3 import *

if 'f' not in locals():
	f = imread(opjD('fig2.png'))[:,:,:3]
	g = imread(opjD('gnd.png'))[:,:,:3]
	sf = shape(f)
	sg = shape(g)


def corner(a,b_min,b_max,show=False):
	if show:
		cg(a,b_max,b_max)
	if a <= b_max:
		if a >= b_min:
			aa = a
			da = 0
			if show:
				cg('1')
		else:
			aa = b_min
			da = a - b_min
			if show:
				cb('2')
	elif a > b_max:
		aa = b_max
		da = b_max - a
		if show:
				cy('3')
	return aa,da


def test(x0,y0):

	x0_,x0d_ = corner(x0,0,sg[1],show=True)
	x1 = x0 + sf[1]
	x1_,x1d_ = corner(x1,0,sg[1],show=True)

	y0_,y0d_ = corner(y0,0,sg[0])
	y1 = y0 + sf[0]
	y1_,y1d_ = corner(y1,0,sg[0])

	g0 = g.copy()

	cg('x0',x0,' x0_',x0_,' x0d_',x0d_,' x1',x1,' x1_',x1_,' x1d_',x1d_)
	cb(((y0_,y1_),(x0_,x1_+x0d_-x0d_)),((0,y1_-y0_),(-x0d_,x1_-x0d_)))
	cy(-x0d_,x1_-x0d_)
	if x1 > sg[1]:
		q = -x0_
	else:
		q = -x0d_
	if y1 > sg[0]:
		cr('a')
		u = -y0_
	else:
		u = -y0d_
		cr('b')
	#g0[  y0_:y1_,  x0_:x1_+x0d_-x0d_,:] = f.copy()[:y1_-y0_,-x0d_:x1_+q,:]
	g0[  y0_:y1_+y0d_-y0d_,  x0_:x1_+x0d_-x0d_,:] = f.copy()[-y0d_:y1_+u,-x0d_:x1_+q,:]
	mi(g0)
	spause()




