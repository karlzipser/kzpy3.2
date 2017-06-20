# $ python kzpy3/teg1/rosbag_work/example_of_accessing_data.py  
from kzpy3.vis import *
from kzpy3.teg1.rosbag_work.get_data_from_bag_files3 import *

path = '/media/your_computer/rosbags/bair_car_data'
path = '/home/karlzipser/Desktop/Old_Desktop/bair_car_rescue/bair_car_data'
path = opjD('temp_bags_saved')
# The two variables below exist because it is time consuming
# to randomly access from all the bag files. It is faster to open a
# file and sample it several times. Likewise, each folder has metadata
# to be opened.
# Thus, from a given
# run, a certain number of bag files will be sampled, and
# from each a certain number of samples will be taken. Choose whatever
# values you want. If sequence order is not important, you can make the 
# value large. Once the max is reached, the objects reset. It doesn't
# mean you can't access the same data more than once.
# Note that bag files are abou 30s long. I make no attempt to splice them.
# Thus, if you request 29s long samples, they will be very similar.
# I am working on a much shorter time scale so I was not worried about this.

num_bag_files_to_sample_from_given_run = 10
num_samples_from_given_bag_file = 10

num_frames = 30 * 3 # three seconds

topics = ['state','encoder','steer','motor','gyro','acc'] # images not included in this list

data_object = Bair_Car_Data(path, num_bag_files_to_sample_from_given_run, num_samples_from_given_bag_file)
plt.ion()
#while True :
#	if True:
for i in range(10000):
	a_data_sequence = data_object.get_data(topics, num_frames, num_frames)

	print a_data_sequence.keys()

	# There are no timestamps in this representation. It is assumed
	# that the framerate is 30 Hz (good approximation).
	# All the data are syncronized to the left images.

	assert(len(a_data_sequence['acc']) == num_frames)

	assert(len(a_data_sequence['left']) == num_frames)

	plt.figure('acc')
	plt.clf()
	plt.figure('acc')

	plt.plot(a_data_sequence['acc'])
	plt.plot(a_data_sequence['state'])
	plt.plot(np.array(a_data_sequence['steer'])/10.)
	for j in range(num_frames):
		mi(a_data_sequence['left'][j],'left',img_title=str(j))
		plt.pause(0.01)
	#	else:
	#		pass