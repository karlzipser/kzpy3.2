from kzpy3.utils.common import *



def get_safe_name(name):
    lst = []
    for i in range(len(name)):
        if name[i].isalnum():
            lst.append(name[i])
        else:
            lst.append('_')
    return "".join(lst)
    

def num_from_str(s):
    try:
        return int(s)
    except:
        try:
            return float(s)
        except:
            return 'String does not represent a number.'

def str_contains(st,str_list):
    for s in str_list:
        if not s in st:
            return False
    return True
    
def str_contains_one(st,str_list):
    for s in str_list:
        if s in st:
            return True
    return False

            
#exec(identify_file_str)

#EOF
