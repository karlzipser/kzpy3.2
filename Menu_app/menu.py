from kzpy3.utils3 import *

def menu(Topics,path):

    message = False
    choice_number = 0
    Number_name_binding = {}
    Name_number_binding = {}

    while choice_number != 1:

        try:


            clear_screen()

            ctr = 1
            Number_name_binding[ctr]='exit';print d2n(' ',ctr,') ',Number_name_binding[ctr]);ctr+=1
            Number_name_binding[ctr]='load';print d2n(' ',ctr,') ',Number_name_binding[ctr]);ctr+=1
            Number_name_binding[ctr]='save';print d2n(' ',ctr,') ',Number_name_binding[ctr]);ctr+=1
            Number_name_binding[ctr]='add';print d2n(' ',ctr,') ',Number_name_binding[ctr]);ctr+=1
            Number_name_binding[ctr]='hide';print d2n(' ',ctr,') ',Number_name_binding[ctr]);ctr+=1
            Number_name_binding[ctr]='expose';print d2n(' ',ctr,') ',Number_name_binding[ctr])

            first = True
            if 'to_expose' in Topics:
                names_to_use = Topics['to_expose']
            else:
                names_to_use = Topics.keys()

            for name in names_to_use:

                ctr += 1

                Number_name_binding[ctr] = name

                if first:
                    q = ' '
                    first = False
                else:
                    q = ''
                print d2n(q,ctr,') ',name,': ',Topics[name],'  '),
                cprint(type(Topics[name]).__name__,'grey')

            for n in Number_name_binding.keys():
                Name_number_binding[Number_name_binding[n]] = n

            if message:

                CS_(message)

            choice_number = input('#? ')

            if type(choice_number) != int:
                message = "bad option"

            elif choice_number == Name_number_binding['exit']:
                pass

            elif choice_number == Name_number_binding['load']:
                message = 'file not loaded'
                files = get_files_sorted_by_mtime(opj(path,'__local__','*.pkl'))

                files.reverse()
                filenames = []
                ctr2 = 1
                for f in files:
                    if fname(f[0]) != 'Topics.pkl':
                        filenames.append(fname(f[0]))
                        print d2n('\t',ctr2,') ',filenames[-1])
                        ctr2 += 1

                filename = filenames[input('\tload #? ')-1]

                Topics_loaded = lo(opj(path,'__local__',filename))
                for t in Topics_loaded:
                    Topics[t] = Topics_loaded[t]
                save_topics(Topics,path)
                message = d2s('loaded',filename)

            elif choice_number == Name_number_binding['save']:
                message = 'file not saved'         
                description = get_safe_name(raw_input('\tshort description #? '))
                assert(len(description)>0)
                filename = d2n('Topics.',description,'.pkl')
                so(Topics,opj(path,'__local__',filename))
                message = d2s('saved',filename)
                save_topics(Topics,path)


            elif choice_number == Name_number_binding['add']:
                message = 'topic not added'
                topic_name = get_safe_name(raw_input('\tnew topic name #? '))
                if topic_name in Topics:
                    message = topic_name +' already in Topics. ' + message
                    assert(False)
                Topics[topic_name] = None
                Topics['to_expose'].append(topic_name)
                message = d2s('added topic',topic_name)
                save_topics(Topics,path)
                    

            elif choice_number == Name_number_binding['hide']:
                message = 'topic not hidden'
                hide_number = input('\tnumber to hide #? ')
                topic_name = Number_name_binding[hide_number]
                Topics['to_hide'].append(topic_name)
                #Topics['to_expose'] = []
                #for k in Topics.keys():
                #    if k not in Topics['to_hide']:
                #        Topics['to_expose'].append(k)
                for k in Topics['to_hide']:
                    if k in Topics['to_expose']:
                        Topics['to_expose'].remove(k)
                message = d2s('topic',topic_name,'hidden')
                save_topics(Topics,path)
                    

            elif choice_number == Name_number_binding['expose']:
                message = 'topic not exposed'
                #expose_name = input('\tname to expose #? ')
                ctr2 = 1
                for f in Topics['to_hide']:
                    print d2n('\t',ctr2,') ',f)
                    ctr2 += 1
                expose_number = input('\tnumber to expose #? ')
                expose_name = Topics['to_hide'][expose_number-1]
                if expose_name in Topics['to_hide']:
                    Topics['to_hide'].remove(expose_name)
                if expose_name not in Topics['to_expose']:
                    Topics['to_expose'].append(expose_name)
                message = d2s('topic',expose_name,'exposed')
                save_topics(Topics,path)
                    
            else:
                name = Number_name_binding[choice_number]
                message = name+' value not changed'
                current_val = Topics[name]
                Topics[name] = input(d2n(name,'(',current_val,') new value > '))
                save_topics(Topics,path)
                message = 'changed '+name

        except Exception as e:
            print("********** rosmenu.py Exception ***********************")
            print(e.message, e.args)
            exec(EXCEPT_STR)
            raw_enter()


def save_topics(Topics,path):
    try:
        os.remove(opj(path,'__local__','ready'))
    except:
        pass
    try:
        os.remove(opj(path,'__local__','Topics.pkl'))
    except:
        pass
    #unix(d2n('rm ',opj(path,'ready')))
    #unix(d2n('rm ',opj(path,'Topics.pkl')))
    so(Topics,opj(path,'__local__','Topics.pkl'))
    text_to_file(opj(path,'__local__','ready'),'')
    #unix('touch '+opj(path,'ready'))

def print_exposed(Topics):
    print ''
    for name in Topics['to_expose']:
        print d2n(name,': ',Topics[name],'  '),
        cprint(type(Topics[name]).__name__,'grey')
    print ''

def load_Topics(input_path,first_load=False):
    path = opj(input_path,'__local__')
    #print path
    #print(sggo(path,'*'))
    r = sggo(path,'ready')
    #print r
    if len(r) > 1:
        CS_('Warning, more than one ready in '+path)
    if len(r) == 1 or first_load:
        Topics = lo(opjh(path,'Topics.pkl'))
        #print 'Topics='
        #print Topics
        print_exposed(Topics)
        if len(r) == 1:
            try:
                os.remove(opj(path,'ready'))
            except:
                pass
            #unix(d2n('rm ',opj(path,'ready')))
        return Topics
    else:
        return None

def load_menu_data(path,Parameters,first_load=False):
    timer = Timer(0.5)
    try:
        while Parameters['ABORT'] == False:
            if timer.check():
                Topics = load_Topics(path,first_load)
                if type(Topics) == dict:
                    for t in Topics.keys():
                        Parameters[t] = Topics[t]
                timer.reset()
            else:
                time.sleep(0.1)
    except:
        Parameters['ABORT'] = True
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        CS_('Exception!',exception=True,newline=False)
        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)


if False:
    __MENU_THREAD_EXEC_STR__ = """
#exec(d2s("import",__default_values_module_name__,"as default_values"))
#exec(d2n("Topics = default_values.",__topics_dic_name__))
import __default_values_module_name__ as default_values
Topics = default_values.__topics_dic_name__


Topics['ABORT'] = False
import kzpy3.Menu_app.menu

menu_path = Topics['The menu path.']
if not os.path.exists(menu_path):
    os.makedirs(menu_path)
try:
    os.remove(opj(path,'ready'))
except:
    pass
threading.Thread(target=kzpy3.Menu_app.menu.load_menu_data,args=[menu_path,Topics]).start()

    """
if True:
    __MENU_THREAD_EXEC_STR__ = """
#exec(d2s("import",__default_values_module_name__,"as default_values"))
#exec(d2n("__topics_dic_name__ = default_values.",__topics_dic_name__))
import __default_values_module_name__ as default_values
__topics_dic_name__ = default_values.__topics_dic_name__


__topics_dic_name__['ABORT'] = False
import kzpy3.Menu_app.menu

menu_path = __topics_dic_name__['The menu path.']
if not os.path.exists(menu_path):
    os.makedirs(menu_path)
try:
    os.remove(opj(path,'ready'))
except:
    pass
threading.Thread(target=kzpy3.Menu_app.menu.load_menu_data,args=[menu_path,__topics_dic_name__]).start()
"""

if __name__ == '__main__':
    path = Arguments['path']
    module = path.replace('/','.').replace('.py','')
    CS_(module,'module')
    dic = Arguments['dic']
    CS_(dic,'dic')
    exec(d2n('import ',module,'.default_values as default_values'))
    exec(d2n('Topics = default_values.',dic))       
    menu(Topics,path)

# python kzpy3/Menu_app/menu.py path ~/kzpy3/Cars/car_24July2018/nodes/__local__/arduino/ default 1 Topics arduino

#CS_(d2c('e.g.','python kzpy3/Menu_app/menu.py module kzpy3.Cars.car_24July2018.nodes.Default_values.arduino dic Parameters'))



"""
e.g.
python kzpy3/Menu_app/menu.py path ~/kzpy3/Train_app/Train_Z1dconvnet0/__local__/arduino/ default 1 Topics arduino
python kzpy3/Menu_app/menu.py path ~/kzpy3/Train_app/Train_Z1dconvnet0/__local__/network/ default 1 Topics network


if False:

    if __name__ == '__main__':
        path = Arguments['path']
        if 'default' in Arguments.keys():
            import kzpy3.Cars.car_24July2018.nodes.default_values as default_values
            if 'Topics' in Arguments.keys():
                if Arguments['Topics'] == 'arduino':
                    Topics = default_values.Parameters
                elif Arguments['Topics'] == 'network':
                    Topics = default_values.Network
                else:
                    assert False
        else:
            try:
                Topics = load_Topics(path,first_load=True)
            except:
                Topics = {}
        menu(Topics,path)

    if __name__ == '__main__':
        path = Arguments['path']
        if 'Topics' in Arguments:
            if (Arguments['Topics'] == 'arduino') or (Arguments['Topics'] == 'network'):
                if 'default' in Arguments.keys():
                    import kzpy3.Cars.car_24July2018.nodes.default_values as default_values
                    if Arguments['Topics'] == 'arduino':
                        Topics = default_values.Parameters
                    elif Arguments['Topics'] == 'network':
                        Topics = default_values.Network
                    else:
                        assert False
                else:
                    try:
                        Topics = load_Topics(path,first_load=True)
                    except:
                        Topics = {}

            elif Arguments['Topics'] == 'znn':
                if 'default' in Arguments.keys():
                    import kzpy3.Train_app.Train_znn0.default_values as default_values
                    Topics = default_values.P
        else:
            try:
                Topics = load_Topics(path,first_load=True)
            except:
                Topics = {}            
        menu(Topics,path)
"""
True
#EOF
