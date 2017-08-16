from kzpy3.utils2 import *
pythonpaths(['kzpy3'])
from vis2 import *


if len(Command_line_arguments) == 0:
    Command_line_arguments = {'--src':opjD(), '--dst':opjh()}


print(Command_line_arguments)
#zdprint('dic',Command_line_arguments)


for _name in ['dic','name','test','dic_type','purpose']:exec(d2n(_name,'=',"'",_name,"'"))


G = {}



for _name in ['first','second']:exec(d2n(_name,'=',"'",_name,"'"))
def fun1(*args):
    keys = [first,[second,2]]
    exec(dic_exec_str)
    if True:
        print(da(Args,first)-da(Args,second))
        pd2s(name,'=',da(Args,name))
        pd2s('dic_2','=',da(Args,dic,2))
        da(Args,dic,2,equals,22)
        da(Args,second,equals,{1:2,3:4,5:6})
        pd2s('dic_2','=',da(Args,dic,2))
        zdprint(dic,Args)
    return Args




fun1(dic,{1:2,2:3} ,name,Command_line_arguments['--src'] ,first,10 ,second,100)



for _name in ['fun2']:exec(d2n(_name,'=',"'",_name,"'"))

def Dic_Blank(*args):
    keys = [first,[second,2]]
    exec(dic_exec_str)
    D = {}
    D[first] = Args[first]
    D[second] = Args[second]
    if True:
        D[dic_type] = 'Dic_Blank'
        D[purpose] = d2s(inspect.stack()[0][3],':','Test out new thing')    
        D[fun2] = _fun2
    return D
if True:
    def _fun2(*args):
        keys = [first,[second,2]]
        exec(dic_exec_str)
        if True:
            print(da(Args,first)-da(Args,second))
            pd2s(name,'=',da(Args,name))
            pd2s('dic_2','=',da(Args,dic,2))
            da(Args,dic,2,equals,22)
            da(Args,second,equals,{1:2,3:4,5:6})
            pd2s('dic_2','=',da(Args,dic,2))
            zdprint(dic,Args)
        return Args

DB = Dic_Blank(first,10)
zdprint(dic,DB)
da(DB,fun2)(first,3 ,second,200)
DB[fun2](first,3 ,second,200)
da(DB,fun2,equals,"Now a string, now a function")
zdprint(dic,DB)





#EOF