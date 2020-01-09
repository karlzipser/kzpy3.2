
exec_str = """

from kzpy3.utils3 import *

import Menu.main

M = Menu.main.start_Dic(dic_project_path=pname(opjh(__file__)))

time.sleep(1)

M['load']()


import default_args


requirements_satisfied = True
kprint(default_args.Default_Arguments,'Default arguments')
for a in required_arguments:
    if a not in Arguments or len(Arguments.keys()) == 0:
        requirements_satisfied = False
        clp('ERROR!!! Argument',"'"+a+"'",'is required','`wrb')
if not requirements_satisfied:
    sys.exit()

if len(required_arguments) > 0:
	key_arg = Arguments[required_arguments[0]]
else:
	key_arg = 'KEY_ARG'

setup_Default_Arguments(
    default_args.Default_Arguments[key_arg]#Arguments['NET_TYPE']]
)

"""
#    default_args.Default_Arguments[Arguments[required_arguments[0]]]#Arguments['NET_TYPE']]

#EOF
