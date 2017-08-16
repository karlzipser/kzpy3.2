import io
import socket
import struct
#from PIL import Image
import time
import numpy as np
from kzpy3.vis import *
#from  matplotlib.animation import FuncAnimation


"""
a=np.random.randn(10000)
hist(a,100)
plt.ion()
plt.show()
"""



# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
t = time.time()
t2 = t


first_time = True
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
        img = np.asarray(image.convert('RGB'))
        #print('Image is %dx%d' % image.size)

        
        if True: #t - t2 > 1:
            t2 = t
            #image.show()
            print("*************************")
            #img = np.random.rand(10,10)
            plt.clf()
            mi(img)
            if first_time:
                plt.ion()
                plt.show()
                first_time = False
            plt.pause(0.0001)

      
        print(t-time.time(),np.shape(img))
        #image.verify()
        #print('Image is verified')
        
finally:
    connection.close()
    server_socket.close()

