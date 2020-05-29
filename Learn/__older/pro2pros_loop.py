 
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

if True:
	I = {
		'cluster_img':[],
		'world_img':[],
		'prediction_img':[],
		'cluster_avg_img':[],
		'button':[],
	}

	img = C['get_img'](cluster_number,index)

	CA()
	img = cv2.resize( img,(168,94))
	for i in range(100):
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

		for j in range(10):

			#raw_enter()
			in_imgs = [img,button]
			I['button'].append(button)
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
