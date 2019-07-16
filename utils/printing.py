#from kzpy3.utils.common import *
import numpy as np
from termcolor import cprint

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

base = '\033[1;'
ascii_colors = {
    'red':31,
    'green':32,
    'on_magenta':45,
    'on_transparent':49
}

astr = d2n(
    base,
    ascii_colors['red'],
    ';',
    str(ascii_colors['on_magenta']) + 'm',
)




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




rd = '\033[1;31;49m'
gr = '\033[1;32;49m'
yl = '\033[1;33;49m'
bl = '\033[1;34;49m'
mg = '\033[1;35;49m'
lb = '\033[1;36;49m'
wh = '\033[1;37;49m'
og = '\033[1;91;49m'

on_bk = '\x1b[40m'
on_rd = '\x1b[41m'
on_gr = '\x1b[42m'
on_bl = '\x1b[44m'
on_mg = '\x1b[45m'
on_lb = '\x1b[46m'



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



def Progress_animator(total_count,update_Hz=1.0,message=''):
    from kzpy3.misc.progress import ProgressBar2
    D = {}
    D['total_count'] = total_count
    D['progress'] = ProgressBar2(total_count,message=' '+message+': ') 
    D['progress timer'] = Timer(1.0/(1.0*update_Hz))
    def _update_function(current_count):
        if True:
            if D['progress timer'].check():
                #print 'CCC'
                assert current_count < D['total_count']+1
                D['progress'].animate(current_count)
                D['progress timer'].reset()
            else:
                pass#time.sleep(0.1)
        else:#except Exception as e:
            pass
    D['update'] = _update_function
    return D



#exec(identify_file_str)

#EOF
