#!/usr/bin/env python
from kzpy3.utils3 import *
from termcolor import colored
from datetime import date

set_Argument_defaults(Arguments,{'p':7,'f':28})



Days = {
	0:'Mon',
	1:'Tue',
	2:'Wed',
	3:'Thu',
	4:'Fri',
	5:'Sat',
	6:'Sun',
}

today = datetime.date.today()
ref_day = date(2019,4,29)
one_day = datetime.timedelta(days=1)

pr = datetime.datetime.strptime('13042019', "%d%m%Y").date()

my_day_pattern = [0,0, 1,1, 0,0,0,0,0, 1,1,1,1,1]

Day_colors = {}
dcs = [((1,7),'red'),((8,9),'yellow'),((10,14),'green'),((15,16),'yellow'),((17,23),'blue'),((23,28),'cyan')]
for d in dcs:
	r = d[0]
	c = d[1]
	for i in range(r[0]-1,r[1]):
		#print i,c
		Day_colors[i] = c

#for i in range(-27,27+28):
#	Day_colors[i] = np.mod(i,28)



def fr(pr,today,past_days,future_days):
	clear_screen()
	past_days *= -1
	pday_int = (pr-today).days
	#cr('pday_int =',pday_int)
	for i in range(past_days,future_days):

		day = i*one_day+today

		#print day
		j = np.mod(i-pday_int,28)
		#print day,j,Day_colors[j]

		#,colored(d2s((day-today).days,'days'),'white')
		day_count = (day-today).days
		attrs=[]
		
		show_today = ''
		if day_count == 0:
			today_attrs = attrs
			attrs.append('underline')
			show_today = 'today'
		else:
			today_attrs = []
		show_mine = ''
		mine = my_day_pattern[np.mod(i+(today-ref_day).days,14)]
		if mine:
			#show_mine = '*'
			attrs=['bold','reverse']
		print colored(d2n(show_mine,Days[day.weekday()],' ',day.month,'/',day.day,' '),Day_colors[j],attrs=attrs),colored(d2s(day_count,show_today),'white',attrs=today_attrs)

	print('\n\n')



fr(pr,today,Arguments['p'],Arguments['f'])


if 'wait' in Arguments:
	if Arguments['wait']:
		raw_enter()


#EOF