from kzpy3.utils2 import *




translation_dic = {'a':'apples','b':'build','c':'cats','d':'dogs'}




if __name__ == "__main__" and '__file__' in vars():
	argument_dictionary = args_to_dic({  'pargs':sys.argv[1:]  })
else:
	print('Running this within interactive python.')
	argument_dictionary = args_to_dic({  'pargs':"-a -1 -b 4 -c '[1,2,9]' -d '{1:5,2:4}'"  })



argument_dictionary = translate_args(
	{'argument_dictionary':argument_dictionary,
	'translation_dic':translation_dic})
print(argument_dictionary)
#print(argument_dictionary['cats'][2])
#print(argument_dictionary['dogs'][2])