 
from kzpy3.vis3 import *
from kzpy3.Train_app.Sq_ldr_interval_tester5_modified.Main import get_similarity
from kzpy3.Learn.main import Main6_Output_Object
from kzpy3.Learn.clusters import Clusters,threshold_img

C = Clusters(get_similarity)
M = Main6_Output_Object('pro2pros')


cluster_number = 400
index = 1
threshold = 25
button_number = None


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
		in_imgs = [img,button]
		out_imgs = M['output'](in_imgs)
		img = out_imgs[0]
		#mi(in_imgs[0],5)
		#mi(img,10)
		img_small = cv2.resize( out_imgs[0],(41,23))
		cb('searching for cluster...')
		r = C['find_most_similar_cluster'](img_small,show=False,use_random=False)

		img = C['get_random_img_from_cluster'](r[0])
		img = cv2.resize( img,(168,94))
		in_imgs = [img,button]

		#raw_enter()





#EOF
