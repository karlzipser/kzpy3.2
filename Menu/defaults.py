from kzpy3.utils3 import *

Q = {
    '--mode--':'extern',
}

data = find_files_recursively(opjk(),'defaults.py',FILES_ONLY=True,ignore_underscore=True) 
for d in data['paths'].keys():
    Q[d] = opjk(d)

"""
ignore_list = []#['Menu']

items = sggo(opjk('*'))
for m in items:
    if fname(m)[0] == '_':
        continue
    if fname(m) in ignore_list:
        continue
    if len(sggo(m,'defaults.py')) == 1:
        Q[fname(m)] = m

items = sggo(opjk('Cars/*'))
for m in items:
    if fname(m)[0] == '_':
        continue
    if fname(m) in ignore_list:
        continue
    n = opj(m,'nodes')
    if len(sggo(n,'defaults.py')) == 1:
        Q[opj('Cars',fname(m))] = n
"""






#EOF
