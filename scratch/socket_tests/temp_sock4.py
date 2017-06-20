from kzpy3.utils import *

import socket
host = '0.0.0.0'
port = 5007
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((host, port))
serversocket.listen(5)
TIMEOUT_DURATION = 0.333
print 'Waiting for connection . . .'
connection, address = serversocket.accept()
connection.settimeout(TIMEOUT_DURATION)

def cleanup_and_exit():
    serversocket.close()
    
    
try:
    while True:
        okay = False
        try:
            buf = ''
            t0 = time.time()
            while len(buf) < 64:
                buf += connection.recv(64)
                if time.time()-t0 > 0.5:
                    print("""\a stuck in 'while len(buf) < 64' """)
                    raise Exception(d2s("""stuck in 'while len(buf) < 64' """,buf))
                    t0 = time.time()
            assert len(buf) == 64
            buf = buf.strip('?')
            okay = True
        except Exception, e:
            print(d2s(os.path.basename(sys.argv[0]),':',e,' \a ######### pwm_motor.ChangeDutyCycle(0)'))
        if okay:
            if len(buf) != "":
                print buf
            else:
                print("\a *** No Data received from socket ***")
                cleanup_and_exit()
                break
except KeyboardInterrupt:
    print(d2s(os.path.basename(sys.argv[0]),':','KeyboardInterrupt \a'))
    cleanup_and_exit()

