from kzpy3.vis3 import *
import Menu.main

Q = Menu.main.start_Dic(
    dic_project_path=pname(opjk()), # i.e., use ~/kzpy3/defaults.py for data
    Arguments={
        'menu':False,
        'read_only':True,
    }
)
Q['load']()
T = Q['Q']

raw_enter('from command line: ~/kzpy3/Menu/main.py --path ~/kzpy3/')

def sample_use_of_menu_data():

    while True:

        time.sleep(0.1)

        loaded = Q['load']()

        if loaded:
            print(time.time())
            pprint(T['State'])


if __name__ == '__main__':
    sample_use_of_menu_data()


#EOF
