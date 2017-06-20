
from kzpy3.vis import *
from kzpy3.teg2.gps_fence.geometry import *

class Points:
	def __init__(self):
		self.my_position = (np.random.random(2)-0.5)/4.0
		self.pts = []
		r = 20.0/10.0
		for a in range(0,360,5):
			x = r*np.sin(np.deg2rad(a))
			y = r*np.cos(np.deg2rad(a))
			self.pts.append([x,y])
		r2 = 100.0/10.0
		for a in range(0,360,5):
			x = r2*np.sin(np.deg2rad(a))
			y = r2*np.cos(np.deg2rad(a))
			self.pts.append([x,y])
		for i in range(20):
			p = 2*np.random.random(2) - 1
			self.pts.append(p)
		self.pts = na(self.pts)
		self.vec_total_prev = na((0,0))
		self.my_position_prev = na((0,0))
		self.graphics = False

	def do_nothing(self):
		pass
		
	def do_update(self):
		self.vec_total = na([0.0,0.0])
		for i in range(1,len(self.pts)):
			self.vec_total += 0.01 * force_function((self.my_position[0],self.my_position[1]),self.pts[i,:])
			pass

		self.vec_total += 0.01 * force_function2((self.my_position[0],self.my_position[1]),self.pts[0,:])

		self.vec_total_copy = self.vec_total.copy()
		#print vec_total,vec_total_prev

		while inner_angle(self.vec_total,self.vec_total_prev) > 5:
			#print inner_angle(vec_total,vec_total_prev)
			self.vec_total = 0.1*self.vec_total + 0.9*self.vec_total_prev
		self.vec_total += 0.03*np.random.random(2)


		d = distance(self.my_position,[0,0])
		if d > 0.75:
			q = 0.01
		else:
			q = 0.01
		#my_position += 1.0/distance(vec_total,(0,0)) * vec_total * q
		self.my_position += 1.0/distance(self.vec_total,(0,0)) * self.vec_total * q
		#if distance(my_position_prev,my_position) < q:
		#	my_position+=1.0/distance(vec_total_prev,(0,0)) * vec_total_prev * q
		self.vec_total_prev = self.vec_total.copy()
		self.my_position_prev = self.my_position.copy()

		self.my_position_R = na([0,0])

		a = angle_clockwise(self.vec_total,[0,1])
		self.pts_R = []
		for p in self.pts:
			p = p.copy()
			p -= self.my_position
			p = rotatePoint([0,0],p,-a)
			self.pts_R.append(p)
		self.pts_R = na(self.pts_R)

		plot_rotated = True

		if self.graphics:
			if d > 0: #0.65:
				plt.figure(1)
				plt.clf()
				if not plot_rotated:
					plt.plot(self.pts[:,0],self.pts[:,1],'.')
					#plt.plot([my_position[0],my_position[0]+vec_total[0]/10000.],[my_position[1],my_position[1]+vec_total[1]/10000.],'r-')
					plt.plot(self.my_position[0],self.my_position[1],'go')
				else:
					plt.title(a)
					plt.plot(self.pts_R[:,0],self.pts_R[:,1],'.')
					plt.plot(self.my_position_R[0],self.my_position_R[1],'go')

				plt.xlim(-1.5,1.5)
				plt.ylim(-1.5,1.5)
				plt.pause(0.00333)


		return self.pts_R





def force_function(my_position,object_position):
	dist = distance(my_position,object_position)
	if dist < 0.2:
		f = 1.0/((0.01*dist)**4)#1/(dist+0.01)
	elif dist < 2:
		f = 0.5/((0.01*dist)**4)
	else:
		f = 0.0
	vec = na(my_position) - na(object_position)
	vec *= f
	return vec

def force_function2(my_position,object_position):
	dist = distance(my_position,object_position)
	f = -5*dist
	vec = na(my_position) - na(object_position)
	vec *= f
	return vec



