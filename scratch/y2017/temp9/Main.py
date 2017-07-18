from Parameters import *
exec(identify_file_str)
from Dic_Blank import Dic_Blank

if len(Command_line_arguments) == 0:
    Command_line_arguments = {GPU:66, DISPLAY:False}

for a in Command_line_arguments.keys():
    P[a] = Command_line_arguments[a]


#zdprint(dic,P)
#zdprint(dic,Command_line_arguments) # bug, len of dic must be greater than 1

DB = Dic_Blank(first,10)
zdprint(dic,DB)
da(DB,fun2)(first,3 ,second,200)
DB[fun2](first,3 ,second,200)
da(DB,fun2,equals,"Now a string, now a function")
zdprint(dic,DB)





#EOF