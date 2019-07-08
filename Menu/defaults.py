from kzpy3.utils3 import *

Q = {
    'defaults.py': {
        '--mode--':'extern',
    },
    'main.py': {
        '--mode--':'bash',
    },
    'scripts': {
        '--mode--':'bash',
    },
}

data = find_files_recursively(opjk(),'defaults.py',FILES_ONLY=True,ignore_underscore=True) 
for d in data['paths'].keys():
    Q['defaults.py'][d] = opjk(d)

data = find_files_recursively(opjk(),'main.py',FILES_ONLY=True,ignore_underscore=True) 
for d in data['paths'].keys():
    Q['main.py'][d] = 'python '+opjk(d,'main.py')

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
