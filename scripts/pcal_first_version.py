#!/usr/bin/env python
from kzpy3.utils3 import *
from termcolor import colored
Days = {
	0:'Mon',
	1:'Tue',
	2:'Wed',
	3:'Thu',
	4:'Fri',
	5:'Sat',
	6:'Sun',
}
c = 28
today = datetime.date.today()
one_day = datetime.timedelta(days=1)
#pr = datetime.datetime.strptime('17032019', "%d%m%Y").date()
#pr2 = one_day*c + pr
pr2 = datetime.datetime.strptime('13042019', "%d%m%Y").date()
def fr(pr,today):
	for i in range((today-pr).days,19+1):
		clr='green'#cc = cg
		if i < 0:
			clr = 'grey'
		elif i < 8:
			clr = 'magenta'
		elif i < 11:
			clr='yellow'#cc = cb
		elif i > 16:
			clr='yellow'#cc = cb
		day = i*one_day+pr
		#cc(day,day-today,sf=0)
		print colored(d2n(Days[day.weekday()],' ',day.month,'/',day.day,' '),clr),colored(d2s((day-today).days,'days'),'white')

fr(pr2,today)

if 'wait' in Arguments:
	if Arguments['wait']:
		raw_enter()
#EOF