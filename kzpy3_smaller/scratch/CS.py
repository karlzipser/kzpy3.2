from kzpy3.utils2 import *


local_dot_cs = opjh('.cs')
unix(d2s('mkdir -p',local_dot_cs))

Mr_Blue_Back_dot_cs = """nvidia@192.168.1.120:"~/.cs \b"""

#CS_(" comment section id level max_freq stop_after just_once")
"""
C_write = C_['write']; Cw = C_write
C_say = CS['say']; Cs = C_say

def CS(txt,dot_cs=local_dot_cs):
	#txt = "test."
	_CS_(txt)
	if dot_cs != local_dot_cs:
		unix(d2s("scp",dot_cs,local_dot_cs))
	text_to_file(opj(dot_cs,'cs.txt'),txt)
	_say()
"""
"""
grey.
red.
green.
yellow.
blue.
magenta.
cyan.
white.

bold
dark
underline
blink
reverse
concealed
"""

def _write(args,section='',foreground='white',background='on_green',attrs=[],spacer=' ',num_tabs=0):
	comment_str = '# ' + d2s_spacer(args,spacer=spacer)
	for i in range(num_tabs):
		comment_str = '\t' + comment_str
	if section != '':
		section =  section + " : "
	total_str = section+comment_str
	cprint(total_str,foreground,background,attrs=attrs)
	if using_osx():
		say(total_str,rate=250,print_text=False)

def _write1(args,section='',num_tabs=0):
	_write(args,background='on_yellow',section=section,foreground='blue',attrs=['bold'],num_tabs=num_tabs)

_write(['hi',1+7],background='on_cyan',section='section 1',foreground='white',attrs=['blink','reverse'],num_tabs=3,spacer=',')

_write1(['bye!',3+2],section='section 22')

"""
def _write():
	pass

def _clear():
	"delete cs.*"

CSd = {'w':_write}

def _say():
	say(file_to_text(opjh('.cs','cs.txt')))

def _CS_(comment,section='',foreground='white',background='on_green'):
	stri = '# - '
	if len(section) > 0:
		stri = stri + section + ': '
	stri = stri + comment
	if PRINT_COMMENTS:
		cprint(stri,foreground,background)

class CS
"""
None