

class Xi():
	def __init__(self, A={} ):
		B = {
			'a':1,
			'b':2,
		}
		set_Defaults(B, A)
		for a in A:
			self.__dict__[a] = A[a]
		#kprint(self.__dict__,title='self.__dict__')
	def show(self,name='',space=0,start=True):
		if start:
			print name+' <'+self.__class__.__name__+'>'
		s = space * ' '
		for a in sorted(self.__dict__.keys()):
			if isinstance(self.__dict__[a],Xi):
				print s+a+' <'+self.__dict__[a].__class__.__name__+'>'
				self.__dict__[a].show(space=space+4,start=False)
			else:
				c = self.__dict__[a]
				if type(c) == np.ndarray:
					c = d2s(shape(c),'<array>')
				elif type(c) == list:
					c = str(c)
					if len(c) > 40:
						c = c[:40] + ' . . .'
					c += ' <list>'
					#c = self.__dict__[a]
				print s+a,c

class Xj(Xi):
	def __init__(self, A={} ):
		Xi.__init__(self,A)




A0 = Xi(
		{
			'a':9,
			'z':66,

		}
	)

A1 = Xj({'A0':A0,'g':(range(400))})

A2 = Xj({'A1':A1,'xxxx':zeros((10,10,10))})

A2.show(name='A2',space=4)

print A2.A1.A0.z
# print A2['A1']['A0']['z']
#EOF


