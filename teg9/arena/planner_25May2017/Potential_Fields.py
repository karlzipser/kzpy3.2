from kzpy3.utils import *
pythonpaths(['kzpy3','kzpy3/teg9'])
from vis import *
from data.utils.general import car_colors as colors







def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))


R = 4*107/100.0
def f(x,a,b,c,d,e):
	if is_number(x):
		x = array([x])
	g = c*gaussian(x/R,0,d)
	ga = c*gaussian(a,0,d)
	y = 0*x
	for i in range(len(x)):
		if x[i]/R < -a:
			y[i] = (x[i]/R+a)**2 / b
		elif x[i]/R > a:
			y[i] = (x[i]/R-a)**2 / b
		else:
			y[i] = g[i] - ga
	y = (1-e)*y + e
	y[y>2.0] = 2.0
	return y









def Potential_Field(xy_sizes,origin,mult):
	D = {}
	D['Purpose'] = d2s(inspect.stack()[0][3],':','Potential field for path planning.')
	D['Image'] = Image(xy_sizes,origin,mult,data_type=np.float)
	D['previous_additions'] = []
	def _sub_add(additions):
		for p in D['previous_additions']:
			isub(p[0],D['Image']['img'],p[1])
		D['previous_additions'] = []
		for a in additions:
			D['add'](a[0],a[1])
	def _add(addition,xy):
		xy_pixels = D['Image']['floats_to_pixels'](xy)
		iadd(addition,D['Image']['img'],xy_pixels)
		D['previous_additions'].append([addition,xy_pixels])
	D['sub_add'] = _sub_add
	D['add'] = _add
	return D




def Arena_Potential_Field(origin,mult,markers):
	xy_sizes = [2*origin,2*origin]
	D = Potential_Field(xy_sizes,origin,mult)
	D['Purpose'] = d2f('\n',d2s(inspect.stack()[0][3],':','Potential field specific for arena.'),D['Purpose'])
	gau_marker = Gaussian_2D(mult)
	gau_s = Gaussian_2D(0.24*mult)
	gau_center = Gaussian_2D(6*mult)
	gau_follow = Gaussian_2D(12*mult)
	gau_car = Gaussian_2D(6*mult)
	if False:
		for xy in markers['xy']:
			D['add'](gau_marker,xy)
			#D['add'](-1.0*gau_s,xy)
			D['add'](2*gau_marker,1.05*(array(xy)))
			D['add'](3*gau_marker,1.1*(array(xy)))
			D['add'](4*gau_marker,1.15*(array(xy)))
	D['previous_additions'] = []
	def _test(iterations=1,Graphics=True):
		timer = Timer(0)
		ctr = 0
		for i in range(iterations):
			print (dp(timer.time(),2),ctr)
			for xy in markers['xy']:
				ctr += 1
				D['sub_add']([[-15*gau_follow,0.75*(array(xy))],[10*gau_marker,0.75*(array(xy))]])
				if Graphics:
					img = D['Image']['img']
					width = shape(img)[0]
					mi(img[width/2-origin/2:width/2+origin/2,width/2-origin/2:width/2+origin/2],1)
					figure(2);clf();plot(a['Image']['img'][Origin,:],'o-');pause(0.0001)
		print timer.time()
		print ctr
	D['test'] = _test
	def _other_cars(xy_list,mode,xy_our):
		sub_add_list = []
		for xy in xy_list:
			if mode=='Follow_Arena_Potential_Field' and length(xy-xy_our)>1.5:
				continue
			sub_add_list.append([5/6.5*gau_car,array(xy)])
			sub_add_list.append([5/6.5*gau_marker,array(xy)])
		D['sub_add'](sub_add_list)
	D['other_cars'] = _other_cars
	def _fill_in_potential_field(a,b,c,d,e):
		D['Image']['img'] *= 0
		for x in range(0,2*origin):
			for y in range(0,2*origin):
				xyf = D['Image']['pixel_to_float']((x,y))
				l = length((xyf[0],xyf[1]))
				if l < 5:
					D['Image']['img'][x][y] = 0.75*f(l,a,b,c,d,e)
	D['fill_in_potential_field'] = _fill_in_potential_field
	return D


def Play_Arena_Potential_Field(origin,mult,markers):
	D = Arena_Potential_Field(origin,mult,markers)
	D['type'] = 'Play_Arena_Potential_Field'
	if False:
		gau_center = Gaussian_2D(6*mult)
		for xy in markers['xy']:
			D['add'](gau_center,xy)
	D['previous_additions'] = []
	a = 0.0
	b = (-1+a)**2
	c = 0.0
	d = 1/2.0
	e = 0	
	D['fill_in_potential_field'](a,b,c,d,e)
	return D

def Follow_Arena_Potential_Field(origin,mult,markers):
	D = Arena_Potential_Field(origin,mult,markers)
	D['type'] = 'Follow_Arena_Potential_Field'
	D['other_cars_parent'] = D['other_cars']
	def _other_cars(xy_list,mode,xy_our):
		D['other_cars_parent'](xy_list,mode,xy_our)
	D['other_cars'] = _other_cars
	a = 0.0
	b = (-1+a)**2
	c = 0.0
	d = 1/2.0
	e = 0.5
	D['fill_in_potential_field'](a,b,c,d,e)
	return D

def Direct_Arena_Potential_Field(origin,mult,markers):
	D = Arena_Potential_Field(origin,mult,markers)
	D['type'] = 'Direct_Arena_Potential_Field'
	if False:
		gau_marker = Gaussian_2D(mult)
		gau_s = Gaussian_2D(0.24*mult)
		gau_center = Gaussian_2D(6*mult)
		gau_follow = Gaussian_2D(12*mult)
		gau_car = Gaussian_2D(6*mult)
		for xy in markers['xy']:
			D['add'](-1.0*gau_marker,0.75*(array(xy)))
		D['add'](4*gau_center,[0,0])
	D['previous_additions'] = []
	a = 0.85
	b = (-1+a)**2
	c = 0.75
	d = 1/2.0
	e = 0
	D['fill_in_potential_field'](a,b,c,d,e)
	return D


def Furtive_Arena_Potential_Field(origin,mult,markers):
	D = Arena_Potential_Field(origin,mult,markers)
	D['type'] = 'Furtive_Arena_Potential_Field'
	if False:
		gau_marker = Gaussian_2D(mult)
		gau_s = Gaussian_2D(0.24*mult)
		gau_center = Gaussian_2D(6*mult)
		gau_follow = Gaussian_2D(12*mult)
		gau_car = Gaussian_2D(6*mult)
		for xy in markers['xy']:
			D['add'](-1.0*gau_marker,0.92*(array(xy)))
		D['add'](4*gau_center,[0,0])
	D['previous_additions'] = []
	a = 0.93
	b = (-1+a)**2
	c = 2.0
	d = 1/1.5
	e = 0
	D['fill_in_potential_field'](a,b,c,d,e)
	return D





