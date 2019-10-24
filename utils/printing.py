#from kzpy3.utils.common import *
# This file is used by .common, so can't import it. Therefore, imports must be
# specified here.
import numpy as np
from termcolor import cprint
from termcolor import colored

PRINT_COMMENTS = True
def CS_(comment,section='',s='',say_comment=False,emphasis=False,exception=False,newline=True,print_comment=True):

    if print_comment and PRINT_COMMENTS:
        stri = '#  '
        stri = stri + comment
        if len(s) > len(section):
            section = s
        if len(section) > 0:
            stri += ' ('+section+')'
        if not emphasis and not exception:
            cprint(stri,attrs=[],color='white',on_color='on_grey')#cprint(stri,'red','on_green')
        elif exception:
            cprint(stri,attrs=['blink','bold'],color='red',on_color='on_yellow')
        else:
            cprint(stri,attrs=['bold','reverse'],color='white',on_color='on_grey')
            #spd2s(comment)
        if newline:
            print('\n')
    if say_comment:
        if using_osx():
            say(comment,rate=250,print_text=False)
    return True
    
CS = CS_
#CS_('imported kzpy3.utils3')
def cs(*args):
    CS(d2s_spacer(args,spacer=' '))





def d2s_spacer(args,spacer=' '):
    lst = []
    for e in args:
        lst.append(str(e))
    return spacer.join(lst)
def d2s(*args):
    '''
    e.g.,
    
    d2s('I','like',1,'or',[2,3,4])
    
    yields
    
    'I like 1 or [2, 3, 4]'
    
    d2c(1,2,3) => '1,2,3'
    d2f('/',1,2,3) => '1/2/3'
    '''
    return d2s_spacer(args)
def d2c(*args):
    return d2s_spacer(args,spacer=',')
def d2p(*args):
    return d2s_spacer(args,spacer='.')
def d2n(*args):
    return d2s_spacer(args,spacer='')
def d2f(*args):
    return d2s_spacer(args[1:],spacer=args[0])
def pd2s(*args):
    cprint(d2s(*args))
def pd2n(*args):
    print(d2n(*args))

#if False:
#   for i in range(256):
#       print d2n('\x1b[',i,'m',i,' test','\x1b[36m')
rd = '\x1b[31m'
gr = '\x1b[32m'
yl = '\x1b[33m'
bl = '\x1b[34m'
mg = '\x1b[35m'
lb = '\x1b[36m'
wh = '\x1b[37m'

wh_bk = '\x1b[40m'
wh_rd = '\x1b[41m'
wh_gr = '\x1b[42m'
wh_bl = '\x1b[44m'
wh_mg = '\x1b[45m'
wh_lb = '\x1b[46m'

mg = '\x1b[35m'
lb = '\x1b[36m'
wh = '\x1b[37m'

og = '\x1b[91m'
underlined = '\x1b[4m'

def spd2s(*args):
    d_ = d2s(*args)
    l_ = len(d_)
    s_ = ""
    for q_ in range(len(d_)+4):
        s_ += "*"
    cprint(s_+'\n*','yellow')
    cprint('* '+d_,'yellow')
    cprint('*\n'+s_,'yellow')
def sbpd2s(*args):
    d_ = d2s(*args)
    l_ = len(d_)
    s_ = ""
    for q_ in range(len(d_)+4):
        s_ += "*"
    cprint(s_+'\n*','blue')
    cprint('* '+d_,'blue')
    cprint('*\n'+s_,'blue')
def srpd2s(*args):
    d_ = d2s(*args)
    l_ = len(d_)
    s_ = ""
    for q_ in range(len(d_)+4):
        s_ += "*"
    cprint(s_+'\n*','red')
    cprint('* '+d_,'red')
    cprint('*\n'+s_,'red')


def beep():
    print('\007')

def print_stars(n=1):
    for i in range(n):
        print("""*************************************************""")
def print_stars0(n=1):
    print_stars()
    print("*")
def print_stars1(n=1):
    print("*")
    print_stars()


def dp(f,n=2):
    """
    get floats to the right number of decimal places, for display purposes
    """
    assert(n>=0)
    if n == 0:
        return int(np.round(f))
    f *= 10.0**n
    f = int(np.round(f))
    return f/(10.0**n)






def clear_screen():
    print(chr(27) + "[2J")

def format_row(list_of_sym_percent_pairs):
    __,ncols = get_terminal_size()
    row_str = ''
    for i in range(ncols):
        for sp in list_of_sym_percent_pairs:
            sym = sp[0]
            per = sp[1]
            if per < 0:
                per = 0.
            elif per > 99:
                per = 99.
            col = int(per/100.*ncols)
            if i == col:
                row_str += sym
                break
        else:
            row_str += ' '
    return row_str





def cl(*args,**Kwargs):
    """
    Return string based on colored function, but with d2s style input.

    e.g.,
        pd2n(
            cl(1,2,3,o='b',s=' ... '),
            cl(1,2,3,c='blue',s='+'),
            cl(1,2,3,c='white',a=['r','b'],s='>')
        )
    """
    Translation = {
        'on_color': {
            'on_red':['on_red','red','r'],
            'on_green':['on_green','green','g'],
            'on_blue':['on_blue','blue','b'],
            'on_yellow':['on_yellow','on_yellow','y'],
            'on_white':['on_white','white','w'],
            'on_magenta':['on_magenta','magenta','m'],
            'on_blue':['on_blue','blue','b'],
            'on_yellow':['on_yellow','yellow','y'],
            'on_cyan':['on_cyan','cyan','c'],
        },
        'color': {
            'red':['red','r'],
            'green':['green','g'],
            'blue':['blue','b'],
            'yellow':['yellow','y'],
            'white':['white','w'],
            'magenta':['magenta','m'],
            'blue':['blue','b'],
            'yellow':['yellow','y'],
            'cyan':['cyan','c'],
        },
        'attrs': {
            'bold':['bold','b'],
            'underline':['underline','u'],
            'dark': ['dark','d'],
            'reverse': ['reverse','r']
        }
    }
    Defaults = {'c':None, 'o':None, 'a':None, 's':' '}
    for k in Kwargs.keys():
        if k not in Defaults.keys():
            cr("*** Warning, argument '"+k+"' not in expected arguments:\n\t",Defaults.keys())
    for k in Defaults.keys():
        if k not in Kwargs.keys():
            Kwargs[k] = Defaults[k]
    if type(Kwargs['a']) == str:
        Kwargs['a'] = [char for char in Kwargs['a']]
    for c in Translation['color']:
        if Kwargs['c'] in Translation['color'][c]:
            Kwargs['c'] = c
            break
    for c in Translation['on_color']:
        if Kwargs['o'] in Translation['on_color'][c]:
            Kwargs['o'] = c
            break
    attributes = []
    if Kwargs['a'] != None:
        for a in Kwargs['a']:
            for c in Translation['attrs']:
                if a in Translation['attrs'][c]:
                    attributes.append(c)
                    break
        Kwargs['a'] = attributes
    #print(Kwargs)
    s = colored(
        text=d2s_spacer(args,spacer=Kwargs['s']),
        color=Kwargs['c'],
        on_color=Kwargs['o'],
        attrs=Kwargs['a']
    )
    return s

def clp(*args,**Kwargs):
    print cl(*args,**Kwargs)



def kprint(item,title=None):
    item_printed = False
    if title != None:
        print('')
        if type(item) in [dict,list]:
            len_item = len(item)
            clp(title,' (n=',len_item,')',o='g',s='') 
        else:
            pd2n( cl(title,':',o='g',s=''),' ',cl(item,c='g') )
            item_printed = True
        
    if type(item) == list:
        for i in item:
            clp(i,c='b')
    elif type(item) == dict:
        for k in sorted(item.keys()):
            if type(item[k]) in [dict,list]:
                l = len(item[k])
            else:
                l = 1
            clp(k,' {n=',l,'}',c='y',s='')
    elif not item_printed:
        clp(item,c='g')

#EOF
