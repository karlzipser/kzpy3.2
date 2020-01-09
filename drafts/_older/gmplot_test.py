#,
from kzpy3.vis3 import *
import gmplot 

latitude_list = []
longitude_list = []

files = sggo(opjD('GPS3/*.pkl'))
for f in files:
	G = lo(f)
	xys = na(G['xys'])
	latitude_list += list(xys[:,0])
	longitude_list += list(xys[:,1])

gmap3 = gmplot.GoogleMapPlotter(latitude_list[0], longitude_list[0], 18) 

gmap3.scatter( latitude_list, longitude_list, '#FFFFFF', size = 1, marker = False ) 

gmap3.draw( opjD('m0.html') ) 
#,b
