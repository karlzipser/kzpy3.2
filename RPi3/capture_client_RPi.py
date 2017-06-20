import io
import socket
import struct
import time
import threading
import picamera
import sys
sys.path.insert(0, "/home/pi")
from kzpy3.utils import *

client_socket = socket.socket()
client_socket.connect(('192.168.43.243', 8000))
connection = client_socket.makefile('wb')

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('192.168.43.243', 8080))

try:
    connection_lock = threading.Lock()
    pool_lock = threading.Lock()
    pool = []

    class ImageStreamer(threading.Thread):
        def __init__(self):
            super(ImageStreamer, self).__init__()
            self.stream = io.BytesIO()
            self.event = threading.Event()
            self.terminated = False
            self.start()

        def run(self):
            # This method runs in a background thread
            while not self.terminated:
                # Wait for the image to be written to the stream
                if self.event.wait(1):
                    try:
                        with connection_lock:
                            connection.write(struct.pack('<L', self.stream.tell()))
                            connection.flush()
                            self.stream.seek(0)
                            connection.write(self.stream.read())
                            drive_data = 'FAIL'
                            fail_ctr = 0
                            fail_t = time.time()
                            while drive_data == 'FAIL':
                                try:
                                    drive_data_strs = txt_file_to_list_of_strings("/home/pi/drive_data.txt")
                                    if drive_data_strs[1] == 'okay':
                                        d = drive_data_strs[0].split(' ')
                                        if d[0] == 'Begin':
                                            if d[-1] == 'End':
                                                drive_data = d[1]
                                except Exception, e:
                                    fail_ctr += 1
                                    print(d2s('fail time =',time.time()-fail_t,'fail ctr =',fail_ctr,drive_data_strs,os.path.basename(sys.argv[0]),':',e))
                            buf = d2n(time.time(),drive_data)
                            #print buf
                            while len(buf)<128:
                                buf += '?'
                            assert len(buf) == 128
                            clientsocket.send(buf)
                            #print buf
                    finally:
                        self.stream.seek(0)
                        self.stream.truncate()
                        self.event.clear()
                        with pool_lock:
                            pool.append(self)

    count = 0
    start = time.time()
    finish = time.time()
    check_command_file_t = time.time()
    continue_running = True
    def streams():
        global count, finish
        global continue_running
        global check_command_file_t
        while continue_running: #finish - start < 30:
            with pool_lock:
                if pool:
                    streamer = pool.pop()
                else:
                    streamer = None
            if streamer:
                yield streamer.stream
                streamer.event.set()
                count += 1
            else:
                # When the pool is starved, wait a while for it to refill
                time.sleep(0.1)
            finish = time.time()
            if time.time() - check_command_file_t > 1:
                check_command_file_t = time.time()
                try:
                    cmd = txt_file_to_list_of_strings("/home/pi/command_file.txt")[0]
                    if cmd == 'quit':
                        continue_running = False
                except Exception, e:
                    print(d2s(os.path.basename(sys.argv[0]),':',e))

    with picamera.PiCamera() as camera:
        pool = [ImageStreamer() for i in range(4)]
        camera.resolution = (300,225)#(640, 480)
        camera.framerate = 15
        time.sleep(2)
        start = time.time()
        camera.capture_sequence(streams(), 'jpeg', use_video_port=True)

    # Shut down the streamers in an orderly fashion
    while pool:
        streamer = pool.pop()
        streamer.terminated = True
        streamer.join()

    # Write the terminating 0-length to the connection to let the server
    # know we're done
    with connection_lock:
        connection.write(struct.pack('<L', 0))

except KeyboardInterrupt:
    continue_running = False


finally:
    camera.close()
    connection.close()
    client_socket.close()
    clientsocket.close()

print('Sent %d images in %d seconds at %.2ffps' % (
    count, finish-start, count / (finish-start)))


