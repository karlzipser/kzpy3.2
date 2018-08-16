from kzpy3.utils2 import *

local_dot_cs = opjh('.cs')
unix(d2s('mkdir -p',local_dot_cs))

Mr_Blue_Back_dot_cs = """nvidia@192.168.1.120:"~/.cs \b"""

#CS_(" comment section id level max_freq stop_after just_once")

def CS(txt,dot_cs=local_dot_cs):
	#txt = "test."
	_CS_(txt)
	if dot_cs != local_dot_cs:
		unix(d2s("scp",dot_cs,local_dot_cs))
	text_to_file(opj(dot_cs,'cs.txt'),txt)
	_say()


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