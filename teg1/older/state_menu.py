# from kzpy3.caf2.state_menu import *
from kzpy3.utils import *



state_names = ['action','capture','deep drive','trim','init','refresh','quit']


def init_states(states):
	for s in state_names:
		states[s] = False
	return states

def display_states(states):
	print 'display_states'
	ctr = 0
	for s in state_names:
		print(d2n(ctr,') ',s,':\t',states[s]))
		ctr += 1


def menu_choice():
	#states = load_obj(opjD('states'))
	exec('states='+txt_file_to_list_of_strings(opjD('temp.txt'))[0])
	display_states(states)
	i = input(">> ")
	if type(i) in [tuple,list]:
		sn = state_names[i[0]]
		states[sn] = i[1]
	else:
		sn = state_names[i]
		if sn == 'quit':
			return False
		if sn == 'refresh':
			return True
		states[sn] = not states[sn]
		if states['init']:
			states = init_states(states)
	list_of_strings_to_txt_file(opjD('temp.txt'),[str(states)])
	#save_obj(states,opjD('states'))
	return True
"""
def menu_choice():
	print 'menu_choice'
	states = {}
	del states
	states = load_obj(opjD('states'))
	print states
	
	for s in state_names:
		if s not in states:
			print('Adding '+s)
			states[s] = False
	
	display_states(states)
	i = input(">> ")
	if type(i) in [tuple,list]:
		sn = state_names[i[0]]
		states[sn] = i[1]
	else:
		sn = state_names[i]
		if sn == 'quit':
			return False
		states[sn] = not states[sn]
	if states['init']:
		init_states(states)
	save_obj(states,opjD('states'))
	del states
	return True
"""
def main():
	while menu_choice():
		pass

if __name__ == '__main__':
	main()
