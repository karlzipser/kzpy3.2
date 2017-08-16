import io
import socket
import struct
#from PIL import Image
import time
import numpy as np
from kzpy3.vis import *
#from  matplotlib.animation import FuncAnimation
# ps -fA | grep python

img_path = opjh('Desktop/RPi_data',time_str())
unix(d2s('mkdir -p',img_path))

"""
def delete_not_yet_viewed():
    _,img_files = dir_as_dic_and_list(opj(img_path,'not_yet_viewed'))
    for f in img_files:
        print f
        unix(d2s('rm',opj(img_path,'not_yet_viewed',f)),False)

delete_not_yet_viewed()
"""

print 'Start a socket listening for connections'
# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)


host = '0.0.0.0'
port = 8080
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((host, port))
serversocket.listen(5) # become a server socket, maximum 5 connections
TIMEOUT_DURATION = 1.0
meta_connection, address = serversocket.accept()
#meta_connection.settimeout(TIMEOUT_DURATION)




# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')




ctr = 0
cum_dt = 0
try:
    while True:
        t = time.time()
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(4))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection

        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)

        image = PIL.Image.open(image_stream)
        buf = ''
        while len(buf) < 128:
            buf += meta_connection.recv(128)
        assert len(buf) == 128
        ts = (buf.split(' ')[0]).strip('?')
        img = np.asarray(image.convert('RGB'))
        
        #print('Image is %dx%d' % image.size)
        imsave(opj(img_path,d2n(ctr,'_',ts,'.jpg')),img)
        ctr += 1
        if ctr > 0:
            cum_dt += time.time()-t
            if np.mod(ctr,20) == 0 or ctr == 1:
                print(time.time()-t, (1.0*ctr)/cum_dt,np.shape(img), ctr)
        #image.verify()
        #print('Image is verified')
        
finally:
    connection.close()
    server_socket.close()
    meta_connection.close()
    serversocket.close()
print ctr


