from kzpy3.utils3 import *

def menu(Topics,path):

    message = False
    choice_number = 0
    Number_name_binding = {}
    Name_number_binding = {}

    while choice_number != 1:

        if True:#try:


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
                files = get_files_sorted_by_mtime(opj(path,'*.pkl'))

                files.reverse()
                filenames = []
                ctr2 = 1
                for f in files:
                    if fname(f[0]) != 'Topics.pkl':
                        filenames.append(fname(f[0]))
                        print d2n('\t',ctr2,') ',filenames[-1])
                        ctr2 += 1

                filename = filenames[input('\tload #? ')-1]

                Topics_loaded = lo(opj(path,filename))
                for t in Topics_loaded:
                    Topics[t] = Topics_loaded[t]
                save_topics(Topics,path)
                message = d2s('loaded',filename)

            elif choice_number == Name_number_binding['save']:
                message = 'file not saved'         
                description = get_safe_name(raw_input('\tshort description #? '))
                assert(len(description)>0)
                filename = d2n('Topics.',description,'.pkl')
                so(Topics,opj(path,filename))
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

        else:#except Exception as e:
            print("********** rosmenu.py Exception ***********************")
            print(e.message, e.args)
            exec(EXCEPT_STR)
            raw_enter()


def save_topics(Topics,path):
    os.remove(opj(path,'ready'))
    os.remove(opj(path,'Topics.pkl'))
    #unix(d2n('rm ',opj(path,'ready')))
    #unix(d2n('rm ',opj(path,'Topics.pkl')))
    so(Topics,opj(path,'Topics.pkl'))
    text_to_file(opj(path,('ready'),''))
    #unix('touch '+opj(path,'ready'))

def load_Topics(path,first_load=False):
    r = sggo(path,'ready')
    if len(r) > 1:
        CS_('Warning, more than one ready in '+path)
    if len(r) == 1 or first_load:
        Topics = lo(opjh(path,'Topics.pkl'))
        if len(r) == 1:
            os.remove(opj(path,'ready'))
            #unix(d2n('rm ',opj(path,'ready')))
        return Topics
    else:
        return None

def load_menu_data(path,Parameters,first_load=False):
    timer = Timer(0.5)
    while Parameters['ABORT'] == False:
        if timer.check():
            Topics = load_Topics(path,first_load)
            if type(Topics) == dict:
                for t in Topics.keys():
                    Parameters[t] = Topics[t]
            timer.reset()
        else:
            time.sleep(0.1)

"""
e.g.
python kzpy3/Menu_app/menu.py path ~/kzpy3/Train_app/Train_Z1dconvnet0/__local__/arduino/ default 1 Topics arduino
python kzpy3/Menu_app/menu.py path ~/kzpy3/Train_app/Train_Z1dconvnet0/__local__/network/ default 1 Topics network
"""

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

#EOF
