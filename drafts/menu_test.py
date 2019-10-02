from kzpy3.vis3 import *
import Menu.main

Q = Menu.main.start_Dic(
    dic_project_path=pname(opjk()),
    Arguments={
        'menu':False,
        'read_only':True,
    }
)
Q['load']()
T = Q['Q']
pprint(Q)



def abc():

    while True:

        time.sleep(0.1)

        loaded = Q['load']()

        if loaded:
            print(time.time())
            pprint(T['State'])


if __name__ == '__main__':
    abc()


#EOF
