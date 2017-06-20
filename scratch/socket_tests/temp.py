from kzpy3.utils import *

ports = serial_ports()
print ports
slist = []
BAUD = 115200
TIMEOUT = 0.01

for p in ports:
	if 'tty.usbmodem' in p or 'ttyACM' in p:
		print "Arduino port:" + p
		slist.append(serial.Serial(p,BAUD,timeout=TIMEOUT))

if len(slist) > 0:
	while True:
		for s in slist:
			d = s.readline()
			#print  (len(d),type(d))
			if '(' in d:#len(d) > 1:
				print d
			time.sleep(0.0)
else:
	print 'no Arduino ports!!!'


for s in slist:
    s.close()


# http://www.tutorialspoint.com/python/python_multithreading.htm


# http://jessenoller.com/blog/2009/02/01/python-threads-and-the-global-interpreter-lock