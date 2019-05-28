from kzpy3.utils3 import *


def normal_dic_to_dic_in_Command_form(D):
    for d in D.keys():
        if type(D[d]) == dict:
            normal_dic_to_dic_in_Command_form(D[d])
        else:
            D[d] = ('set value',D[d])


def dic_in_Command_form_to_normal_dic(D):
	for d in D.keys():
		if type(D[d]) == dict:
			dic_in_Command_form_to_normal_dic(D[d])
		else:
			e = D[d]
			assert e[0] in ['set value','const']
			assert len(e) > 1
			D[d] = e[1]



Q = {'a':1,'b':2,'c':3,'d':{'e':4,'f':5,'d':{'e':4,'f':5}}}


cy(Q)
normal_dic_to_dic_in_Command_form(Q)
cg(Q)
dic_in_Command_form_to_normal_dic(Q)
cb(Q)
