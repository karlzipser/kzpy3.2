from kzpy3.vis3 import *
import Menu

dic_project_path = opjk('Menu','A')

Dics = {}

Q = Menu.start_Dic(
    dic_project_path=dic_project_path,
    Dics=Dics,
    Arguments={
        'menu':False,
        'read_only':False,
    }
)

P = Q['Q']

while True:
    Q['load']()
    cg(P['tests'],ra=1)

#EOF
