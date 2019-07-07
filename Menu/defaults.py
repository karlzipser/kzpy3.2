from kzpy3.utils3 import *

Q = {
    'defaults.py': {
        '--mode--':'extern',
    },
    'main.py': {
        '--mode--':'bash',
    }
}

data = find_files_recursively(opjk(),'defaults.py',FILES_ONLY=True,ignore_underscore=True) 
for d in data['paths'].keys():
    Q['defaults.py'][d] = opjk(d)

data = find_files_recursively(opjk(),'main.py',FILES_ONLY=True,ignore_underscore=True) 
for d in data['paths'].keys():
    Q['main.py'][d] = 'python '+opjk(d,'main.py')

data = find_files_recursively(opjk(),'Main.py',FILES_ONLY=True,ignore_underscore=True) 
for d in data['paths'].keys():
    Q['main.py'][d] = 'python '+opjk(d,'Main.py')







#EOF
