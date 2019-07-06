from kzpy3.vis3 import *
import gmplot 

latitude_list = [ 30.3358376, 30.307977, 30.3216419 ] 
longitude_list = [ 77.8701919, 78.048457, 78.0413095 ] 
#G = lo('/Users/karlzipser/Desktop/GPS3/1562099347.61.pkl')
G = lo('/Users/karlzipser/Desktop/GPS3/1562360832.11_1873.pkl')
xys = na(G['xys'])
latitude_list = list(xys[:,0])
longitude_list = list(xys[:,1])

gmap3 = gmplot.GoogleMapPlotter(latitude_list[0], longitude_list[0], 18) 

gmap3.scatter( latitude_list, longitude_list, '#FFFFFF', size = 1, marker = False ) 

# Plot method Draw a line in 
# between given coordinates 
#gmap3.plot(latitude_list, longitude_list, 'cornflowerblue', edge_width = 2.5) 

gmap3.draw( opjD('m0.html') ) 

