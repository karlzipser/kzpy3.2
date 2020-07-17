#!/usr/bin/env python
#,a
from kzpy3.utils3 import *



try:
	lst = lo(opjD('multiclip.pkl'))
except:
	lst = []

#lst = []

E = {'Command':None,'noisy':True}

def clipthread():

	print_lst()

	while True:
		#print '.'
		if E['Command'] == 'quit':
			cg('quitting clipthread()')
			return 0

		c = getClipboardData()

		found = False
		for l in lst:
			if c == l[0]:
				found = True

		if found:
			time.sleep(0.2)

		else:
			

			s = time_str('Pretty2')
			lst.append( [c,s] )

			print_lst()

			so(lst,opjD('multiclip.pkl'),noisy=E['noisy'])
			E['noisy'] = False

		
def print_lst():
	clear_screen()
	for i in rlen(lst):
		m = min(len(lst[i][0]),100)
		a = lst[i][0][:m]
		b = a.split('\n')
		c = []
		for d in b:
			if len(d) > 0:
				c.append(d)
		clp(str(i)+')','`--b',lst[i][1],'`--d','\n'+'\n'.join(c),'`wbb')
		if m < len(lst[i][0]):
			clp('...','`gbb')


threading.Thread(target=clipthread).start()

while True:
	q = raw_input('-->')
	r = q.split(' ')
	if str_is_int(r[0]):
		setClipboardData(lst[int(r[0])][0])
		clp('set clipboard to:\n','`',lst[int(r[0])][0])
	elif r[0] == 'q':
		E['Command'] = 'quit'
		break#return 0
	elif r[0] == 'r':
		u = 0
		if len(r) == 3:
			u  = int(r[2]) + 1
		elif len(r) == 2:
			u = int(r[1])+1
		if u:
			for v in range(int(r[1]),u):
				lst.pop(int(r[1]))
			so(lst,opjD('multiclip.pkl'),noisy=E['noisy'])
			print_lst()


#,b
#EOF

