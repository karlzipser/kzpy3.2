from kzpy3.utils import *
from kzpy3.misc.progress import *

pb = ProgressBar(1000)

c = 0

ctr = 0
for i in range(1000):
	try:
		#unix("rsync -a pi@10.0.0.25:/home/pi/Desktop/image1.jpg "+opjD(''),print_stdout=False)
		unix("rsync -a pi@192.168.43.20:/home/pi/Desktop/image1.jpg "+opjD(''),print_stdout=False)
		c_new = os.path.getctime(opjD('image1.jpg'))
		if c_new == c:
			pass#print('waiting...')
		else:
			c = c_new
			pb.animate(ctr)
			ctr += 1
			#print('New image!')
	except:
		print('Image not found, will try again . . .')
	time.sleep(0.5)
		