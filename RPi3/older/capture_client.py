# see http://picamera.readthedocs.org/en/latest/recipes2.html

import io
import socket
import struct
import time
import picamera

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
client_socket.connect(('192.168.43.243', 8000))

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
try:
    with picamera.PiCamera() as camera:
        print 'warming up'
        camera.resolution = (300,225)#(150,112)#(128,96)#(150,112)#(640, 480)#(640, 480)# #(300,225)
        camera.framerate = 15
        # Start a preview and let the camera warm up for 2 seconds
        #camera.start_preview()
        time.sleep(2)

        # Note the start time and construct a stream to hold image data
        # temporarily (we could write it directly to connection but in this
        # case we want to find out the size of each capture first to keep
        # our protocol simple)
        start = time.time()
        stream = io.BytesIO()
        print 'starting capture'
        while time.time()-start < 300:
			camera.capture(stream, format='jpeg', use_video_port=True)
			# Write the length of the capture to the stream and flush to
			# ensure it actually gets sent
			connection.write(struct.pack('<L', stream.tell()))
			connection.flush()
			# Rewind the stream and send the image data over the wire
			stream.seek(0)
			connection.write(stream.read())
			# Reset the stream for the next capture
			stream.seek(0)
			stream.truncate()


    # Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()


"""
        for foo in camera.capture_continuous(stream, format='jpeg', use_video_port=True,quality=10):
            # Write the length of the capture to the stream and flush to
            # ensure it actually gets sent
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            # Rewind the stream and send the image data over the wire
            stream.seek(0)
            connection.write(stream.read())
            # If we've been capturing for more than 30 seconds, quit
            if time.time() - start > 30:
                break
            # Reset the stream for the next capture
            stream.seek(0)
            stream.truncate()
"""

