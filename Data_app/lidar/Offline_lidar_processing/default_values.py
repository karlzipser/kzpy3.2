#!/usr/bin/env python

from kzpy3.utils3 import *

###############################################3
#
P = {}
P['ABORT'] = False
P['customers'] = ['Main']
P['To Expose'] = {}
P['To Expose']['Main'] = [
	'show time 1',
] 
#
###############################################3


P['To Expose']['Main'] = ['ABORT']
P['experiments'] = opjm('/media/karlzipser/1_TB_Samsung_n1')
P['exclusion prefix'] = '_'
P['dst folder'] = opjD('Depth_Images')
P['dst folder working'] = opjD('Depth_Images_working')

#EOF
P['width'] = 1024
P['height'] = 16
P['width_times_height'] = P['width'] * P['height']
P['show time 1'] = 10


######################################
#
width = P['width']
Y = {}
mx = 2*np.pi*1000.0
extra = 500
for d in range(0,int(mx+extra)):
    v = int( width*d / (1.0*mx) )
    if v > (width-1):
        v = (width-1)
    Y[d] = v

j = 0
for i in range(sorted(Y.keys())[-1]):
    if i in Y:
        j = Y[i]
    Y[i] = j

Y[np.nan] = 0
P['Y'] = Y
#
######################################
