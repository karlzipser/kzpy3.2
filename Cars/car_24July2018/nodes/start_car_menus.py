from kzpy3.utils3 import *
from kzpy3.Menu_app.menu import *

"""
e.g.
python kzpy3/Menu_app/menu.py path ~/kzpy3/Train_app/Train_Z1dconvnet0/__local__/arduino/ default 1 Topics arduino
python kzpy3/Menu_app/menu.py path ~/kzpy3/Train_app/Train_Z1dconvnet0/__local__/network/ default 1 Topics arduino
"""

if __name__ == '__main__':
    path = Arguments['path']
    if 'default' in Arguments.keys():
        import kzpy3.Cars.car_24July2018.nodes.default_values as default_values
        if 'Topics' in Arguments.keys():
            if Arguments['Topics'] == 'arduino':
                Topics = default_values.Parameters
            elsif Arguments['Topics'] == 'network':
                Topics = default_values.Network
            else:
                assert False
    else:
        try:
            Topics = load_Topics(path,first_load=True)
        except:
            Topics = {}
    menu(Topics,path)

#EOF
