from kzpy3.utils3 import *

c = 28
one_day = datetime.timedelta(days=1)
pr = datetime.datetime.strptime('17032019', "%d%m%Y").date()
pr2 = one_day*c + pr
def fr(pr):
	for i in range(11,15):
		cg(i*one_day+pr)