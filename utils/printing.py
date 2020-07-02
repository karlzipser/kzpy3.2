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





def __d2s_spacer(args,spacer=' '):
    lst = []
    for e in args:
        lst.append(str(e))
    return spacer.join(lst)


def d2s_spacer(args,spacer=' '):
    lst = []
    for e in args:
        try:
            ee = str(e)
        except:
            ee = e
            #print('d2s_spacer except with '+ee)
        lst.append(ee)
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








#EOF
