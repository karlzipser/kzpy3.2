
class mtrx:
	def __init__(self,name,lst):
		self.data = np.array(lst)
		self.name = name
		self.show()
	def show(self):
		print(self.name)
		print(self.data)
	def multiply(self,B,result_name):
		print('__________________')
		self.show()
		print('\ttimes')
		B.show()
		print '\tequals'
		C = mtrx(result_name,self.data.dot(B.data))
		print('__________________')
		return C
	def plus(self,B,result_name):
		print('__________________')
		self.show()
		print('\tplus')
		B.show()
		print '\tequals'
		C = mtrx(result_name,self.data + B.data)
		print('__________________')
		return C

I = mtrx('I',[[1,0,0],[0,1,0],[0,0,1]])
A = mtrx('A',[[2,1,1],[4,-6,0],[-2,7,2]])
E_ = mtrx('E_',[[0,0,0],[-2,0,0],[0,0,0]])
E_A = E_.multiply(A,'E_A')
EA = E_A.plus(A,'EA')
F_ = mtrx('F_',[[0,0,0],[0,0,0],[1,0,0]])
F_EA = F_.multiply(EA,'F_EA')
FEA = F_EA.plus(EA,'FEA')
G_ = mtrx('G_',[[0,0,0],[0,0,0],[0,1,0]])
G_FEA = G_.multiply(FEA,'G_FEA')
GFEA = G_FEA.plus(FEA,'GFEA')

E = E_.plus(I,'E')
F = F_.plus(I,'F')
G = G_.plus(I,'G')

GFE = G.multiply(F.multiply(E,'FE'),'GFE')

U = GFE.multiply(A,'U')

b = mtrx('b',[[5],[-2],[9]])

c = GFE.multiply(b,'c')

Ei = mtrx('Ei',[[1,0,0],[2,1,0],[0,0,1]])
Fi = mtrx('Fi',[[1,0,0],[0,1,0],[-1,0,1]])
Gi = mtrx('Gi',[[1,0,0],[0,1,0],[0,-1,1]])

L = Ei.multiply(Fi.multiply(Gi,'FiGi'),'L')

D = mtrx('D',[[2,0,0],[0,-8,0],[0,0,1]])
Uu = mtrx('Uu',[[2/2.,1/2.,1/.2],[0,8/8.,2/8.],[0,0,1]])
D.multiply(Uu,'DUu');

L.multiply(D.multiply(Uu,'DUu'),'LDUu');



N = mtrx('N',[[1,2,3],[4,5,6],[7,8,9]])
P1 = mtrx('P1',[[0,0,1],[0,0,0],[0,0,1]])
P1.multiply(N,'P1N');

V = mtrx('V',[[4],[5]])
R = mtrx('R',[[1,2],[3,4],[5,6]])
R.multiply(V,'RV');

V = mtrx('V',[[4,5,6]])
R = mtrx('R',[[1,2],[3,4],[5,6]])
V.multiply(R,'VR');




# http://www.wikihow.com/Calculate-Pi
_pi = 0
sign = 1.0
N = 100000000
for i in range(1,N,2):
	_pi += sign * 4/(1.*i)
	if sign == 1:
		sign = -1
	else:
		sign = 1

print _pi
print np.pi - _pi






