#!/usr/bin/env python
#,a
from kzpy3.utils3 import *



save_dir = opjh('multiclip')

os.system('mkdir -p' + save_dir)

try:
	save_file = opj(save_dir,'multiclip.pkl')
	mtime = os.path.getmtime(save_file)
	timestamped_save_file = save_file.replace('.pkl','.'+str(int(mtime)))+'.pkl'
	os.system(d2s('cp',save_file,timestamped_save_file))
	lst = lo(save_file)
	just_text = []
	for l in lst:
		just_text.append(l[1])
		just_text.append(l[0])
		just_text.append('___\n')
	list_of_strings_to_txt_file(timestamped_save_file.replace('.pkl','.txt'),just_text)

	
except:
	lst = []

use_prefix_and_suffix = k_in_D('x',Arguments)

prefix = "Hi "
suffix = "! You seem like a fun and interesting person. It would be fascinating to get to know you. I'd love to hear more about your interests and passions."

E = {
	'Command':None,
	'noisy':False,
	'num_chars':100,
	'lst':lst,
	'pause_thread':False,
}

def clipthread():

	print_lst()

	while True:
		#print '.'
		if E['Command'] == 'quit':
			cg('quitting clipthread()')
			return 0
		if True:
			#cm(E['pause_thread'])
			if E['pause_thread']:
				E['thread_sleeping'] = True
				time.sleep(0.2)
				E['thread_sleeping'] = False
				return 0

		c = getClipboardData()

		

		if use_prefix_and_suffix and prefix not in c and suffix not in c:
			c = prefix + c + suffix
			setClipboardData(c)

		found = False
		for l in E['lst']:
			if c == l[0]:
				found = True

		if found:
			E['thread_sleeping'] = True
			time.sleep(0.2)
		else:
			E['thread_sleeping'] = False

			s = time_str('Pretty2')
			E['lst'].append( [c,s] )

			print_lst()

			so(E['lst'],save_file,noisy=E['noisy'])
			E['noisy'] = False

		
def print_lst():
	clear_screen()
	for i in rlen(E['lst']):
		m = min(len(E['lst'][i][0]),E['num_chars'])
		a = E['lst'][i][0][:m]
		b = a.split('\n')
		c = []
		for d in b:
			if len(d) > 0:
				c.append(d)
		clp(str(i)+')','`--b',E['lst'][i][1],'`--d','\n'+'\n'.join(c), '`-wb') #'`wbb')
		if m < len(E['lst'][i][0]):
			clp('...','`bwb')


threading.Thread(target=clipthread).start()

while True:
	if False:#not E['thread_sleeping']:
		continue
	try:
		istr =  '--> '

		if use_prefix_and_suffix:
			istr = 'X' + istr

		if E['pause_thread']:
			istr = 'P' + istr
		
			
		q = raw_input(istr)
		r = q.split(' ')
		if str_is_int(r[0]):
			setClipboardData(E['lst'][int(r[0])][0])
			clp('set clipboard to:\n','`',E['lst'][int(r[0])][0])
		elif r[0] == 'q':
			E['Command'] = 'quit'
			break
		elif r[0] == 'r':
			u = 0
			if len(r) == 3:
				u  = int(r[2]) + 1
			elif len(r) == 2:
				u = int(r[1])+1
			if u:
				for v in range(int(r[1]),u):
					E['lst'].pop(int(r[1]))
				so(E['lst'],save_file,noisy=E['noisy'])
				print_lst()
		elif r[0] == 'n':
			if int(r[1]) < 0:
				E['num_chars'] = 999999
			else:
				E['num_chars'] = int(r[1])
			print_lst()
		elif r[0] == 'l':
			files = sggo(save_dir,'*.pkl')
			for i in rlen(files):
				if '.pkl' in files[i]:
					clp(i,')',fname(files[i]))
			j = input('==>> ')
			E['lst'] = lo(files[j])
			print_lst()
		elif r[0] == 'x':
			if use_prefix_and_suffix:
				use_prefix_and_suffix = False
			else:
				use_prefix_and_suffix = True

		elif r[0] == 'p':
			E['pause_thread'] = not E['pause_thread']

	except KeyboardInterrupt:
	    cr('*** KeyboardInterrupt ***')
	    E['Command'] = 'quit'
	    time.sleep(0.3)
	    sys.exit()
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		CS_('Exception!',emphasis=True)
		CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)		

if False:
	a = [44,47,53,47,43,55,44,48,47,48,47,44,55,46,36,45,47,44,48,47,45,46,53,45,44]
	mx = 51
	mn = 38
	c = []
	for d in a:
		if d <= mx and d >= mn:
			c.append(d)
	hist(c)
	print np.median(c),np.mean(c)

#,b
#EOF

