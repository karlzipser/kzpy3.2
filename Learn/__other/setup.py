
exec_str = """

from kzpy3.utils3 import *

import Menu.main

M = Menu.main.start_Dic(dic_project_path=pname(opjh(__file__)))

time.sleep(1)

M['load']()



import other.default_args

requirements_satisfied = True
kprint(other.default_args.Default_Arguments,'Default arguments')
for a in required_arguments:
    if a not in Arguments or len(Arguments.keys()) == 0:
        requirements_satisfied = False
        clp('ERROR!!! Argument',"'"+a+"'",'is required','`wrb')
if not requirements_satisfied:
    sys.exit()


"""

#EOF
