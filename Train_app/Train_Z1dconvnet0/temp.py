###start
from kzpy3.utils3 import *

import default_values

Parameters = default_values.Parameters

import kzpy3.Menu_app.menu
menu_path = Parameters['The menu path.']
unix('mkdir -p '+menu_path)
unix(d2s('rm',opj(menu_path,'ready')))
threading.Thread(target=kzpy3.Menu_app.menu.load_menu_data,args=[menu_path,Parameters]).start()


while P['ABORT'] == False:
	print memory()
	time.sleep(1)

#EOF