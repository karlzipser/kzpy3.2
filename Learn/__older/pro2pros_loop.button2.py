 
from kzpy3.vis3 import *
from kzpy3.Train_app.Sq_ldr_interval_tester5_modified.Main import get_similarity
from kzpy3.Learn.main import Main6_Output_Object
from kzpy3.Learn.clusters import Clusters,threshold_img

C = Clusters(get_similarity)
Pro2pros = Main6_Output_Object('pro2pros')
ProRgb2rgb = Main6_Output_Object('proRgb2rgb')

path = opjD('Destkop_clusters_and_not_essential_24July2019')
cluster_averages = lo(opj(path,'cluster_averages.pkl'))


cluster_number = 400
index = 1
threshold = 25
button_number = None







I = loD('I_second_pass.pkl')


Colors = {
    0:(255,0,0),
    1:(0,255,0),
    2:(0,0,255)
}


e = 0.5#0.1
def trajectory_curves(img):
	img = cv2.resize(img,(168,94))
	img2=img.copy() * 0
	h,w,d = shape(img)
	for z in range(d):
	    a,a_prev = None,None
	    pt = None
	    for y in range(h/2+6,h-5):
	        if a != None:
	            a_prev = b
	        a = np.argsort(img[y,:,z])[-1]
	        if a_prev == None:
	            a_prev = a
	        #print(a)
	        #print a,a_prev,b
	        b = int(e*a + (1-e)*(a_prev))
	        if pt == None:
	            pt = (b,y)
	        s = int((y**2/47./3.)/10)
	        #print s
	        cv2.line(img2,pt,(b,y),Colors[z],s)
	        pt = (b,y)
	return img2


def ppercent(i,total,n=100,s='charlie: '):
	if i % n == 0:
		clp(s,int(100.0 *i/(1.0*total)),'%',s0='')

#world_img = I['world_img'][-1]


#mi(world_img)

I['world_img_with_traj'] = []
timer = Timer(5)
l = len(I['cluster_avg_img'])

I['world_img_with_traj'] = []
for i in rlen(I['cluster_avg_img']):
	if i % 100 == 0:
		print i,l
	img = I['prediction_img'][i]
	world_img = I['world_img'][i].copy()
	timer.message(d2s(int(100*i/(1.0*l)),'%'))
	img2 = trajectory_curves(img)
	h,w,d = shape(img2)
	for y in range(h):
		for x in range(w):
			for z in range(d):
				if img2[y,x,z] == 255:
					world_img[y,x,:] = Colors[z]
	I['world_img_with_traj'].append(world_img)
	#mci(world_img,scale=4);#spause();time.sleep(30/1000.)




for i in rlen(I['world_img_with_traj']):
	imsave(opjD('imgs',d2p(i,'png')),I['world_img_with_traj'][i])

for i in rlen(I['cluster_avg_img']):
	imsave(opjD('imgs2',d2p(i,'png')),I['cluster_avg_img'][i])












if True:



	I = {
		'cluster_img':[],
		'world_img':[],
		'prediction_img':[],
		'cluster_avg_img':[],
		'button':[],
		'button_number':[],
	}

	img = C['get_img'](cluster_number,index)
	img = cv2.resize( img,(168,94))
	button = 0*img.astype(float)
	button0 = button.copy()
	button1 = button.copy()
	button2 = button.copy()
	button0[:,:,0] = 1
	button1[:,:,1] = 1
	button2[:,:,2] = 1	
	B = {
		0:button0,
		1:button1,
		2:button2,
	}
	button = B[1].copy()
	CA()
	
	s = 0.90
	for i in range(30*3):
		button_number = rndchoice([0,1,2])


		for j in range(20):
			button = s * button + (1-s) * B[button_number]
			print button_number,button[0,0,:]
			#button = 0.1*button/(1.0*button.sum()) * 15792.0
			in_imgs = [img,button]
			I['button'].append(button)
			I['button_number'].append(B[button_number])
			out_imgs = Pro2pros['output'](in_imgs)
			img = out_imgs[0]
			I['prediction_img'].append(img)
			#mi(in_imgs[0],5)
			#mi(img,10)
			img_small = cv2.resize( out_imgs[0],(41,23))
			cb('searching for cluster...')
			r = C['find_most_similar_cluster'](img_small,show=False,use_random=False)
			r0 = r[0]
			img = C['get_random_img_from_cluster'](r0)
			img = cv2.resize( img,(168,94))
			in_imgs = [img,button]
			noise = 50 * rnd((23,41,3)) - 50/2.
			img_small = 1.0 * cv2.resize( img,(41,23)) + noise
			img_noise = cv2.resize( img_small,(168,94))
			world_img = ProRgb2rgb['output']([0*img_noise,img_noise])[0]
			cv2.waitKey(33)
			I['cluster_img'].append(img)
			I['world_img'].append(world_img)
			I['cluster_avg_img'].append(cluster_averages[r0])
			mi(img,'cluster_img');spause()
			mi(world_img,'world_img');spause()
			mi(I['cluster_avg_img'][-1],'cluster_avg_img');spause()
	

if False:
	I = {
		'in_img':[],
		'cluster_img':[],
		'img_noise':[],
		'rgb_img':[],
		'button':[],
		'button_show':[],
		'button_number':[],
		'out_img':[],
	}

	cluster_img = C['get_img'](cluster_number,index)
	in_img = cv2.resize( cluster_img,(168,94))
	blank = 0 * in_img

	I['in_img'].append(in_img)
	I['button_number'] = 1

	#def step(I):

	in_img = I['in_img'][-1]

	button = blank.copy()
	button[:,:,I['button_number']] = 1
	I['button_show'].append(255 * button)

	out_img = Pro2pros['output']([in_img,button])[0]

	img_small = cv2.resize( out_img,(41,23))

	r = C['find_most_similar_cluster'](img_small,show=False,use_random=False)

	cluster_img = C['get_random_img_from_cluster'](r[0])

	new_in_img = cv2.resize( cluster_img,(168,94))

	noise = 50. * rnd((23,41,3)) - 50/2.

	#img_small = cluster_img + noise
	img_small = z55(cluster_img.astype(float) + noise.astype(float))
	img_noise = cv2.resize( img_small,(168,94))

	rgb_img = ProRgb2rgb['output']([blank,img_noise])

	I['in_img'].append(new_in_img)
	I['out_img'].append(out_img)
	I['cluster_img'].append(cluster_img)
	I['img_noise'].append(img_noise)
	I['rgb_img'].append(rgb_img)
	I['button'].append(button)

	def show(I):
		for k in I:
			if k != 'button_number':
				mi(I[k][-1],k,img_title=k)	

#EOF
