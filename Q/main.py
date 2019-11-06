from kzpy3.vis3 import *
import_path = opjk('Q')
as_import = ['fsm','examples']
for a in as_import:
    exec_str = d2s('import',import_path.replace(opjh(),'').replace('/','.')+'.'+a,'as',a)
    exec(exec_str)
import kzpy3.Menu.main
Q = kzpy3.Menu.main.start_Dic(
    dic_project_path=import_path, 
    Arguments={
        'menu':False,
        'read_only':True,
    }
)

if __name__ == '__main__':

    S = examples.Subway()

    N = fsm.Net(
        Network_layout=S['Network_layout'],
        start=S['start'],
    )
     
    fsm.eg_run(N,S['Environment'](),Q)


        
#EOF
