from kzpy3.vis3 import *

def in_or_out(x,y,w,h,a,b):
	cb(0)
	if x+w > a:
		cb(1)
		print y+h,b
		if y+h > b:
			cb(1)
			if x+w > a:
				cb(1)
				if y-h < b:
					cb(1)
					if x-h < a:
						cb(1)
						if y+h > b:
							cb(1)
							if x-h < a:
								cb(1)
								if y-h < b:
									cb(1)
									return True
	return False
for i in range(100):
	clf()
	xysqlim(3)
	x = np.random.randn()
	y = np.random.randn()
	h = 1#np.abs(np.random.randn())
	w = 1#np.abs(np.random.randn())
	a = np.random.randn()
	b = np.random.randn()
	plot(x,y,'y.')
	plot(x+h,y+h,'k.')
	plot(x-h,y+h,'k.')
	plot(x-h,y-h,'k.')
	plot(x+h,y-h,'k.')
	plot(a,b,'bo')
	spause()
	result = in_or_out(x=x,y=y,w=w,h=h,a=a,b=b)
	say(result)
	raw_enter()

