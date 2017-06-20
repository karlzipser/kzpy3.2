print "Client Side:"

from kzpy3.utils import *
import socket

host = '127.0.0.1' # 'localhost'
port = 5000



clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((host, port))

s = ''

while s != 'q':
	s = raw_input()
	clientsocket.send(s)

clientsocket.close()


