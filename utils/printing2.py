from kzpy3.utils.common import *




def kprint(
    item,
    title='', 
    spaces='',
    space_increment='    ',
    ignore_keys=[],
    only_keys=[],
    ignore_types=[],
    numbering=True,
    max_items=sys.maxint,
    ra=0,
    r=0,
    p=0,
):
    #'<untitled>',
    item_printed = False
    if type(item) in ignore_types:
        return
    if type(title) not in [str,type(None)]:
        #print title,str(title)
        title = str(title)
    lst = []
    for i in range(len(space_increment)):
        lst.append('-')
    lst.append('.')
    indent_text = ''.join(lst)
    #print item,indent_text,title
    n_equals = ''
    #if type(item) == type(na([0])):
    #    item = item.tolist()
    if numbering:
        if type(item) in [dict,list]:
            n_equals = cf(' (n=',len(item),')','`w-d',s0='',s1='')

            n_equals

    if title != None:
        if len(title) > len(indent_text):
            indent_title = title
        else:
            indent_title = title + indent_text[len(title):]
    if title != None:
        if type(item) in [dict,list]:
            color_print(spaces,'`',indent_title,'`',n_equals,s0='',s1='')
        else:
            color_print(spaces,'`',title,'','`y',' ','`',item,'`g',s1='',s0='' )
            item_printed = True
    else:
        if type(item) in [dict,list]:
            color_print(spaces,indent_text,n_equals,s0='',s1='')


    if type(item) == list:
        ctr = 0
        for i in item:
            kprint(i,title=None,spaces=spaces+space_increment,space_increment=space_increment,ignore_keys=ignore_keys,only_keys=only_keys,ignore_types=ignore_types,numbering=numbering)
            ctr += 1
            if ctr >= max_items:
                break
    elif type(item) == dict:
        ctr = 0
        for k in sorted(item.keys()):
            if k in ignore_keys:
                continue
            if len(only_keys) > 0:
                if k not in only_keys:
                    continue
            if type(item[k]) in [dict,list]:
                l = len(item[k])
            else:
                l = 1
            kprint(item[k],title=k,spaces=spaces+space_increment,space_increment=space_increment,ignore_keys=ignore_keys,only_keys=only_keys,ignore_types=ignore_types,numbering=numbering)
            ctr += 1
            if ctr >= max_items:
                break            
    elif not item_printed:
        color_print(spaces,item,'`g',s0='',s1='')

    if p:
        time.sleep(p)

    if ra or r:
        raw_enter()



function_types = [type(sorted),type(fname)]



def color_format(*args,**Kwargs):
    set_Defaults({'s0':' ','s1':' ','ra':False,'r':False,'p':0},Kwargs,)
    B = color_define_list(args)
    c = []
    for i in sorted(B.keys()):
        if len(B[i]['data']) > 0:
            if 'colors' in B[i] and B[i]['colors'] != None and len(B[i]['colors']) > 0:
                c.append(colored(
                    d2s_spacer(B[i]['data'],spacer=Kwargs['s0']),
                    B[i]['colors'][0],
                    B[i]['colors'][1],
                    B[i]['colors'][2]),
                )
            else:
                c.append(colored(*B[i]['data']))
    #print c
    s = d2s_spacer(c,spacer=Kwargs['s1'])
    if 'strip_opjh' not in Kwargs or Kwargs['strip_opjh']:
        s = s.replace(opjh(),'')
    return s #d2s_spacer(c,spacer=Kwargs['s1'])

def color_print(*args,**Kwargs):
    """
    e.g.,

        color_print(1,2,3,'`bgu',4,5,6,'`',7,8,9,'`gbb',s1='<==>',s0='-')
    """
    print(color_format(*args,**Kwargs))
    re = False
    if 'ra' in Kwargs:
        if Kwargs['ra']:
            re = True
    if 'r' in Kwargs:
        if Kwargs['r']:
            re = True
    if re:
        raw_enter()
    if 'p' in Kwargs:
        time.sleep(Kwargs['p'])

cf = color_format
clp = color_print

def color_define_list(a):
    B = {}
    ctr = 0
    B[ctr] = {}
    B[ctr]['data'] = []
    B[ctr]['colors'] = (None,None,None)
    for c in a:
        if type(c) == str and len(c) > 0:
            if c[0]=='`':
                B[ctr]['colors'] = translate_color_string(c[1:])
                ctr += 1
                B[ctr] = {}
                B[ctr]['data'] = []
                B[ctr]['colors'] = (None,None,None)
                continue
        B[ctr]['data'].append(c)
    for i in B.keys():
        if len(B[i]['data']) == 0:
            del B[i]
    return B


def translate_color_string(s):
    color,on_color,attrs = None,None,None
    Translate_color = {
        'g':'green',
        'b':'blue',
        'w':'white',
        'y':'yellow',
        'r':'red',
        'm':'magenta',
        'c':'cyan',
        'e':'grey',
        '-':None,
    }
    Translate_on_color = {
        'g':'on_green',
        'b':'on_blue',
        'w':'on_white',
        'y':'on_yellow',
        'r':'on_red',
        'm':'on_magenta',
        'c':'on_cyan',
        'e':'on_grey',
        '-':None,
    }
    Translate_attribute = {
        'b':'bold',
        'u':'underline',
        'd':'dark',
        'r':'reverse',
        '-':None,
    }
    if len(s) > 0:
        color = Translate_color[s[0]]
    if len(s) > 1:
        on_color = Translate_on_color[s[1]]
    if len(s) > 2:
        attrs = []
        for i in range(2,len(s)):
            attrs.append(Translate_attribute[s[i]])
    if attrs != None:
        attrs = list(set(attrs))
        if attrs[0] == None:
            attrs = None
    return color,on_color,attrs

if False:
    kprint([12,3,3],title='aa')
    kprint({1:2,3:4},title='aa')
    kprint(1,title='aa')

exec(identify_file_str)


if False:
    function_type = type(kprint)
    def Environment():
        D = {}
        D['encoder'] = 0
        D['motor'] = 49
        def function_step():
            D['encoder'] += 0.1*rndn()
            D['motor'] += 10*rndn()
            D['encoder'] = dp(D['encoder'])
            D['motor'] = int(D['motor'])
            return {
                'encoder':D['encoder'],
                'motor':D['motor'],
            }
        D['step'] = function_step
        D['collection'] = range(3)+[{'a':1,'b':2},3,{'e':{'c':{1:2,3:4},'d':{1:2,3:4},}}]
        D['dictionary'] = {'a':1,'b':2}
        D['Dic2'] = {'cdefghi':{1:2,3:4},'d':{1:2,3:4},'e':{'c':{1:2,3:4},'d':{1:2,3:4},}}
        return D
    E = Environment()
    #kprint(E,'E',ignore_keys=[],ignore_types=[])


# http://code.activestate.com/recipes/145297-grabbing-the-current-line-number-easily/
import inspect
def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

def fline():
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    filename = module.__file__
    now = datetime.datetime.now()
    return cf(inspect.currentframe().f_back.f_lineno,'`--r',
        fname(filename),'`',
        pname(filename),now.strftime('(%H:%M:%S)'),'`--d')

if False:
    COUNTER_PRINT_CTR_____ = 0
    def counter_print(reset=False):
        global COUNTER_PRINT_CTR_____
        if reset:
            COUNTER_PRINT_CTR_____ = 0
        clp('counter_print','`',COUNTER_PRINT_CTR_____,'`--r')
        COUNTER_PRINT_CTR_____ += 1

#EOF
