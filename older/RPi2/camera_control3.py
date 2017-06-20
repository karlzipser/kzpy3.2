import sys
sys.path.insert(0, "/home/pi")
from kzpy3.utils import *
import picamera
import paramiko

def get_sftp(pw_file_path):
	hup = txt_file_to_list_of_strings(pw_file_path)
	host = hup[0]
	port = 22
	transport = paramiko.Transport((host, port))
	password = hup[2]
	username = hup[1]
	transport.connect(username = username, password = password)
	sftp = paramiko.SFTPClient.from_transport(transport)
	return sftp,transport

sftp,transport = get_sftp(opjh('/home/pi/pw_MacbookPro.txt'))

camera = picamera.PiCamera()
#camera.hflip = True
#camera.vflip = True
ydim = 224
camera.resolution = (np.int(1.3333*ydim), ydim)

image_path = '/home/pi/image1.jpg'
dst_image_path = '/Users/karlzipser/scratch/2015/11/RPi_images/not_yet_viewed'
control_path = '/home/pi/camera_control.txt'

STANDBY = 'STANDBY'
CAPTURE = 'CAPTURE'
QUIT = 'QUIT'
status = STANDBY

ctr = 0
last_status_check_time = time.time()
while status != QUIT:
	try:
		t = time.time()
		if t - last_status_check_time > 1:
			last_status_check_time = t
			s = txt_file_to_list_of_strings(control_path)
			status = s[0]
			print(status)
			#handshake_t = np.load('handshake.npy')
			#if time.time() - handshake_t > 1.0:
			#	print('Handshake lost, closing down GPIOs')
			#	error_cleanup()
		if status == CAPTURE:
			camera.capture(image_path,format='jpeg', use_video_port=True,quality=100)
			sftp.put(image_path, d2n(dst_image_path,'/',ctr,'-',t,'.jpg'))
			print(time.time()-t)
			"""
			for q=10, diff is ~0.13
			for q=100, diff is ~0.15
			"""
			ctr += 1
	except: # Exception,e:
		print('\nCamera or transfer failed, cleaning up, including GPIO.')
		del camera
		sftp.close()
		transport.close()
		sys.exit()
		#print str(e)
		break
print('\nNormal Quit, cleaning up.')
del camera
sftp.close()
transport.close()
print('Done.')


