from kzpy3.utils3 import *

def clear_screen():
    print(chr(27) + "[2J")

def menu(Topics,menu_path):

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
            Number_name_binding[ctr]='add';print d2n(' ',ctr,') ',Number_name_binding[ctr])

            first = True
            for name in Topics.keys():

                ctr += 1

                Number_name_binding[ctr] = name
                # Number_name_binding[ctr]
                if first:
                    q = ' '
                    first = False
                else:
                    q = ''
                print d2n(q,ctr,') ',name,': ',Topics[name],'  '),
                cprint(type(Topics[name]).__name__,'grey')
                #print d2n(ctr,') ',name,': ',dp(Topics[Number_name_binding[ctr]],2))

            for n in Number_name_binding.keys():
                Name_number_binding[Number_name_binding[n]] = n
            #pprint(Number_name_binding)
            #pprint(Name_number_binding)
            #raw_enter()
            if message:
                #print message
                CS_(message)#

            choice_number = input('#? ')

            if type(choice_number) != int:
                message = "bad option"

            elif choice_number == Name_number_binding['exit']:
                pass

            elif choice_number == Name_number_binding['load']:
                message = 'file not loaded'
                files = get_files_sorted_by_mtime(opj(menu_path,'*.pkl'))
                #print files
                #print type(files)
                files.reverse()
                filenames = []
                ctr2 = 1
                for f in files:
                    if fname(f[0]) != 'Topics.pkl':
                        filenames.append(fname(f[0]))
                        print d2n('\t',ctr2,') ',filenames[-1])
                        ctr2 += 1
                #file_choice_number = input('\t#? ')
                filename = filenames[input('\tload #? ')-1]
                #Topics_loaded = lo(opj(menu_path,filenames[file_choice_number-1]))
                Topics_loaded = lo(opj(menu_path,filename))
                for t in Topics_loaded:
                    Topics[t] = Topics_loaded[t]
                save_topics(Topics,menu_path)
                message = d2s('loaded',filename)

            elif choice_number == Name_number_binding['save']:
                message = 'file not saved'         
                description = get_safe_name(raw_input('\tshort description #? '))
                assert(len(description)>0)
                filename = d2n('Topics.',description,'.pkl')
                so(Topics,opj(menu_path,filename))
                message = d2s('saved',filename)


            elif choice_number == Name_number_binding['add']:
                message = 'topic not added'
                topic_name = get_safe_name(raw_input('\tnew topic name #? '))
                if topic_name in Topics:
                    message = topic_name +' already in Topics. ' + message
                    assert(False)
                Topics[topic_name] = None
                message = d2s('added topic',topic_name)
                    
            else:
                name = Number_name_binding[choice_number]
                message = name+' value not changed'
                current_val = Topics[name]
                Topics[name] = input(d2n(name,'(',current_val,') new value > '))
                save_topics(Topics,menu_path)
                message = 'changed '+name

        except Exception as e:
            print("********** rosmenu.py Exception ***********************")
            print(e.message, e.args)
            exec(EXCEPT_STR)
            #raw_enter()

    #clear_screen()

def save_topics(Topics,menu_path):
    unix(d2n('rm ',opj(menu_path,'ready')))
    unix(d2n('rm ',opj(menu_path,'Topics.pkl')))
    so(Topics,opj(menu_path,'Topics.pkl'))
    unix('touch '+opj(menu_path,'ready'))

def load_Topics(menu_path,first_load=False):
    if first_load:
        r = ['ready']
    else:
        r = sggo(menu_path,'ready')
    if len(r) > 1:
        CS_('Warning, more than one ready in '+menu_path)
    if len(r) == 1:
        Topics = lo(opjh(menu_path,'Topics.pkl'))
        unix(d2n('rm ',opj(menu_path,'ready')))
        return Topics
    else:
        #pd2s('Could not load from',menu_path)
        return None

def load_menu_data(menu_path,Parameters,first_load=False):
    timer = Timer(0.5)
    while Parameters['ABORT'] == False:
        if timer.check():
            Topics = load_Topics(menu_path,first_load)
            if type(Topics) == dict:
                for t in Topics.keys():
                    Parameters[t] = Topics[t]
            timer.reset()
        else:
            time.sleep(0.1)

#EOF