from Parameters import *
exec(identify_file_str)
import Data

for a in Command_line_arguments.keys():
    P[a] = Command_line_arguments[a]

DD=Data.Data()

zdprint(dic,P)
#zdprint(dic,Command_line_arguments) # bug, len of dic must be greater than 1
"""
DB = Dic_Blank(first,10)
zdprint(dic,DB)
da(DB,fun2)(first,3 ,second,200)
DB[fun2](first,3 ,second,200)
da(DB,fun2,equals,"Now a string, now a function")
zdprint(dic,DB)
"""




#EOF