from kzpy3.utils3 import *


project_path = pname(__file__)
a = project_path.split('/')
c = []
for b in a:
	if len(b) > 0:
		c.append(b)
project_import_prefix = '.'.join(c)

module_name = 'default_values'

exec_str = d2s('import',project_import_prefix+'.'+module_name,'as',module_name)
exec(exec_str)
cr(exec_str)
cg(project_import_prefix)
cy(default_values.P['ABORT'])


#EOF
