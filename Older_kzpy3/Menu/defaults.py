from kzpy3.utils3 import *

menus = 'menus'
run_options = 'run programs'
Q = {
    menus: {
        '--mode--':'extern',
    },
    run_options: {
        '--mode--':'bash',
    },
    'scripts': {
        '--mode--':'bash',
    },
    "ssh's": {
    	'--mode--':'bash',
    	'Mr_New 169.254.131.242':'ssh -X nvidia@169.254.131.242',
    	'Mr_Purple 169.254.131.243':'ssh -X nvidia@169.254.131.243',
    }
}

data = find_files_recursively(opjk(),'defaults.py',FILES_ONLY=True,ignore_underscore=True) 
for d in data['paths'].keys():
    Q[menus][d] = opjk(d)

data = find_files_recursively(opjk(),'main.py',FILES_ONLY=True,ignore_underscore=True) 
for d in data['paths'].keys():
    Q[run_options][d] = 'python '+opjk(d,'main.py')

dir_lst = [opjk('scripts')]
folders = sggo(opjk('scripts/*'))
for f in folders:
	if f[0] == '_':
		continue
	if os.path.isdir(f):
		dir_lst.append(f)

for d in dir_lst:
	py_files = sggo(opj(d,'*.py'))
	sh_files = sggo(opj(d,'*.sh'))
	files = py_files + sh_files
	for f in files:
		n = fname(f)
		if n[0] == '_':
			continue
		if '_older' in f:
			continue
		Q['scripts'][f.replace(opjk('scripts'),'')] = f
		os.system(d2s('chmod u+x',f))


#EOF
