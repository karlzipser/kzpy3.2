#!/usr/bin/env python
from kzpy3.utils3 import *
exec(identify_file_str)


commands = [
	 "python kzpy3/Train_app/Sq40_proj_from_scratch_premeta_from_24Dec/trainloop.py",
	"python kzpy3/Train_app/Sq120_ldr_output_4April2019/trainloop.py",
	"python kzpy3/Menu_app/menu2.py path kzpy3/Train_app/Sq120_ldr_output_4April2019 dic P",
	# "python kzpy3/Train_app/Sq_ldr_interval_tester5/Main.py cluster_list ~/Desktop/cluster_list_25_1st_pass.pkl threshold 0.25",
	# "python kzpy3/Train_app/Sq_ldr_classifier_/trainloop.py",
	"python kzpy3/Train_app/Sq120_ldr_output_2nd_training_16April2019/trainloop.py",
	"python kzpy3/Menu_app/menu2.py path kzpy3/Train_app/Sq120_ldr_output_2nd_training_16April2019 dic P",
]

finished = False
print('\n\n')
while not finished:
	try:
		ctr = 0
		for c in commands:
			if is_even(ctr):
				cc = cg
			else:
				cc = cb
			cc(ctr,c)
			ctr += 1
		choice = input('choice > ')
		cy("Doing: ",choice)
		os.system(commands[choice])
		finished = True
		
	except KeyboardInterrupt:
	    cr('\n\n*** KeyboardInterrupt ***\n')
	    sys.exit()
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		CS_('Exception!',emphasis=True)
		CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)		


#EOF
