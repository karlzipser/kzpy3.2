#,a
from kzpy3.vis3 import *

assert 'run_name' in Arguments

save_path = opjD('Data','pts2D_multi_step','pkl_angles0',Arguments['run_name']+'.pkl')

if os.path.exists(save_path):
    clp('!!!',save_path,'exists!!!','`wrb')
    exit()
    
make_path_and_touch_file(save_path)

if 'lst' not in locals():
	lst = lo(opjD('Data','pts2D_multi_step','pkl',Arguments['run_name']))

P = {}
P['behavioral_mode_list'] = ['left','direct','right']

Colors = {'direct':'b','left':'r','right':'g'}




def angle_between_with_sign(a,b):

	import math

	class Vect: # magnitudes not correct for large angles, only sign

	   def __init__(self, a, b):
	        self.a = a
	        self.b = b

	   def findClockwiseAngle(self, other):
	       # using cross-product formula
	       return -math.degrees(math.asin((self.a * other.b - self.b * other.a)/(self.length()*other.length())))
	       # the dot-product formula, left here just for comparison (does not return angles in the desired range)
	       # return math.degrees(math.acos((self.a * other.a + self.b * other.b)/(self.length()*other.length())))

	   def length(self):
	       return math.sqrt(self.a**2 + self.b**2)

	sgn = 1.
	vector1 = Vect(a[0],a[1])
	vector2 = Vect(b[0],b[1])
	angle = vector1.findClockwiseAngle(vector2)
	if angle < 0.:
		sgn = -1

	return sgn * degrees(angle_between(a,b))



Angles = { 'left':[], 'right':[] }

for i in range(len(lst)-1):
	print i
	Q = lst[i]

	Vectors = {}
	for b in P['behavioral_mode_list']:
		Vectors[b] = Q[b][-1] - Q[b][-2]

	for b in ['left','right']:
		Angles[b].append( angle_between_with_sign( Vectors['direct'], Vectors[b]) )
		
	if False: # np.abs(Angles['left']) > 90 or np.abs(Angles['right']) > 90:
		print "\n\n"
		print Angles['left'][-1], Angles['right'][-1]
		clf()
		plt_square()
		for b in P['behavioral_mode_list']:
			pts_plot(Q[b],color=Colors[b],sym='.-')
		spause()
		raw_enter()

so(Angles,save_path)
#,b
#EOF
