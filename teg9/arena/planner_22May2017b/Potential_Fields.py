from kzpy3.utils import *
pythonpaths(['kzpy3','kzpy3/teg9'])
from vis import *
from data.utils.general import car_colors as colors




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
			#print(mode,length(xy-xy_our))
			if mode=='Follow_Arena_Potential_Field' and length(xy-xy_our)>1.5:
				continue
			sub_add_list.append([5/6.5*gau_car,array(xy)])
			sub_add_list.append([5/6.5*gau_marker,array(xy)])
		D['sub_add'](sub_add_list)
	D['other_cars'] = _other_cars
	return D


def Play_Arena_Potential_Field(origin,mult,markers):
	D = Arena_Potential_Field(origin,mult,markers)
	D['type'] = 'Play_Arena_Potential_Field'
	gau_center = Gaussian_2D(6*mult)
	for xy in markers['xy']:
		D['add'](gau_center,xy)
	D['previous_additions'] = []
	return D

def Follow_Arena_Potential_Field(origin,mult,markers):
	D = Arena_Potential_Field(origin,mult,markers)
	D['type'] = 'Follow_Arena_Potential_Field'
	D['other_cars_parent'] = D['other_cars']
	def _other_cars(xy_list,mode,xy_our):
		D['other_cars_parent'](xy_list,mode,xy_our)
	D['other_cars'] = _other_cars
	return D

def Direct_Arena_Potential_Field(origin,mult,markers):
	D = Arena_Potential_Field(origin,mult,markers)
	D['type'] = 'Direct_Arena_Potential_Field'
	gau_marker = Gaussian_2D(mult)
	gau_s = Gaussian_2D(0.24*mult)
	gau_center = Gaussian_2D(6*mult)
	gau_follow = Gaussian_2D(12*mult)
	gau_car = Gaussian_2D(6*mult)
	for xy in markers['xy']:
		D['add'](-1.0*gau_marker,0.75*(array(xy)))
	D['add'](4*gau_center,[0,0])
	D['previous_additions'] = []
	return D


def Furtive_Arena_Potential_Field(origin,mult,markers):
	D = Arena_Potential_Field(origin,mult,markers)
	D['type'] = 'Furtive_Arena_Potential_Field'
	gau_marker = Gaussian_2D(mult)
	gau_s = Gaussian_2D(0.24*mult)
	gau_center = Gaussian_2D(6*mult)
	gau_follow = Gaussian_2D(12*mult)
	gau_car = Gaussian_2D(6*mult)
	for xy in markers['xy']:
		D['add'](-1.0*gau_marker,0.92*(array(xy)))
	D['add'](4*gau_center,[0,0])
	D['previous_additions'] = []
	return D





