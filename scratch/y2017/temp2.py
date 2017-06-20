




def zlist_str(lst):
	len_lst = len(lst)
	lst_str = "["
	for i in range(len_lst):
		if i < 2:
			lst_str += d2s(lst[i])
		if i < 1:
			lst_str += ','
		else:
			if len_lst > 2:
				lst_str += "... "
				break
			else:
				lst_str += "]"
				return lst_str
	if len_lst - 2 > 0:
		for i in range(len_lst-2,len_lst):
			lst_str += d2s(lst[i])
			if i < len_lst-1:
				lst_str += ','
	lst_str += "]"
	return lst_str



def zlst_truncate(lst,show_ends=2):
	if len(lst) > 2*show_ends:
		out_lst = lst[:2] + ['...'] + lst[-2:]
	else:
		out_lst = lst
	return out_lst

def zlst_to_str(lst,truncate=True,decimal_places=2):
	if truncate:
		lst = zlst_truncate(lst)
	lst_str = "["
	for i in range(len(lst)):
		e = lst[i]
		if type(e) == str:
			lst_str += e
		elif type(e) == int:
			lst_str += str(e)
		elif is_number(e):
			lst_str += str(dp(e,decimal_places))
		elif type(e) == list:
			lst_str += zlst_to_str(e)
		else:
			lst_str += '???'
		if i < len(lst)-1:
			lst_str += ' '
	lst_str += ']'
	return lst_str





def zp(d,range_lst,depth=0):

	sorted_keys = sorted(d.keys())
	
	this_range = range_lst[0]
	
	if type(this_range) == int:
		if this_range == -1:
			this_range = [0,len(sorted_keys)]
		elif this_range == -2:
			this_range = [0,len(sorted_keys)]
			range_lst = range_lst + [-2]
		else:
			this_range = [this_range,this_range+1]

	if this_range[0] > 0:
		cprint(d2n('\t'*depth,'0) ...'),'yellow')

	for i in range(this_range[0],this_range[1]):
		if i >= len(sorted_keys):
			return
		key = sorted_keys[i]
		value = d[key]

		cprint(d2n('\t'*depth,i,') ',key),'yellow')

		if isinstance(value,dict):
			#if max_depth_lst[0] > depth:
			if len(range_lst) > 1:
				zp(value,range_lst[1:],depth=depth+1)
			else:
				cprint(d2n('\t'*(depth+1),'...'),'yellow')
		else:
			cprint(d2s('\t'*(depth+1),str(value)),'green')

	if this_range[1] < len(sorted_keys):
		cprint(d2n('\t'*depth,'... ',len(d)-1,')'),'yellow')


d = {}
d['a'] = 'A'
d['b'] = {}
d['b']['B1'] = {}
d['b']['B1']['b1'] = 'b11'
d['b']['B2'] = 'b2'
d['c'] = 'C'


zp(d,[[1,2],[0,0]])
print('')
zp(d,[[0,3]])
print('')
alst = [0,0,0]
zp(d,alst)


def zaccess(d,alst):
	for a in alst:
		#print a,d
		if type(d) != dict:
			break
		d = d[sorted(d.keys())[a]]
	return d

v = zaccess(d,[1,0,0]);print v