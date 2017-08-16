"""
animate random matrix
"""
from kzpy3.vis import *
from matplotlib.animation import FuncAnimation

fig = plt.figure(figsize=(9,9))

n_frames = 100
rnd = np.random.random((n_frames,512,512))
def update2(frame_number):
	print(frame_number)
	plt.clf()
	mi(rnd[frame_number,:,:])
	if frame_number == n_frames-1:
		plt.close()

animation = FuncAnimation(fig, update2, frames = n_frames, interval=30, repeat=False)

plt.show()

print('done.')