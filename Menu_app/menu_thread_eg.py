from kzpy3.utils3 import *

#  python kzpy3/Menu_app/menu.py path kzpy3/Cars/car_24July2018/nodes/Default_values/arduino dic Parameters


############# start menu thread ############
#
import kzpy3.Menu_app.menu
__default_values_module_name__ = "kzpy3.Menu_app.default_values"
__topics_dic_name__ = "M"
exec(kzpy3.Menu_app.menu.__MENU_THREAD_EXEC_STR__.replace(
	'__default_values_module_name__',__default_values_module_name__
	).replace('__topics_dic_name__',__topics_dic_name__))
#
############################################


timer = Timer(5)
while M['ABORT'] == False:
	timer.message(d2s(M['a/a']))


#EOF
