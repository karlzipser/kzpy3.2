from kzpy3.utils3 import *
"""
e.g.,

    python kzpy3/Menu_app/menu2.py path kzpy3/Menu_app dic M

"""



def menu2(Topics,path):

    assert 'ABORT' in Topics
    assert 'To Expose' in Topics

    EXIT = False
    message = False

    to_expose_keys = sorted(Topics['To Expose'])
    Q = to_expose_keys[0]

    choice_number = 0
    Number_name_binding = {}
    Name_number_binding = {}

    if 'cmd/clear_screen' not in Topics:
        Topics['cmd/clear_screen'] = True

    while EXIT == False and Topics['ABORT'] == False:

        choice_number = 0
        Number_name_binding = {}
        Name_number_binding = {}

        try:

            if Topics['cmd/clear_screen']:
                clear_screen()

#            cprint("<<<<<<<<<<<<<<<<<< "+Q+" >>>>>>>>>>>>>>>>>>",attrs=['bold'],color='white',on_color='on_grey')
            cprint("<<<<<<<<<<<<< "+Q+" >>>>>>>>>>>>>",attrs=['bold'],color='white',on_color='on_grey')
#                   8) IMU_SMOOTHING_PARAMETER: 0.95  float
            ctr = 1
            Number_name_binding[ctr]='exit';cprint(d2n(ctr,') ',Number_name_binding[ctr]),'yellow');ctr+=1
            Number_name_binding[ctr]='load';cprint(d2n(ctr,') ',Number_name_binding[ctr]),'yellow');ctr+=1
            Number_name_binding[ctr]='save';cprint(d2n(ctr,') ',Number_name_binding[ctr]),'yellow');ctr+=1
            Number_name_binding[ctr]='hide';cprint(d2n(ctr,') ',Number_name_binding[ctr]),'yellow');ctr+=1

            
            for k in to_expose_keys:
                if k != Q:
                    Number_name_binding[ctr]=k;cprint(d2n(ctr,') ',Number_name_binding[ctr]),'green');ctr+=1

            first = True

            names_to_use = Topics['To Expose'][Q]

            for name in sorted(names_to_use):
                
                

                Number_name_binding[ctr] = name
                
                if first:
                    q = ' '
                    first = False
                else:
                    q = ''
                q = ''
                
                color_scheme = [
                    ['cmd/',['red','on_white']],
                    ['path/','blue'],
                    ['net/',['white','on_green']],
                    ['dat/','green'],
                    ['cmd/',['red','on_white']],
                    ['ABORT',['white','on_red']],
                    ['plt/',['white','on_green']],
                    ['sys/',['white','on_blue']],
                ]
                for c in color_scheme:
                    s = c[0]
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

                ctr += 1

            for n in Number_name_binding.keys():
                Name_number_binding[Number_name_binding[n]] = n

            if message:

                CS(message)

            choice_number = input('#? ')

            for k in to_expose_keys:
                #print k
                if k in Name_number_binding:
                    #print k
                    if choice_number == Name_number_binding[k]:
                        #print Q,k
                        Q = k
                        continue

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

            elif choice_number == Name_number_binding['hide']:
                message = 'topic not hidden'
                hide_number = input('\tnumber to hide #? ')
                topic_name = Number_name_binding[hide_number]
                Topics['to_hide'].append(topic_name)
                for k in Topics['to_hide']:
                    if k in Topics['To Expose'][Q]:
                        Topics['To Expose'][Q].remove(k)
                message = d2s('topic',topic_name,'hidden')
                save_topics(Topics,path)
                                        
            else:
                name = Number_name_binding[choice_number]
                if name in to_expose_keys:
                    continue
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
                pd2s('**',path,'**')
                save_topics(Topics,path)
                message = 'changed '+name

        except Exception as e:
            print("********** rosmenu.py Exception ***********************")
            print(e.message, e.args)
            exec(EXCEPT_STR)
            raw_enter()


def save_topics(Topics,path):
    for customer in Topics['customers']:
        c = get_safe_name(customer)
        print '****'
        try:
            os.remove(opj(path,'__local__','ready.'+c))
        except:
            pass
        try:
            os.remove(opj(path,'__local__','Topics.'+c+'.pkl'))
        except:
            pass
        pd2s('***',opjh(path,'__local__','Topics.'+c+'.pkl'),'***')
        so(Topics,opjh(path,'__local__','Topics.'+c+'.pkl'))
        text_to_file(opjh(path,'__local__','ready.'+c),'')


def print_exposed(Topics,customer):
    if Topics['cmd/clear_screen']:
        clear_screen()
    print ''
    if 'menu name' in Topics:
        pd2s('##############',customer,'##############')
    first = True
    for name in sorted(Topics['To Expose'][customer]):
        if first:
            name_ = ' '+name
            first = False
        else:
            name_ = name
        print d2n(name_,': ',Topics[name],'  '),
        cprint(type(Topics[name]).__name__,'grey')
    print ''

def load_Topics(input_path,first_load=False,customer=''):
    c = get_safe_name(customer)
    path = opj(input_path,'__local__')
    r = sggo(path,'ready.'+c)
    cr("TEMP ",r)
    if len(r) > 1:
        CS_('Warning, more than one ready in '+path)
    assert len(r) < 2
    if len(r) == 1 or first_load:
        Topics = lo(opjh(path,'Topics.'+c+'.pkl'))
        print_exposed(Topics,customer)
        if len(r) == 1:
            try:
                os.remove(opj(path,'ready.'+c))
            except:
                pass
        cr("TEMP return Topics")
        return Topics
    else:
        cr("TEMP  return None")
        return None

def load_menu_data(path,Parameters,first_load=False,customer=''):
    timer = Timer(0.5)
    if True:#try:
        while Parameters['ABORT'] == False:
            if timer.check():
                Topics = load_Topics(path,first_load,customer)
                if type(Topics) == dict:
                    for t in Topics['To Expose'][Q]:
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



if __name__ == '__main__':# and EXIT == False:
    path = Arguments['path']
    module = path.replace('/','.').replace('.py','')
    CS_(module,'module')
    dic = Arguments['dic']
    CS_(dic,'dic')
    exec(d2n('import ',module,'.default_values as default_values'))
    exec(d2n('Topics = default_values.',dic))
    menu2(Topics,path)
    print '\ndone.\n'


# python kzpy3/Menu_app/menu.py path ~/kzpy3/Cars/car_24July2018/nodes/__local__/arduino/ default 1 Topics arduino

#CS_(d2c('e.g.','python kzpy3/Menu_app/menu.py module kzpy3.Cars.car_24July2018.nodes.Default_values.arduino dic Parameters'))



#EOF
