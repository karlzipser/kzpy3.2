#,a


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


#,b


#EOF
