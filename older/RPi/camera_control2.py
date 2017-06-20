import sys
sys.path.insert(0, "/home/pi")
from kzpy3.utils import *
import picamera
import paramiko

sftp = get_sftp(opjh('/home/pi/pw_MacbookPro.txt'))

camera = picamera.PiCamera()
#camera.hflip = True
#camera.vflip = True
ydim = 224
camera.resolution = (np.int(1.3333*ydim), ydim)

image_path = '/home/pi/image1.jpg'
dst_image_path = '/Users/karlzipser/scratch/2015/11/RPi_images/not_yet_viewed'

camera_on_time = 600
start_time = time.time()
last_time = start_time

ctr = 0
time_sum = 0

while time.time() < start_time + camera_on_time:
	try:
		t = time.time()
		time_sum += t-last_time
		last_time = t
		camera.capture(image_path,format='jpeg', use_video_port=True,quality=10)
		sftp.put(image_path, d2n(dst_image_path,'/',ctr,'.',t,'.jpg'))
		ctr += 1
		if np.mod(ctr,100) == 0:
			print(d2s('Average interval =',time_sum / (1.0*ctr)))

		#sftp.put(image_path, opj(dst_image_path,d2n(ctr,'.jpg')))
	except Exception,e:
		print('\nCleaning up.')
		del camera
		sftp.close()
		transport.close()
		print('Done.')
		print str(e)
		break
    
print('\nCleaning up.')
sftp.close()
transport.close()
print('Done.')
