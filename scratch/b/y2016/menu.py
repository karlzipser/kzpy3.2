from kzpy3.utils import *

menu_str = """Menu:
a) do this
b) do that
q) quit"""

def menu():
	print(menu_str)
	r = raw_input(">")
	if r == 'a':
		cprint("DO THIS!",'red')
	if r == 'b':
		cprint("DO THAT",'red')
	if r == 'q':
		return
	menu()
