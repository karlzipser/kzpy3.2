from kzpy3.utils2 import *
exec(identify_file_str)

for _name in [
	'menu_dic'
	]:exec(d2n(_name,'=',"'",_name,"'"))

#

#EOF

_ = dictionary_access


def menu(*args):
    Args = args_to_dictionary(args)
    True
    menu_strv = 'echo \"menu\"\n'
    sorted_keysv = sorted(Args[menu_dic].keys())
    menu_strv += "OPTIONS=\""
    for sv in sorted_keysv:
    	menu_strv += sv
    	if sv != sorted_keysv[-1]:
    		menu_strv += " "
    menu_strv += '\"\nCOLUMNS=12\nselect opt in $OPTIONS; do\n'
    ctr = 0
    for sv in sorted_keysv:
    	if ctr == 0:
    		menu_strv+='  if'
    	else:
    		menu_strv+='  elif'
    	ctr += 1
    	menu_strv+=' [ \"$opt\" = \"'+sv+'\" ]; then\n'
    	menu_strv+= '      '+Args[menu_dic][sv]+'\n'
    menu_strv += "   fi\ndone\n"
    print menu_strv


menu(menu_dic,{'ls':"echo 'ls'\nls ", 'B':"echo 'B'\n\t\tcd kzpy3\n\t\tgit pull "})
