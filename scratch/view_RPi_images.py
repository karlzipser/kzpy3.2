"""
python kzpy3/scratch/view_RPi_images.py
"""
from kzpy3.vis import *
from matplotlib.animation import FuncAnimation


n_frames = 3000

c = 0
ctr = 0

def even_frames(frame_number):
	global c
	global ctr
	#print(frame_number)

	start_time = time.time()
	try:
		#c_new = os.path.getctime(opjD('image1.jpg'))
		#if c_new == c:
		#	pass #print('waiting...')
		#else:
		#c = c_new
		#unix(d2n('cp ',opjD('image1.jpg '),' /Users/karlzipser/Desktop/RPi_images/',c_new,'.',ctr,'.jpg'),False)
		#ctr += 1
		#print ctr
		img = imread(opjD('image1.jpg'))
		#print(shape(img))
		if shape(img)[2] == 3:
			plt.clf()
			mi(img)
		else:
			print('Empyt frame.')
	except KeyboardInterrupt:
		print('Quitting now.')
		sys.exit(1)
	except:
		pass
	#if frame_number == n_frames-1:
	#	plt.close()


fig = plt.figure(1,figsize=(9,9))

animation = FuncAnimation(fig, even_frames, frames=n_frames, interval=30, repeat=False)

plt.show()
#input('adfa')
print('done....')