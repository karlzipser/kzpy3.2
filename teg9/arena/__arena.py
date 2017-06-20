from kzpy3.utils import *
pythonpaths(['kzpy3','kzpy3/teg9'])
from vis import *

###############
#
def Markers(markers_clockwise,radius):
	D = {}
	D['Purpose'] = 'Markers for the aruco arena.'
	D['clockwise'] = markers_clockwise
	D['ids_all'] = []
	D['angles_dic'] = {}
	D['angles'] = 2*np.pi*np.arange(len(markers_clockwise))/(1.0*len(markers_clockwise))
	D['xy'] = []
	for i in range(len(markers_clockwise)):
		a = D['angles'][i]
		D['angles_dic'][markers_clockwise[i]] = a
		x = radius*np.sin(a)
		y = radius*np.cos(a)
		D['xy'].append([x,y])
	D['xy_dic'] = {}
	assert(len(markers_clockwise) == len(D['xy']))
	D['cv2_draw'] = _cv2_draw
	return D

def _cv2_draw(D,img):
	for j in range(len(D['clockwise'])):
		m = D['clockwise'][j]
		xy = D['xy'][j]
		D['xy_dic'][m] = xy
		c = (255,0,0)
		xp,yp = img['floats_to_pixels'](img,xy)
		cv2.circle(img['img'],(xp,yp),4,c,-1)


#
###################