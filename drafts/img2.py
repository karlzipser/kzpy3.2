from kzpy3.vis3 import *

def place_img_f_in_img_g(x0,y0,f,g,bottom=False,center=False):
	sf = shape(f)
	sg = shape(g)
	if bottom:
		y0 -= sf[0]
	if center:
		x0 -= sf[1]/2

	def corner(a,b_min,b_max):
		if a <= b_max:
			if a >= b_min:
				aa = a
				da = 0
			else:
				aa = b_min
				da = a - b_min
		elif a > b_max:
			aa = b_max
			da = b_max - a
		return aa,da

	x0_,x0d_ = corner(x0,0,sg[1])
	x1 = x0 + sf[1]
	x1_,x1d_ = corner(x1,0,sg[1])

	y0_,y0d_ = corner(y0,0,sg[0])
	y1 = y0 + sf[0]
	y1_,y1d_ = corner(y1,0,sg[0])

	g0 = g.copy()

	if x1 > sg[1]:
		q = -x0_
	else:
		q = -x0d_
	if y1 > sg[0]:

		u = -y0_
	else:
		u = -y0d_
	g0[  y0_:y1_+y0d_-y0d_,  x0_:x1_+x0d_-x0d_,:] = f.copy()[-y0d_:y1_+u,-x0d_:x1_+q,:]

	return g0








q = 'quit'
while True:
	if 'f' not in locals():
		f = imread(opjD('fig2.png'))[:,:,:3]
		g = imread(opjD('gnd.png'))[:,:,:3]


	inputs = input('> ')
	if inputs == q:
		break
	x = inputs[0]
	y = inputs[1]
	b,c = 0,0
	if len(inputs) > 2:
		b = inputs[2]
	if len(inputs) > 3:
		c = inputs[3]
	img = place_img_f_in_img_g(x,y,f,g,bottom=b,center=c)
	mi(img)
	plot(x,y,'r.')
	spause()



