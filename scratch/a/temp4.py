from kzpy3.utils import *

def temp4(c):
	f = '/Users/karlzipser/Desktop/temp.py'
	t = txt_file_to_list_of_strings(f)
	ctr = 0
	u = '\n'.join(t)
	v = u.split('############\n')
	print('###########\n')
	print(v[c])
	d = raw_input('########### Do this? ')
	if d == 'y':
		exec(v[c],globals())


from kzpy3.teg2.data.access.get_data_from_bag_files6 import * 
#B=Bag_Folder('/media/karlzipser/ExtraDrive1/bair_car_data_min_disks/bair_car_data_6_min/caffe_z2_direct_local_sidewalks_28Sep16_08h06m57s_Mr_Orange'  )
B=Bag_Folder('/media/karlzipser/ExtraDrive1/bair_car_data_min_disks/bair_car_data_4_min/caffe_z2_direct_local_Tilden_22Sep16_14h31m11s_Mr_Orange')
data = 'timecourse data'
plt.figure(data);plt.clf()
ts = B.data['timestamps']
plt.figure(data);
topics = sorted(B.data.keys())

ctr = 6.0
legend_handles = []
for tp in topics:
	if tp != 'timestamps':
		legend_handles.append(z2o_plot(ts,B.data[tp],ctr,'.',tp)[0])
		ctr -= 0.5
plt.legend(handles=legend_handles)

plt.figure('scatter')
b=B.data['state_one_steps']
plt.plot(B.data['steer'][b>0],B.data['gyro_x'][b>0],'.')




t0 = time.time()
for i in range(100):
	unix('scp /home/karlzipser/Pictures/bay2.png /home/karlzipser/',False) # 0.97 s
	#unix('scp /home/karlzipser/Pictures/bay2.png /media/karlzipser/ExtraDrive1/',False) # 1.46 s
print time.time()-t0






def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

a = 0.65
b = (-1+a)**2
c = 0.75
d = 1/2.0
e = 0
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
	#y[y>2.0] = 2.0
	return y

x = arange(-4,4.1,0.1)
xn = x.copy()
for i in range(len(x)):
	if x[i] > 0:
		x[i] *= 1.9

y = f(x,a,b,c,d,e)
for i in range(len(xn)):
	if xn[i] > 1.5:
		y[i] *= 0.1
clf();xylim(-4,4,0,1);plot(xn,y);pause(0.01)


def f_asym(xy,a,b,c,d,e):
	x = xy[0]
	y = xy[1]
	l = np.sqrt(x**2+y**2)
	if x > 0:
		l *= 1.9
	g = c*gaussian(l/R,0,d)
	ga = c*gaussian(a,0,d)

	if l/R < -a:
		z = (l/R+a)**2 / b
	elif l/R > a:
		z = (l/R-a)**2 / b
	else:
		z = g - ga
	z = (1-e)*z + e
	if x > 1.5:
		z *= 0.1
	return z


x = arange(-4,4.1,0.1)

y = []
for i in range(len(x)):
	y.append(f_asym([3,x[i]],a,b,c,d,e))
figure(2);clf();xylim(-4,4,0,1);plot(x,y);pause(0.01)



Origin = int(2*1000/300.*300 / 5)
Mult = 1000/300.*50 / 5

arena = Direct_Arena_Potential_Field(Origin,Mult,None)
img=zaccess(arena,[0,2]);mi(img,2);pause(0.001)

img2 = 0*img.copy()
for x in range(2*Origin):
	for y in range(2*Origin):
		xn = x
		yn = y
		if x > Origin:
			xn = int(x-Origin)*1.9+Origin
		if y > Origin:
			yn = int(y-Origin)*1.3+Origin
		if y < Origin:
			yn = int(Origin-y)*1.3+Origin
		if xn < 2*Origin and yn < 2*Origin:
			img2[x,y] = img[xn,yn]
		#else:
		#	img2[x,y] = img[x,y]
mi(img2);pause(0.01)


	def _fill_in_potential_field(a,b,c,d,e,warp_image=True):
		D['Image']['img'] *= 0
		for x in range(0,2*origin):
			for y in range(0,2*origin):
				xyf = D['Image']['pixel_to_float']((x,y))
				l = length((xyf[0],xyf[1]))
				if l < 1.9*5:
				img = 0.75*f(l,a,b,c,d,e)
		if warp_image:
			img2 = 0*img.copy()
			for x in range(2*origin):
				for y in range(2*origin):
					xn = x
					yn = y
					if x > Origin:
						xn = int(x-origin)*1.9+origin
					if y > Origin:
						yn = int(y-origin)*1.3+origin
					if y < Origin:
						yn = int(origin-y)*1.3+origin
					if xn < 2*origin and yn < 2*origin:
						img2[x,y] = img[xn,yn]
			D['Image']['img'][x][y] = img2
		else:
			D['Image']['img'][x][y] = img
	D['fill_in_potential_field'] = _fill_in_potential_field
	return D

