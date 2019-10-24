def backup_folder(
	src=opjh('kzpy3'),
	dst=opjh('__kzpy3_older','kzpy3_'+time_str())+'/'
	):
	"""
	Make a time marked backup, with default as kzpy3.
	"""
    os.system('mkdir -p ' + dst)
    os.system(d2s('cp -r',src,dst))



from termcolor import colored

def c1(*args):
	s = d2s_spacer(args)
	return(colored(s,'blue','on_white',attrs=['dark','bold']))

def c2(*args):
	s = d2s_spacer(args)
	return(colored(s,'red','on_green',['bold']))

def c3(*args):
	s = d2s_spacer(args)
	return(colored(s,'green',attrs=[]))

def c4(*args):
	s = d2s_spacer(args)
	return(colored(s,'green',attrs=['bold']))

print(d2n( c2('a','b',1,[1,2]), c1('a','b',1,[1,2]) ))
print(d2n( c3('In ['),c4('7'),c3('7]:')))
print '\x1b[1m \x1b[42m \x1b[31ma b 1 [1, 2] \x1b[0m aa'
print '\x1b[1m \x1b[42m  b 1 [1, 2] \x1b[0m \x1b[31ma aa'
print 'test\x1b[0mtest'

_bold = '\x1b[1m'
_green = '\x1b[32m'
_sp = '\x1b[0m'
_ab = '\x1b[42m'
print d2n(_bold+_green,'asf adf adsf',_sp,'af','asf')


#,a
def cl(*args,**Kwargs):
	Translation = {
		'on_color': {
			'on_red':['on_red','red','r'],
			'on_green':['on_green','green','g'],
			'on_blue':['on_blue','blue','b'],
			'on_yellow':['on_yellow','on_yellow','y'],
			'on_white':['on_white','white','w'],
			'on_magenta':['on_magenta','magenta','m'],
			'on_blue':['on_blue','blue','b'],
			'on_yellow':['on_yellow','yellow','y'],
			'on_cyan':['on_cyan','cyan','c'],
			},
		'color': {
			'red':['red','r'],
			'on_green':['green','g'],
			'on_blue':['blue','b'],
			'yellow':['yellow','y'],
			'white':['white','w'],
			'magenta':['magenta','m'],
			'blue':['blue','b'],
			'yellow':['yellow','y'],
			'cyan':['cyan','c'],
			},
		'attrs': {
			'bold':['bold','b'],
			'underline':['underline','u'],
			'dark': ['dark','d'],
			'reverse': ['reverse','r']
			}
	}
	Defaults = {'c':None, 'o':None, 'a':None, 's':' '}
	for k in Kwargs.keys():
		if k not in Defaults.keys():
			cr("*** Warning, argument '"+k+"' not in expected arguments:\n\t",Defaults.keys())
	for k in Defaults.keys():
		if k not in Kwargs.keys():
			Kwargs[k] = Defaults[k]
	for c in Translation['color']:
		if Kwargs['c'] in Translation['color'][c]:
			Kwargs['c'] = c
			break
	for c in Translation['on_color']:
		if Kwargs['o'] in Translation['on_color'][c]:
			Kwargs['o'] = c
			break
	attributes = []
	if Kwargs['a'] != None:
		for a in Kwargs['a']:
			for c in Translation['attrs']:
				if a in Translation['attrs'][c]:
					attributes.append(c)
					break
		Kwargs['a'] = attributes
	s = colored(
		text=d2s_spacer(args,spacer=Kwargs['s']),
		color=Kwargs['c'],
		on_color=Kwargs['o'],
		attrs=Kwargs['a']
	)
	return s
#,b
#EOF
