from kzpy3.utils2 import *
from kzpy3.Menu_app.menu import *
import kzpy3.Cars.car_24July2018.nodes.default_values as default_values

Topics = {}
menu_path = False
if Arguments['NODE'] == 'network':
	menu_path = opjh('.menu','network_node')
	D = default_values.Network
elif Arguments['NODE'] == 'arduino':
	menu_path = opjh('.menu','arduino_node')
	D = default_values.Parameters	
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
