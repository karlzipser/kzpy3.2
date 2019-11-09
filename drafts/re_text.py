from kzpy3.utils3 import *

#,a
regex = r'\w*def ([a-zA-Z0-9_]+)\('


code = txt_file_to_list_of_strings(opjk('utils.common.py'))

e=r'^.+@[^.].*\.[a-z]{2,10}$'
e=r'[a-zA-Z][a-zA-Z0-9_]+@[^.].*\.[a-z]{2,10}$'
e=r'[a-zA-Z]+[a-zA-Z0-9_]*@[^.].*\.[a-z]{2,10}$'
re.match(e,'a@b.co')

functions = []
ctr = 0
for line in code:
    ctr += 1
    result = re.findall(regex,line)
    if len(result) > 0:
        functions.append(result[0])
        #cg(ctr,result[0],sf=0)
        cg(ctr,line,sf=0)

Regexs = {}
for f in functions:
    Regexs[f] = r'\W*'+f+r'\('

Functions_used = {}

for f in functions:
    Functions_used[f] = {'count':0,'lines':{}}

path_ignore_list=[opjk('utils')]
file_ignore_list=['utils3','utils2']

def visit(path):
    print path
    for i in path_ignore_list:
        if i in path:
            cg('ignoring',path)
            return
    tmp = path
    if tmp[-1] == '/':
        tmp = tmp[:-1]
    if fname(tmp)[0] == '_':
        cb('ignoring',path)
        return
    files = sggo(path,'*')
    for f in files:
        ignoring_f = False
        if os.path.isdir(f):
            visit(f)
        elif f[-3:] == '.py':
            for i in file_ignore_list:
                if i in f:
                    cb('ignoring',f)
                    ignoring_f = True
                    break
            if ignoring_f:
                continue 
            code = txt_file_to_list_of_strings(f)
            for line in code:
                for fun in functions:
                    result = re.findall(Regexs[fun],line)
                    if len(result) > 0:
                        #print result
                        Functions_used[fun]['count'] += 1
                        if line not in Functions_used[fun]['lines']:
                            Functions_used[fun]['lines'][line] = {'files':[]}
                        Functions_used[fun]['lines'][line]['files'].append(f)

visit(opjk())

if False: 
    raw_enter()
    import operator
    sorted_Functions_used = \
        sorted(Functions_used.items(), key=operator.itemgetter(1))

    for f in sorted_Functions_used:
        pd2s(f[0],'\t\t',f[1])

C = {}
for f in sorted(Functions_used.keys()):
    C[f] = len(Functions_used[f]['lines'])
    #print f,len(Functions_used[f]['lines'])

import operator
sorted_C = \
    sorted(C.items(), key=operator.itemgetter(1))
for s in sorted_C:
    count = s[1]
    name = s[0]
    pd2s(count,'\t',name)
soL(
    opjD('Function_use_analysis'),
    {
        'functions':functions,
        'Functions_used':Functions_used,
        'sorted_C':sorted_C,
    },
)
#,b
#EOF