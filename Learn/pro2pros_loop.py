 
from kzpy3.vis3 import *
from kzpy3.Train_app.Sq_ldr_interval_tester5_modified.Main import get_similarity
from kzpy3.Learn.main import Main6_Output_Object
from kzpy3.Learn.clusters import Clusters,threshold_img

C = Clusters(get_similarity)
Pro2pros = Main6_Output_Object('pro2pros')
ProRgb2rgb = Main6_Output_Object('proRgb2rgb')


cluster_number = 400
index = 1
threshold = 25
button_number = None

"""
img = C['get_img'](cluster_number,index)

CA()
img = cv2.resize( img,(168,94))
for i in range(10):
	button_number = rndchoice([0,1,2])
	if False:
		while type(button_number) != int:
			try:
				button_number = input('button number >')
				assert type(button) == int
			except:
				cr('try again')
	button = 0*img
	button[:,:,button_number] = 1
	#in_imgs = [img,button]
	for j in range(10):
		raw_enter()
		in_imgs = [img,button]
		out_imgs = Pro2pros['output'](in_imgs)
		img = out_imgs[0]
		#mi(in_imgs[0],5)
		#mi(img,10)
		img_small = cv2.resize( out_imgs[0],(41,23))
		cb('searching for cluster...')
		r = C['find_most_similar_cluster'](img_small,show=False,use_random=False)

		img = C['get_random_img_from_cluster'](r[0])
		img = cv2.resize( img,(168,94))
		in_imgs = [img,button]
		noise = 50 * rnd((23,41,3)) - 50/2.
		img_small = 1.0 * cv2.resize( img,(41,23)) + noise
		img_noise = cv2.resize( img_small,(168,94))
		rgb_img = ProRgb2rgb['output']([0*img_noise,img_noise])[0]
		cv2.waitKey(33)
		mi(img,99)
		mi(rgb_img,100)
		spause()
"""		


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

def step(I):

	in_img = I['in_img'][-1]

	button = blank.copy()
	button[:,:,button_number] = 1
	I['button_show'].append(255 * button)

	out_img = Pro2pros['output']([in_img,button])[0]

	img_small = cv2.resize( out_img,(41,23))

	r = C['find_most_similar_cluster'](img_small,show=False,use_random=False)

	cluster_img = C['get_random_img_from_cluster'](r[0])

	new_in_img = cv2.resize( cluster_img,(168,94))

	noise = 50. * rnd((23,41,3)) - 50/2.

	img_small = cluster_img + noise

	img_noise = cv2.resize( img_small,(168,94))

	rgb_img = ProRgb2rgb['output']([blank,img_noise])[0]

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
