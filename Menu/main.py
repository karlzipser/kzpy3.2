#!/usr/bin/env python

"""
to run from command line:

    ~/kzpy3/Menu/main.py

this opens the menu defined by:

    ~/kzpy3/Menu/defaults.py

Other menu paths can be specified, e.g.:

    ~/kzpy3/Menu/main.py --path ~/kzpy3/Grapher/

or

    ~/kzpy3/Menu/main.py --path ~/kzpy3/
    
"""

from kzpy3.vis3 import *
try:
    import colored
    have_colored = True
except:
    have_colored = False
exec(identify_file_str)
for k in CShowFile.keys():
    CShowFile[k] = False
if 'Arguments' not in locals():
    Arguments = {}
setup_Default_Arguments(
    {
        'menu': True,
        'read_only': False,
        'help': False,
        'path': 'kzpy3/Menu',
        #'start_keys':[],
        'load_timer_time':0.1,
    }
)



if False:
    # example
    import kzpy3.Menu.main as m
    DV = m.Default_Values
    A={'key 1':{'a':'x','b':'y'}}
    E = DV(A,opjD(),[])
    E['show']() 
    E['down']('key 1')
    E['show']()
    E['set_value']('a')
    E['show']()
    E['set_value']('a',value='qqq')
    E['show']()


def Default_Values(
    Q,
    project_path,
    parent_keys=[],
    read_only=False,
    Dics={},
    load_timer_time=0.1,
):
    D = {}
    os.system('mkdir -p '+opj(project_path,'__local__'))
    D['project_path'] = project_path
    D['.pkl'] = opj(project_path,'__local__','default_values.pkl')
    D['parent_keys'] = parent_keys
    D['current_keys'] = ['Q']
    D['Q'] = Q
    D['read_only'] = read_only
    D['Dics'] = Dics
    D['mtime_prev'] = -1
    D['load_timer'] = Timer(load_timer_time)
    def __add_keys(E,keys=[]):
        E['--keys--'] = keys
        if '--mode--' not in E:
            if D['read_only']:
                E['--mode--'] = 'const'
            else:
                E['--mode--'] = 'var'
        elif D['read_only'] and E['--mode--'] == 'var':
            E['--mode--'] = 'const'
        for k in E.keys():
            if type(E[k]) == dict:
                __add_keys(E[k],keys+[k])



    def __load_C(C,project_path,name='default_values'):
        if len(sggo(opj(project_path,'__local__','ready'))) == 0:
            return False
        if len(sggo(opj(project_path,'__local__',name+'.writing.pkl'))) > 0:
            return False
        if len(sggo(opj(project_path,'__local__',name+'.pkl'))) == 0:
            return False
        try:
            D = lo(opj(project_path,'__local__',name+'.pkl'),noisy=False)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
            return False
        if len(sggo(opj(project_path,'__local__','ready'))) == 0:
            return False
        if len(sggo(opj(project_path,'__local__',name+'.writing.pkl'))) > 0:
            return False
        if len(sggo(opj(project_path,'__local__',name+'.pkl'))) == 0:
            return False
        for k in C.keys():
            C[k] = D[k]

        return True

    def __save_C(C,project_path,name='default_values'):
        try:
            sys_str = d2s('rm',opj(project_path,'__local__','ready'))
            #print sys_str
            os.system(sys_str)
        except:
            cr(sys_str,"failed")
        #cr("so(C,",opj(project_path,'__local__',name+'.writing.pkl'),ra=1)
        so(C,opj(project_path,'__local__',name+'.writing.pkl'))
        #cm(-1)
        #cm(0,ra=1)
        time.sleep(0.1)
        try:
            sys_str = d2s('rm',opj(project_path,'__local__',name+'.pkl'))
            #print sys_str
            os.system(sys_str)
            #cm(1,ra=1)
        except:
            cr(sys_str,"failed")
            #cm(2,ra=1)
        sys_str = d2s('mv',opj(project_path,'__local__',name+'.writing.pkl'),opj(project_path,'__local__',name+'.pkl'))
        #print sys_str
        #cm(3,ra=1)
        os.system(sys_str)
        #cm(4,ra=1)
        sys_str = d2s('touch',opj(project_path,'__local__','ready'))
        #print sys_str
        os.system(sys_str)  
        #cm(5,ra=1)

    def function_save():
        if D['read_only']:
            return
        __save_C(D['Q'],D['project_path'])

    if not read_only:
        os.system('rm '+D['.pkl'])
    __add_keys(D['Q'])
    function_save() # this line added 3 July 2019

    def function_load():
        if D['load_timer'].check():
            D['load_timer'].reset()
        else:
            return False
        #print 'load check'
        try:
            t = file_modified_test(
                opj(D['.pkl']),
                D['mtime_prev']
            )
            #print t,dp(D['mtime_prev'])
            if t:
                D['mtime_prev'] = t
                __load_C(D['Q'],D['project_path'])
                __add_keys(D['Q'])
                return True
            else:
                return False
        except:
            cr('function_load(): load failed')
            return False

    def function_up():
        if len(D['current_keys']) > 0:
            D['current_keys'].pop()
            return {
                'message':  'went up',
                'action':   'success',
            }
        else:
            return {
                'message':  d2s('***','cannot go up.'),
                'action':   'failure',
            }

    def function_down(key):
        K = key_access(D,D['current_keys'])
        #print K.keys(),type(K[key])
        if key in K and type(K[key]) == dict:
            D['current_keys'].append(key)
            return {
                'message':  d2s('down to',key),
                'action':   'success',
            }
        else:
            return {
                'message':  d2s('***',key,'not there, cannot go down to it.'),
                'action':   'failure',
            } 

    def function_show(message=''):
        clear_screen()
        cg(host_name+', '+username+'\n',D['project_path'].replace(opjh(),'~/'))
        return __show_menu(key_access(D,D['current_keys']),message,D['parent_keys'])

    def function_set_value(key,arg_str=None,value=None):
        K = key_access(D,D['current_keys'])
        if K['--mode--'] == 'const':
            message = d2s(key,'is constant, not changed.')
            return {'message':message}
        if K['--mode--'] == 'bash':
            if arg_str != None:
                sys_str = d2s(K[key],arg_str)
            else:
                sys_str = K[key]
            os.system(sys_str)
            raw_enter()
            message = sys_str
            return {'message':message}
        if K['--mode--'] == 'extern':
            #cr('leaving',D['project_path'],'for',K[key],ra=1)
            start_Dic(K[key],D['Dics'],parent_keys=D['parent_keys']+D['current_keys'][1:]+[key])
            message = d2s('returned to',D['project_path'])
            return {'message':message}
        if K['--mode--'] == 'active':
            A = Dic_Loader(K[key])
            while True:
                try:
                    if A['load']():
                        clear_screen()
                        for k in sorted(A['Dic'].keys()):
                            cw(gr,str(k)+')',yl,dp(A['Dic'][k]))
                        cw(lb,time_str('Pretty'))
                    else:
                        pass#print 0
                except KeyboardInterrupt:
                    cr('*** KeyboardInterrupt ***')
                    break
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    CS_('Exception!',emphasis=True)
                    CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
            return {'message':'did active'}
        if type(K[key]) == bool:
            value = not K[key]
            if False: # older version with toggle check
                yes_no = raw_input(d2n("Toggle '",key,"'? ([y]/n) "))
                if yes_no == 'y' or yes_no == '':
                    value = not K[key]
                else:
                    message = d2n("'",key,"' unchanged")
                    return {'message':message}
        elif K[key] in ['_toggle','toggle_']:
            if K[key] == '_toggle':
                value = 'toggle_'
            else:
                value = '_toggle'
        else:
            try:
                if type(K[key]) == np.ndarray:
                    d = d2s('current shape',shape(K[key]))
                else:
                    d = K[key]
                if value == None:
                    type_str = '<'+str(type(d)).split("'")[1]+'>'
                    #type_str = cf('<',type_str,'>','`e-d',s0='')
                    value = input(cf("Enter value for '",key,"' (",d,' ',type_str,"):",'`ybb',' ',s0='',s1=''))

                if type(K[key]) == np.ndarray:
                    if type(value) == str:
                        if value == 's':
                            if len(shape(K[key])) > 1 and len(shape(K[key])) < 4:
                                clf();
                                mi(K[key])
                                spause()
                                return {'message':d2s('mi ',key)}
                            elif len(shape(K[key])) == 1:
                                clf();
                                plot(K[key],'b.-')
                                spause()
                                return {'message':d2s('plot',key)}
                            else:
                                return {'message':d2s('cannot show',key)}
                        elif value == 'h':
                            if len(shape(K[key])) == 1:
                                clf();
                                hist(K[key])
                                spause()
                                return {'message':d2s('hist',key)}
                            else:
                                return {'message':d2s('cannot hist',key)}                    
            except:
                message = d2s(key,'not changed')
                return {'message':message}

        if type(K[key]) == float and type(value) == int:
            value = float(value)

        if type(value) != type(K[key]):
            beep()
            message = d2n("*** type(",value,") != type(",K[key],")")
        else:
            K[key] = value
            message = d2n("set '",key,"' to ",value,'')
            D['save']()
        return {'message':message}

    def function_menu():
        message = ''
        if not D['read_only']:
            D['save']()
        try:
            while True:
                D['load']()
                items = D['show'](message)
                while True:
                    #cr('here',message,ra=1)
                    R = make_choice(items)
                    if R['message'] != 'ran python':
                        break
                if R['action'] == 'quit':
                    cw("\ndone.\n")
                    sys.exit()#return
                elif R['action'] == 'failure':
                    beep()
                    message = R['message']
                    continue
                elif R['action'] == 'continue':
                    message = R['message'] #'continue'
                    continue
                elif R['action'] == 'save':
                    message = R['message']
                    D['save']()
                    continue
                elif R['action'] == 'choose':
                    if R['message'] == '<up>':
                        S = D['up']()
                        message = S['message']
                        cb('S =',S)
                    elif R['message'] == '<top>':
                        message = 'already at <top>'
                    else:
                        S = D['down'](R['message'])
                        message = S['message']
                        if S['action'] == 'success':
                            continue
                        else:
                            #K = key_access(D,D['current_keys'])
                            message = D['set_value'](R['message'],arg_str=R['arg_str'])['message']
                            continue
        
        except KeyboardInterrupt:
            cr('*** KeyboardInterrupt ***')
            sys.exit()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
       


    def __is_meta_key(k):
        if type(k) != str:
            return False
        if len(k) < 2:
            return False
        if k[:2] != '--' and k[-2:] != '--':
            return False
        else:
            return True

    #def clear_screen():
    #    cr("\nclear screen\n")

    def __show_menu(C,message,parent_keys=[]):
        if '--keys--' in C:
            key_list = C['--keys--']
        else:
            key_list = ['no keys']
        q = ': '
        cw(
            bl+q.join(parent_keys)+q+wh+q.join(key_list),
        ) 
        sorted_keys_ = sorted(C.keys())
        sorted_keys = []
        for k in sorted_keys_:
            if not __is_meta_key(k):
                sorted_keys.append(k)
        if len(key_list) == 0 and len(parent_keys) == 0:
            s = '<top>'
        else:
            s = '<up>'
        sorted_keys.insert(0,s)
        cc = bl
        for i in rlen(sorted_keys):
            if i == 0 and s == '<top>':
                cb(s)
                continue #return ''
            k = sorted_keys[i]
            val_color = lb
            v = ''
            edited = ''
            if k in C:
                if type(C[k]) == dict:
                    ctr = 0
                    for l in C[k]:
                        if not __is_meta_key(l):
                            ctr += 1
                    v = ''
                    cc = wh+underlined
                    val_color = wh

                elif False:#k.isupper():
                    C[k] = not C[k] #False
                    v = '' # '<auto False>' # Toggle
                    cc = wh+wh_bk
                elif __is_meta_key(k):
                    v = C[k]
                    if have_colored:
                        cc = colored.fg('grey_23') 
                    else:
                        cc = gr
                elif C['--mode--'] == 'bash':
                    cc = lb
                    v = ''
                elif C['--mode--'] == 'const':
                    v = C[k]
                    cc = wh
                    val_color = wh
                else:
                    if type(C[k]) == np.ndarray:
                        v = d2s('array with shape',shape(C[k]))
                    else:
                        v = C[k]
                    cc = yl
            if have_colored:
                atr = colored.attr('res_underlined')
            else:
                atr = ''
            type_str = '---'
            if v == '':
                type_str = ''
            else:
                type_str = str(type(v)).split("'")[1]
                type_str = cf('<',type_str,'>','`w-d',s0='')
            cb(bl,i,d2n(cc,k,atr),val_color,v,edited,type_str)
        cg('$',message)
        return sorted_keys


    D['up'] = function_up
    D['down'] = function_down
    D['load'] = function_load
    D['save'] = function_save
    D['show'] = function_show
    D['menu'] = function_menu
    D['set_value'] = function_set_value
    return D





def key_access(Dic,keys,start=True):
    if start:
        keys_copy = []
        for k in Dic['current_keys']:
            keys_copy.append(k)
        keys = keys_copy
    #cg(keys,ra=1)
    key = keys.pop(0)
    assert key in Dic.keys()
    if type(Dic[key]) == dict and len(keys) > 0:
        return key_access(Dic[key],keys,start=False)
    else:
        return Dic[key]










def Dic_Loader(path,wait_time=0.2):
    D = {}
    if '.pkl' not in path:
        path = path+'.pkl'
    D['path'] = path
    D['mtime_prev'] = -1
    D['wait time'] = wait_time
    D['wait timer'] = Timer(D['wait time'])
    ############ 12/29/19
    #
    # D['wait timer'].trigger()
    #
    ############
    D['Dic'] = None

    def function_load():
        if D['wait timer'].check():
            D['wait timer'].reset()
            if file_modified_test():
                D['Dic'] = lo(D['path'],noisy=False)
                return True
        time.sleep(D['wait time']/2.)
        return False

    def file_modified_test():
        D['mtime'] = os.path.getmtime(D['path'])
        if D['mtime'] > D['mtime_prev']:
            D['mtime_prev'] = D['mtime']
            return True
        return False

    D['load'] = function_load

    return D



def make_choice(sorted_keys):

    raw_choice = raw_input(wh+'choice: '+lb)

    arg_str = None
    if '`' in raw_choice:
        choice_lst = raw_choice.split('`')
        assert len(choice_lst) == 2
        raw_choice = choice_lst[0]
        arg_str = choice_lst[1]


    if raw_choice == '':
        return {
            'message':"other commands: q(quit) p(python) s(show array) h(hist array) r(resave)."+\
            "\n\tUse ` after selection number to indicate command line args follow.",
            'action':'continue',
        }
        
    if raw_choice == 'q':
        return {
            'message':  "\ndone.\n",
            'action':   'quit',
        }

    if raw_choice == 'p':
        menu_python()
        return {
            'message':  "ran python",
            'action':   'continue',
        }

    if raw_choice == 'r':
        return {
            'message':  "resaved",
            'action':   'save',
        }


    if str_is_int(raw_choice):
        choice = int(raw_choice)
    else:
        return {
            'message':  d2s("*** choice","'"+raw_choice+"'",'is not an integer'),
            'action':   'failure',
        }

    if choice < 0 or choice+1 > len(sorted_keys):
        return {
            'message':  '*** choice is out of range',
            'action':   'failure',
        }
    key_choice = sorted_keys[choice]

    return {
        'message':  key_choice,
        'action':   'choose',
        'arg_str': arg_str,
    }


def menu_python():
    try:
        code = raw_input(d2n("Enter python code: "))
        d = code.split(';')
        if 'print' not in d[-1]:
            d[-1]=d2s('print(',d[-1],')')
        code = ';'.join(d)
        exec(code)
        return ''
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        message = d2s('Exception!',exc_type,file_name,exc_tb.tb_lineno)
        return {'message':message}


def start_Dic(dic_project_path,Dics={},parent_keys=[],Arguments={}):
    set_Defaults( {'menu':False,'read_only':True,'load_timer_time':1.0}, Arguments )
    
    if True:#dic_project_path not in Dics:
        exec_str = d2s(
            'from',
            project_path__to__project_import_prefix(dic_project_path)+'.defaults',
            'import Q',
        )
        #cy(exec_str,ra=1)
        exec(exec_str)
        #kprint(Arguments,title='Arguments')
        #raw_enter()
        Dics[dic_project_path] = \
            Default_Values(
                Q,
                dic_project_path,
                read_only=Arguments['read_only'],
                parent_keys=parent_keys,
                Dics=Dics,
                load_timer_time=Arguments['load_timer_time'],
            )

    if Arguments['read_only']:
        Dics[dic_project_path]['load']()

    if False:
        cg(Arguments['start_keys'])
        for k in Arguments['start_keys']:
            cb(k,ra=1)
            r = Dics[dic_project_path]['down'](k)
            Dics[dic_project_path]['show']()
            cy(r)

    if Arguments['menu']:
        Dics[dic_project_path]['menu']()
    else:
        clp('run menu from command line:\n','`','~/kzpy3/Menu/main.py --path',dic_project_path,'`--rb')

    return Dics[dic_project_path]

























if __name__ == '__main__':


    Dics = {}

    start_Dic(dic_project_path=opjh(Arguments['path']),Dics=Dics,Arguments=Arguments)




#EOF





