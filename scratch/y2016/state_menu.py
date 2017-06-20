from kzpy3.utils import *



state_names = ['capture','deep drive','trim','quit']
states = {}

def init_states():
	global states
	for s in state_names:
		states[s] = False

def display_states():
	ctr = 0
	for s in state_names:
		print(d2n(ctr,') ',s,':\t',states[s]))
		ctr += 1




def menu_choice(load=False):
	global states
	if load:
		states = load_obj(opjD('states'))
	else:
		init_states()
	while states['quit'] == False:
		display_states()
		i = input(">> ")
		if type(i) in [tuple,list]:
			sn = state_names[i[0]]
			states[sn] = i[1]
		else:
			sn = state_names[i]
			states[sn] = not states[sn]
		save_obj(states,opjD('states'))

#menu_choice()