from kzpy3.utils.common import *

def kprint(item,title=None):
    item_printed = False
    if title != None:
        print('')
        if type(item) in [dict,list]:
            len_item = len(item)
            color_print(title,' (n=',len_item,')','`-g',s0='')  #o='g',s='') 
        else:
            color_print(title,':','`-g',' ','`',item,'`g' )
            item_printed = True
        
    if type(item) == list:
        ctr = 0
        for i in item:
            color_print(ctr,') ','`--d',i,'`b',s1='',s0='')
            ctr += 1
    elif type(item) == dict:
        for k in sorted(item.keys()):
            if type(item[k]) in [dict,list]:
                l = len(item[k])
            else:
                l = 1
            color_print(k,' {n=',l,'}','`y')
    elif not item_printed:
        color_print(i,'`g')


def color_format(*args,**Kwargs):
    set_Defaults({'s0':' ','s1':' ','ra':False},Kwargs,)
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
    return d2s_spacer(c,spacer=Kwargs['s1'])

def color_print(*args,**Kwargs):
    """
    e.g.,

        color_print(1,2,3,'`bgu',4,5,6,'`',7,8,9,'`gbb',s1='<==>',s0='-')
    """
    print(color_format(*args,**Kwargs))
    if 'ra' in Kwargs:
        if Kwargs['ra']:
            raw_enter()

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
