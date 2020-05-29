 

path = opjD('Destkop_clusters_and_not_essential_24July2019')
affinity = lo(opj(path,'affinity'))
cluster_list = lo(opj(path,'cluster','cluster_list_25_1st_pass_11April2019_bkp.pkl'))



from kzpy3.Learn.get_data.runs import All_runs
from kzpy3.Learn.get_data.ConDecon_Fire import setup

P = {'type':[0,'Fire3']}
P['runs'] = 'train'
setup(P)



s = zeros((94,168,3))
cl = cluster_list[400]
print len(cl)
for e in cl:
	r,i = e['name'],e['index']
	if r in All_runs['train']:
		Rs = P['Runs'][r]
		left_images = Rs['original_timestamp_data']['data']['left_image']['vals']
		#print r
		img = left_images[i]
		#mi(img,r)
		s += img

mi(z55(s),'s')



from skimage.measure import compare_ssim 

s,d = compare_ssim(s1[:,:,0],z55(rnd((94,168))),full=True)



scores = []
ctr = 0
for e in cl:
	r,i = e['name'],e['index']
	if r in All_runs['train']:
		Rs = P['Runs'][r]
		left_images = Rs['original_timestamp_data']['data']['left_image']['vals']
		#print r
		img = left_images[i]
		if ctr == 10:
			ref = img.copy()
		if ctr > 0:
			s,d = compare_ssim(ref,img,full=True,multichannel=True)
			scores.append((s,r,i))		
		ctr += 1
		
for s in scores:
	if s[0] > 0.3:
		r,i = s[1],s[2]
		img = P['Runs'][r]['original_timestamp_data']['data']['left_image']['vals'][i]
		mi(img,d2s(r,i,s))










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




#for i in rlen(I['world_img_with_traj']):
#	imsave(opjD('imgs',d2p(i,'png')),I['world_img_with_traj'][i])








for n in range(1024):
	s = zeros((94,168,3))
	cl = cluster_list[n]
	print len(cl)
	tc = trajectory_curves(I['cluster_avg_img'][n])
	for e in cl:
		r,i = e['name'],e['index']
		if r in All_runs['train']:
			Rs = P['Runs'][r]
			left_images = Rs['original_timestamp_data']['data']['left_image']['vals']
			#print r
			img = left_images[i]
			#mi(img,r)
			s += img
	s = z55(s)
	h,w,d = shape(s)
	for y in range(h):
		for x in range(w):
			for z in range(d):
				if tc[y,x,z] == 255:
					s[y,x,:] = Colors[z]

	mi(s,'s');raw_enter()
	imsave(opjD('cluster_images_with_world',str(n)+'.png'),z55(s))


#EOF

