
exec_str = """

from kzpy3.utils3 import *

import Menu.main

M = Menu.main.start_Dic(dic_project_path=pname(opjh(__file__)))

time.sleep(1)

M['load']()


import default_args


requirements_satisfied = True
kprint(default_args.Default_Arguments,'Default arguments')

if 'required_arguments' in locals():
	for a in required_arguments:
	    if a not in Arguments or len(Arguments.keys()) == 0:
	        requirements_satisfied = False
	        clp('ERROR!!! Argument',"'"+a+"'",'is required','`wrb')
	if not requirements_satisfied:
	    sys.exit()


just_Defaults = False

if 'required_arguments' not in locals() or len(required_arguments) == 0:
	if 'KEY_ARG' in locals():
		key_arg = KEY_ARG
	else:
		just_Defaults = True
else:
	key_arg = Arguments[required_arguments[0]]

if just_Defaults:
	setup_Default_Arguments(
	    default_args.Default_Arguments
	)
else:
	setup_Default_Arguments(
	    default_args.Default_Arguments[key_arg]
	)
"""
#    default_args.Default_Arguments[Arguments[required_arguments[0]]]#Arguments['NET_TYPE']]

#EOF
