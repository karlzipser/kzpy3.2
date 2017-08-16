from kzpy3.utils import *
import socket

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 5007))
for i in range(1000):
	buf = '('+time_str()+')'
	while len(buf)<64:
		buf += '?'
	assert len(buf) == 64
	clientsocket.send(buf)
	time.sleep(0.1)

