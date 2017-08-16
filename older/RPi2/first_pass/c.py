"Run d.py, then c.py, then keypress_rain.py or b.py"

from kzpy3.utils import *
import socket


host = '127.0.0.1' # 'localhost'
port = 5000
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((host, port))
serversocket.listen(5) # become a server socket, maximum 5 connections
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((host, 5001))
connection, address = serversocket.accept()


def process_buf(buf):
    print buf
    if buf == 'q':
        return 'q'
    r = 'X'
    if buf == 'left':
        r = '(40,7.5)'
    elif buf == 'right':
        r = '(40,11.0)'
    elif buf == 'up':
        r = '(40,9.0)'
    elif buf == ' ':
        r = '(41,9.0)'
    return r





print("c.py Server/Client Side:")
while True:
    buf = connection.recv(64)
    print(d2s("Received:",buf))
    if len(buf) > 0:
        clientsocket.send(process_buf(buf))
        if buf == 'q':
            time.sleep(0.1)
            break       

clientsocket.close()
serversocket.close()

