from kzpy3.utils2 import *
pythonpaths(['kzpy3'])

if len(Command_line_arguments) == 0:
	Command_line_arguments = {'--src':opjD(), '--dst':opjh()}

print(Command_line_arguments)
zdprint('dic',Command_line_arguments)