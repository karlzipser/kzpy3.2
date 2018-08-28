from kzpy3.utils3 import *
import kzpy3.Menu_app.menu
import kzpy3.Train_app.Train_Z1dconvnet0.default_values as default_values

P = default_values.P
menu_path = P['The menu path.']
unix('mkdir -p '+menu_path)
unix(d2s('rm',opj(menu_path,'ready')))
kzpy3.Menu_app.menu.save_topics(P,P['The menu path.'])
unix(d2s('touch',opj(menu_path,'ready')))
threading.Thread(target=kzpy3.Menu_app.menu.load_menu_data,args=[menu_path,P]).start()

