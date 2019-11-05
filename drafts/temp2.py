


def kprint(item,title=None):
    item_printed = False
    if title != None:
        print('')
        if type(item) in [dict,list]:
            len_item = len(item)
            color_print(title,' (n=',len_item,')','`-g')  #o='g',s='') 
        else:
            color_print(title,':','`-g',' ','`',item,'`g' )
            item_printed = True
        
    if type(item) == list:
        for i in item:
        	color_print(i,'`b')
    elif type(item) == dict:
        for k in sorted(item.keys()):
            if type(item[k]) in [dict,list]:
                l = len(item[k])
            else:
                l = 1
            color_print(k,' {n=',l,'}','`y')
    elif not item_printed:
        color_print(i,'`g')


def color_print(*args):
	B = _color_define_list(args)
	c = []
	for i in sorted(B.keys()):
		if len(B[i]['data']) > 0:
			if len(B[i]['colors']) > 0:
				c.append(colored(
					d2n(*B[i]['data']),
					B[i]['colors'][0],
					B[i]['colors'][1],
					B[i]['colors'][2]),
				)
			else:
				c.append(colored(*B[i]['data']))
	#print c
	pd2n(*c)

def _color_define_list(a):
	B = {}
	ctr = 0
	B[ctr] = {}
	B[ctr]['data'] = []
	B[ctr]['colors'] = None
	for c in a:
		if type(c) == str:
			if c[0]=='`':
				B[ctr]['colors'] = _translate_color_string(c[1:])
				ctr += 1
				B[ctr] = {}
				B[ctr]['data'] = []
				B[ctr]['colors'] = None
				continue
		B[ctr]['data'].append(c)
	for i in B.keys():
		if len(B[i]['data']) == 0:
			del B[i]
	return B


def _translate_color_string(s):
	color,on_color,attrs = None,None,None
	Translate_color = {
		'g':'green',
		'b':'blue',
		'w':'white',
		'y':'yellow',
		'-':None,
	}
	Translate_on_color = {
		'g':'on_green',
		'b':'on_blue',
		'w':'on_white',
		'y':'on_yellow',
		'-':None,
	}
	Translate_attribute = {
		'b':'bold',
		'u':'underline',
		'-':None,
	}
	if len(s) > 0:
		color = Translate_color[s[0]]
	if len(s) > 1:
		on_color = Translate_on_color[s[1]]
	if len(s) > 2:
		attrs = []
		for i in range(2,len(s)):
			attrs.append(Translate_attribute[s[i]])
	if attrs != None:
		attrs = list(set(attrs))
		if attrs[0] == None:
			attrs = None
	return color,on_color,attrs

if False:
	kprint([12,3,3],title='aa')
	kprint({1:2,3:4},title='aa')
	kprint(1,title='aa')




bash_history = txt_file_to_list_of_strings(opjh('.bash_history'))
H = {}
Open = {}
for bh in bash_history:
	h = bh
	if len(h) < 1:
		continue
	while h[-1] in [' ','\t']:
		h = h[:-1]
	l = h.split(' ')
	command = l[0]
	if command not in H:
		H[command] = []
	H[command].append(h)
	H[command] = list(set(H[command]))
	Open[command] = False
Open['python'] = True
#Open['history'] = True
#special = ['python','diff']
#hide = ['gacp','et','more','mkdir','mv','pgacp','pgp','bk3','cd']
show = ['python','grep','ls','diff']

while True:
	if True:#try:
		clear_screen()
		print 
		sorted_H_keys = sorted(H.keys())
		line_list = []
		hide = []
		for command in sorted_H_keys:
			if command not in show:
				hide.append(command)
				continue

			if Open[command]:
				line_list.append((command,'-'))
				#print(line_list[-1])
				sorted_commands = sorted(H[command])
				for c in sorted_commands:
					line_list.append((c,'line'))
					#print(line_list[-1])
			else:
				line_list.append((command,'+'))
				#print(line_list[-1])

		hide = list(set(hide))
		try:
			hide.remove('')
		except:
			pass
		clp('Hidden:','`',', '.join(hide),'`b')
		for i in rlen(line_list):
			a = line_list[i]
			if len(a[0]) < 1:
				continue
			assert type(a) == tuple
			assert len(a) == 2
			p = cf(i,')',s0='')
			if a[1] == 'line':
				s = cf('\t',a[0],'`y',s0='',s1='')
			else:
				#if a[0] in special:
				#	p = cf(i,')','`--r',s0='')
				if a[1] == '+':
					s = cf(a[0],'+','`g')
				elif a[1] == '-':
					s = cf(a[0],'-','`r-b')

			clp(p,s,s0=' ')

		b = raw_input(cf("Enter number or 'q' to quit --> ",'`m'))
		if b == 'q':
			break
		elif b[0] == '+':
			show.append(b[1:])
			Open[b[1:]] = True
		elif b[0] == '-':
			show.remove(b[1:])
		if not str_is_int(b):
			continue
		n = int(b)
		a = line_list[n]
		if a[1] == '-':
			Open[a[0]] = False
		elif a[1] == '+':
			Open[a[0]] = True
		elif a[1] == 'line':
			qu = cf('Do','`',a[0],'`rwb','[y]/n ? ')
			try:
				pyperclip.copy(a[0])
				cy("In clipboard:","'"+a[0]+"'")
			except:
				cr('cannot copy to clipboard becaue do not have pyperclip')
			u = raw_input(qu)
			if u in ['','y']:
				os.system(a[0])
				raw_enter()
	"""
	except KeyboardInterrupt:
	    cr('*** KeyboardInterrupt ***')
	    sys.exit()
	except Exception as e:
	    exc_type, exc_obj, exc_tb = sys.exc_info()
	    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	    CS_('Exception!',emphasis=True)
	    CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
	    raw_enter()
	"""











A=lo(opjD('Data/Network_Predictions/tegra-ubuntu_30Dec18_15h14m21s.net_predictions.pkl'))
B=lo('/data/dataset/karl/Disk1/Data_1/Network_Predictions/tegra-ubuntu_30Dec18_15h14m21s.net_predictions.pkl')




#,a
roscore &

python kzpy3/scripts/ros/publish_preprocessed_data.py  --pub_predictions 0 --step 0 --initial_index 10000

rosplay_menu.py

python kzpy3/Menu_app/menu2.py --path kzpy3/Cars/a2Apr19/nodes --dic P
8,12,-1,8,10

python kzpy3/Cars/a2Apr19/nodes/network_node.py desktop_mode 1


python kzpy3/VT_net2__5April2019_2__18April2019_for_speed/main.py




#################
roscore &


python kzpy3/scripts/ros/publish_preprocessed_data.py  --pub_predictions 0 --step 0 --initial_index 10000

rosplay_menu.py


#python kzpy3/Menu_app/menu2.py --path kzpy3/Cars/j26June2019__/nodes --dic P
python kzpy3/Menu_app/menu2.py --path kzpy3/Cars/j26June2019_rgb_v1/nodes --dic P
# 8,12,-1,8,10

#python kzpy3/Cars/j26June2019__/nodes/network_node.py desktop_mode 1
python kzpy3/Cars/j26June2019_rgb_v1/nodes/network_node.py desktop_mode 1

python kzpy3/VT_net2__5April2019_2__18April2019_for_speed/main.py
#,b


#EOF
