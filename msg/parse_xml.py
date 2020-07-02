


#,a

import xmltodict
from json import loads, dumps
from datetime import datetime
from kzpy3.utils3 import *


def parse(fname):

	with open(opjD(fname+'.xml')) as fd:
	    c = xmltodict.parse(fd.read())

	d = c['plist']['dict']['array']['dict']

	p = -1
	t = 0

	assert c['plist']['dict']['array']['string'][4][:2] == 'E:'
	if c['plist']['dict']['array']['string'][5][0] == '+':
		I_start = False
	else:
		I_start = True

	timestamps = []
	mes = []
	texts = []

	for i in rlen(d):
		e = loads(dumps(d[i]))
		if 'dict' in e:
			if 'key' in e and 'real' in e:
				if 'integer' in e['dict']:
					if e['dict']['integer'] == '15' and 'NS.time' in e['key']:

						timestamps.append(float(e['real']))

					else:
						pass


			if 'key' in e:
				if 'Subject' in e['key']:

					p = int(e['dict'][-3]['integer'])

				else:
					pass

			if 'integer' in e['dict'] and 'string' in e:

				if e['dict']['integer'] == '18':

					if p == 6:
						if I_start:
							me = True
						else:
							me = False
					elif p == 11:
						if not I_start:
							me = True
						else:
							me = False
					else:
						assert False

					mes.append(me)
					texts.append(e['string'])
				else:
					pass

	phone = texts[-1]
	lst = []
	T = {}
	for i in rlen(timestamps):
		lst.append({timestamps[i]:{'me':mes[i],'text':texts[i]}})
		T[timestamps[i]] = {'me':mes[i],'text':texts[i]}
	R = {
		'phone':phone,
		'texts':T,
	}
	R2 = {
		phone:T,
	}
	return R

fname = 'f'
pprint(parse(fname))
#pprint(R)
#pprint(R2)



#,b