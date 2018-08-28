from kzpy3.utils3 import *
from kzpy3.Menu_app.menu import *
import kzpy3.Train_app.Train_Z1dconvnet0.default_values as default_values

Topics = {}
menu_path = False
if Arguments['node'] == 'nothing':
	pass
elif Arguments['node'] == 'net':
	D = default_values.P
	menu_path = D['The menu path.']
else:
	assert(False)
print D
for name in D['to_expose']:
	Topics[name] = D[name]

if menu_path:
	menu(Topics,menu_path)
else:
	print('Invalid argument: '+Arguments)



#EOF
