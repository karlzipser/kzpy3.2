from kzpy3.vis import *
from kzpy3.teg1.rosbag_work.get_data_from_bag_files import *

bag_folder_path = '/home/karlzipser/Desktop/bair_car_data/direct_7Sept2016_Mr_Orange_Tilden'

d = Bair_Car_Recorded_Data(bag_folder_path,10,['steer','motor','encoder','acc','gyro'],2)



while True:
	data = d.get_data('bgr8')
	if data == 'END' :
		print """data = 'END':"""
		break
	if 'left' in data:
		if type(data['left'][0]) == np.ndarray:
			
			target_data = data['steer']
			target_data += data['motor']
			"""
			target_data += data['encoder']
			acc = [item for sublist in data['acc'] for item in sublist]
			target_data += acc
			gyro = [item for sublist in data['gyro'] for item in sublist]
			target_data += gyro
			"""
			print target_data

			cv2.imshow('left',data['left'][0])
			cv2.imshow('right',data['left'][1])
			if cv2.waitKey(1) & 0xFF == ord('q'):
			    pass
			plt.pause(1/30.)

		else:
			print """not if type(data['left']) == np.ndarray: """+str(time.time())
	else:
		print """not if 'left' in data: """+str(time.time())



