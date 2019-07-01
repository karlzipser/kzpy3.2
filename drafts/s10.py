if False:
	M = {
		'text':'Warning, meltdown in progress!',
		'period': 5,
		'till': 151239,
		'filename':'m293.py'
	}
	say(M['text'])

	Ms = {
		M['text']:M
	}


	def key_access(Dic,keys,start=True):
	    if start:
	        keys_copy = []
	        for k in Dic['current_keys']:
	            keys_copy.append(k)
	        keys = keys_copy
	    key = keys.pop(0)
	    assert key in Dic.keys()
	    if type(Dic[key]) == dict and len(keys) > 0:
	        return key_access(Dic[key],keys,start=False)
	    else:
	        return Dic[key]



def key_get_set(D,key_list,value=None):
	key = key_list.pop(0)
	assert key in D.keys()
	if len(key_list) == 0:
		if value != None:
			D[key] = value
			return value
		else:
			return D[key]
	else:
		return key_get_set(D[key],key_list,value)
kg = key_get_set
if False:
	Q = {1:{2:{3:4}}}
	print Q
	print kg(Q,[1,2,3])
	print Q
	print kg(Q,[1,2,3],{5:6})
	print Q

#EOF