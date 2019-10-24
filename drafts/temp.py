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

Originals = find_files_recursively(opjD('Data'),'original_timestamp_data.h5py')
so(opjD('Originals'),Originals)


from kzpy3.Data_app.classify_data import *
#top = opjD('h5py_have_already')
top = opjD('Older_version_of_h5py_runs')
H = find_files_recursively(top ,'original*')
for h in H['paths']:
    i = opj(top,h)
    r = fname(i)
    #cg(i,is_preprocessed_run(i),r)
    top2 = opjD('Data')
    P = find_files_recursively(top2,r)
    assert len(P['paths']) == 1
    A = P['paths']
    b = A.keys()[0]
    C = A[b][0]
    old_version_path = opj(top2,b,C)
    new_src = opj(top,h)
    new_dest = opj(top2,b)
    sys_str = d2s('mv',old_version_path,opjD('h5py_have_already'))
    cb(sys_str,ra=1)
    os.system(sys_str)

    sys_str = d2s('mv',new_src,new_dest)
    cy(sys_str,ra=1)
    os.system(sys_str)








train duration = 2 minutes   frequency = 0.01 Hz
tegra-ubuntu_01Dec18_16h38m21s lacks gyro_heading_x
-9243
Traceback (most recent call last):
  File "kzpy3/Train_app/Sq120_ldr_16chLIDAR_180deg/Main.py", line 116, in <module>
    Batch['FILL']()
  File "/home/karlzipser/kzpy3/Train_app/Sq120_ldr_16chLIDAR_180deg/Batch_Module.py", line 192, in _function_fill
    Data_moment = Data_Module.get_Data_moment(_,Network_Predictions,dm=dm,FLIP=FLIP)
  File "/home/karlzipser/kzpy3/Train_app/Sq120_ldr_16chLIDAR_180deg/Data_Module.py", line 384, in get_Data_moment
    Data_moment[q+past][:past_data_len] = _['Loaded_image_files'][dm['run_name']]['left_timestamp_metadata'][q][(left_index-past_data_len):left_index]
ValueError: could not broadcast input array from shape (0) into shape (69)






#EOF
