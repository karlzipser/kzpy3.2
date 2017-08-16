




def zp(d,depth,range_lst):#,max_depth_lst):

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
				zp(value,depth+1,range_lst[1:])#,max_depth_lst[1:])
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
d['b']['B1']['b1'] = ['C']
d['b']['B2'] = 'b2'
d['c'] = 'C'


zp(d,0,[[1,2],[0,0]])
print('')
zp(d,0,[[0,3]])
print('')
zp(d,0,[1,-2])
print('')
zp(d,0,[1,-1])

