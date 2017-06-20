"""
animate timelapse frames matrix
"""
from kzpy3.vis import *
from matplotlib.animation import FuncAnimation


frames = load_img_folder_to_list(opjh('Desktop/DATA/VIEWED'))# 'scratch/2015/11/RPi_images/viewed'))# 'scratch/2015/10/8/timelapse.1444316394'))
n_frames = len(frames)



def even_frames(frame_number):
	print(frame_number)
	plt.clf()
	mi(frames[frame_number])
	if frame_number == n_frames-1:
		plt.close()


fig = plt.figure(1,figsize=(9,9))

animation = FuncAnimation(fig, even_frames, frames=n_frames, interval=3, repeat=False)

plt.show()

print('done....')


