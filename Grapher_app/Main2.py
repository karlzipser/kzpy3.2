###############################
#  for interactive terminal
import __main__ as main
if not hasattr(main,'__file__'):
	from kzpy3.utils2 import *
	pythonpaths(['kzpy3','kzpy3/Grapher_app','kzpy3/teg9'])
#
###############################
from Parameters_Module import *
from kzpy3.vis2 import *
import Graph_Module
from Car_Data_app.Names_Module import *
exec(identify_file_str)

_ = dictionary_access

for a in Args.keys():
	_(P,a,equals,_(Args,a))



Img1 = Graph_Module.Image2(
	xmin,0,
	xmax,1000,
	ymin,-1,
	ymax,100,
	xsize,600,
	ysize,600)

Img1[img][100:400,100:400,:] = (255,128,64)

Img2 = Graph_Module.Image2(
	xmin,0,
	xmax,1000,
	ymin,-1,
	ymax,100,
	xsize,600,
	ysize,600,
	Img,Img1)

mi(Img1[img],1)
mi(Img2[img],2)