from kzpy3.vis3 import *
import kzpy3.Menu.Menu as Menu

Q = Menu.start_Dic(
    dic_project_path=opjk('Menu','A'),
    Dics={},
    load_timer_time=5,
    Arguments={
        'menu':False,
        'read_only':False,
    }
)

while True:
    Q['load']()
    cg(Q['Q']['tests']['a'],Q['Q']['tests']['b'],ra=1,sf=0)

#EOF
