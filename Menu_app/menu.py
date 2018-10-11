from kzpy3.utils3 import *
"""
e.g.,

    python kzpy3/Menu_app/menu.py path kzpy3/Menu_app dic M

"""



def menu(Topics,path):
    if 'ABORT' not in Topics: Topics['ABORT'] = False
    if 'cmd/autostart menu' not in Topics: Topics['autostart menu'] = False
    if 'ABORT' not in Topics: Topics['to_hide'] = []
    if 'ABORT' not in Topics: Topics['to_expose'] = []
    EXIT = False
    message = False
    choice_number = 0
    Number_name_binding = {}
    Name_number_binding = {}
    """
    if 'cmd/clear_screen' not in Topics:
        Topics['cmd/clear_screen'] = True
        Topics['to_expose'].append('clear_screen')
    print Topics
    raw_enter()
    """
    if 'cmd/clear_screen' not in Topics:
        Topics['cmd/clear_screen'] = True
    if 'menu name' not in Topics:
        Topics = '<< menu not yet named >>'
    while EXIT == False and Topics['ABORT'] == False:

        try:

            if Topics['cmd/clear_screen']:
                clear_screen()

            ctr = 1
            Number_name_binding[ctr]='exit';cprint(d2n(ctr,') ',Number_name_binding[ctr]),'yellow');ctr+=1
            Number_name_binding[ctr]='load';cprint(d2n(ctr,') ',Number_name_binding[ctr]),'yellow');ctr+=1
            Number_name_binding[ctr]='save';cprint(d2n(ctr,') ',Number_name_binding[ctr]),'yellow');ctr+=1
            Number_name_binding[ctr]='add';cprint(d2n(ctr,') ',Number_name_binding[ctr]),'yellow');ctr+=1
            Number_name_binding[ctr]='hide';cprint(d2n(ctr,') ',Number_name_binding[ctr]),'yellow');ctr+=1
            Number_name_binding[ctr]='expose';cprint(d2n(ctr,') ',Number_name_binding[ctr]),'yellow')

            first = True
            if 'to_expose' in Topics:
                names_to_use = Topics['to_expose']
            else:
                names_to_use = Topics.keys()

            for name in sorted(names_to_use):
                
                ctr += 1

                Number_name_binding[ctr] = name

                if first:
                    q = ' '
                    first = False
                else:
                    q = ''
                q = ''
                #print d2n(q,ctr,') ',name,': ',Topics[name],'  '),
                #cprint(type(Topics[name]).__name__,'grey')
                color_scheme = [
                    ['cmd/',['red','on_white']],
                    ['path/','blue'],
                    ['net/',['white','on_green']],
                    ['dat/','green'],
                    ['cmd/',['red','on_white']],
                    ['ABORT',['white','on_red']],
                    ['plt/',['white','on_green']],
                    ['sys/',['white','on_blue']],
                    #['cmd/',['red','on_white']],
                    #['cmd/',['red','on_white']],
                ]
                for c in color_scheme:
                    #print c
                    s = c[0]
                    #print s
                    if name.isupper():
                        c = ['cmd/',['red','on_white']]
                    elif s not in name:
                        c = ['normal','normal']
                    cs = c[1]
                    if type(cs) == list:
                        cf,cb = cs[0],cs[1]
                    else:
                        cf,cb = cs,None
                    cstr = d2n(q,ctr,') ',name,': ',Topics[name],'  ',type(Topics[name]).__name__)
                    if c[0] == 'normal':
                        print(cstr)
                    elif cs != None:
                        cprint(cstr,cf,cb)
                    else:
                        cprint(cstr,cf)
                    break

            for n in Number_name_binding.keys():
                Name_number_binding[Number_name_binding[n]] = n

            if message:

                CS_(message)

            choice_number = input('#? ')

            if type(choice_number) != int:
                message = "bad option"

            elif choice_number == Name_number_binding['exit']:
                EXIT = True

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

                Topics_loaded = lo(opjh(path,'__local__',filename))
                for t in Topics_loaded:
                    Topics[t] = Topics_loaded[t]
                save_topics(Topics,path)
                message = d2s('loaded',filename)

            elif choice_number == Name_number_binding['save']:
                message = 'file not saved'         
                description = get_safe_name(raw_input('\tshort description #? '))
                assert(len(description)>0)
                filename = d2n('Topics.',description,'.pkl')
                full_path = opjh(path,'__local__',filename)
                so(Topics,full_path)
                message = d2s('saved',full_path)
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
                if type(current_val) == bool:
                    yes_no = raw_input(d2n(name,'(',current_val,') toggle value? (y/n) '))
                    if yes_no == 'y':
                        if Topics[name]:
                            Topics[name] = False
                        else:
                            Topics[name] = True
                else:    
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
    so(Topics,opjh(path,'__local__','Topics.pkl'))
    text_to_file(opjh(path,'__local__','ready'),'')
    #unix('touch '+opj(path,'ready'))

def print_exposed(Topics):
    if Topics['cmd/clear_screen']:
        clear_screen()
    print ''
    if 'to_expose' not in Topics:
        Topics['to_expose'] = []
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
    if True:#try:
        while Parameters['ABORT'] == False:
            if timer.check():
                Topics = load_Topics(path,first_load)
                if type(Topics) == dict:
                    for t in Topics['to_expose']: #Topics.keys():
                        if '!' in t:
                            pass
                        else:
                            Parameters[t] = Topics[t]
                timer.reset()
            else:
                time.sleep(0.1)
    else:#except:
        Parameters['ABORT'] = True
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        CS_('Exception!',exception=True,newline=False)
        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)

__MENU_THREAD_EXEC_STR__ = """
import __default_values_module_name__ as default_values
__topics_dic_name__ = default_values.__topics_dic_name__
__topics_dic_name__['ABORT'] = False
import kzpy3.Menu_app.menu
menu_path = "__default_values_module_name__".replace('.','/').replace('/default_values','')
#menu_path = __topics_dic_name__['The menu path.']
if not os.path.exists(menu_path):
    os.makedirs(menu_path)
try:
    os.remove(opj(path,'ready'))
except:
    pass
threading.Thread(target=kzpy3.Menu_app.menu.load_menu_data,args=[menu_path,__topics_dic_name__]).start()
#if 'cmd/autostart menu' in __topics_dic_name__:
#    if __topics_dic_name__['cmd/autostart menu']:
#        os.system(d2n("gnome-terminal -x python kzpy3/Menu_app/menu.py path ",menu_path," dic __topics_dic_name__"))
"""

if __name__ == '__main__':# and EXIT == False:
    path = Arguments['path']
    module = path.replace('/','.').replace('.py','')
    CS_(module,'module')
    dic = Arguments['dic']
    CS_(dic,'dic')
    exec(d2n('import ',module,'.default_values as default_values'))
    exec(d2n('Topics = default_values.',dic))
    menu(Topics,path)
    #raw_enter(__file__+' done. ')
    print '\ndone.\n'


# python kzpy3/Menu_app/menu.py path ~/kzpy3/Cars/car_24July2018/nodes/__local__/arduino/ default 1 Topics arduino

#CS_(d2c('e.g.','python kzpy3/Menu_app/menu.py module kzpy3.Cars.car_24July2018.nodes.Default_values.arduino dic Parameters'))


True
#EOF
