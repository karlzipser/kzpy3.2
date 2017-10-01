###############################
#  for interactive terminal
import __main__ as main
if False:#not hasattr(main,'__file__'):
	from kzpy3.utils2 import *
	pythonpaths(['kzpy3','kzpy3/Train_app','kzpy3/teg9'])
#
###############################
from Parameters_Module import *
from kzpy3.vis2 import *
import Graph_Module
exec(identify_file_str)
"""


"""
_ = dictionary_access

for a in Args.keys():
	_(P,a,equals,_(Args,a))


spd2s('The Train application.')

#EOF