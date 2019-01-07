####################### IMPORT ################################
from kzpy3.utils3 import *
import kzpy3.Menu_app.menu2 as menu2
import default_values
cr(__file__)
cr(pname(__file__))
project_path = pname(__file__).replace(opjh(),'')
if project_path[0] == '/':
    project_path = project_path[1:]
sys_str = d2s('mkdir -p',opj(project_path,'__local__'))
cg(sys_str)
os.system(sys_str)
cg("To start menu:\n\tpython kzpy3/Menu_app/menu2.py path",project_path,"dic _")

exec(identify_file_str)
_ = default_values._
#
##############################################################

####################### MENU ################################
#
if _['start menu automatically'] and using_linux():
    dic_name = "_"
    sys_str = d2n("gnome-terminal --geometry 150x30+10+10 -x python kzpy3/Menu_app/menu2.py path ",project_path," dic ",dic_name)
    cr(sys_str)
    os.system(sys_str)

parameter_file_load_timer = Timer(_['load_timer_time'])


def load_parameters(_,customer):
    assert customer in _['customers']
    if parameter_file_load_timer.check():
        #cy("Topics = menu2.load_Topics(",project_path,",first_load=False,customer=",customer)
        Topics = menu2.load_Topics(project_path,first_load=False,customer=customer)
        if type(Topics) == dict:
            for t in Topics['To Expose'][customer]:
                _[t] = Topics[t]
                if '(click)' in t and Topics[t]:
                    cr(t.replace('(click)',''))
                    sys_str = d2n("gnome-terminal --geometry 40x30+100+200 -x "+t.replace('(click)',''))
                    cr(sys_str)
                    os.system(sys_str)
        parameter_file_load_timer.reset()
#
##############################################################

##############################################################
#



if __name__ == '__main__':
    while not _['ABORT']:

        ##########################################################
        #
        load_parameters(_,'command_menu')
        parameter_file_load_timer.trigger()
        load_parameters(_,'M')
        #
        ##########################################################

        time.sleep(1)



cg('\n\nDone.\n')
#EOF
