from kzpy3.utils3 import *
import kzpy3.Menu_app.menu

#  python kzpy3/Menu_app/menu.py path kzpy3/Cars/car_24July2018/nodes/Default_values/arduino dic Parameters


############# start menu thread ############
#
__default_values_module_name__ = "kzpy3.Cars.car_24July2018.nodes.Default_values.arduino.default_values"
__topics_dic_name__ = "Parameters"
exec(kzpy3.Menu_app.menu.__MENU_THREAD_EXEC_STR__.replace(
	'__default_values_module_name__',__default_values_module_name__
	).replace('__topics_dic_name__',__topics_dic_name__))
#
############################################


timer = Timer(5)
while Parameters['ABORT'] == False:
    #q = raw_input()
    #if q == 'q':
    #    Parameters['ABORT'] = True
    timer.message(d2s('time.time()',time.time()))
raw_enter('Done. ')

#EOF
