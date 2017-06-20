"""
animate timelapse frames matrix
"""
from kzpy3.vis import *
from matplotlib.animation import FuncAnimation


n_frames = 3000


def even_frames(frame_number):
	#print(frame_number)
	try:
		img = imread(opjD('image1.jpg'))
		plt.clf()
		mi(img)
	except:
		pass
	if frame_number == n_frames-1:
		plt.close()


fig = plt.figure(1,figsize=(9,9))

animation = FuncAnimation(fig, even_frames, frames=n_frames, interval=30, repeat=False)

plt.show()

print('done....')