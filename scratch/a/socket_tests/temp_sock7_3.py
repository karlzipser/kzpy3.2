from kzpy3.utils import *
# lock and unlock files: http://tilde.town/~cristo/file-locking-in-python.html
import socket
n=3
FIVEK = 5000+n
EIGHTK = 8000+n
client_setup = False





def get_client_socket(host,port):
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((host, port))
    return clientsocket

def send_buf64(clientsocket,buf):
    while len(buf)<64:
        buf += '?'
    assert len(buf) == 64
    clientsocket.send(buf)

def cleanup_and_exit():
    serversocket.close()
    clientsocket.close()


try:
    clientsocket = get_client_socket('localhost', FIVEK)
    buf = '<'+time_str()+'>'
    send_buf64(clientsocket,buf)
    client_setup = True
except:
    pass


host = '0.0.0.0'
if client_setup:
    port = EIGHTK
else:
    port = FIVEK
    subprocess.Popen(['python',opjh('kzpy3/teg1/temp_sock7_3.py')])#unix('python /Users/karlzipser/kzpy3/teg1/.py')

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((host, port))
serversocket.listen(5)
TIMEOUT_DURATION = 0.0333
print 'Waiting for connection . . .'
connection, address = serversocket.accept()
connection.settimeout(TIMEOUT_DURATION)


if not client_setup:
    clientsocket = get_client_socket('localhost', EIGHTK)
    buf = '<'+time_str()+'>'
    send_buf64(clientsocket,buf)


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
            pass #print(d2s(os.path.basename(sys.argv[0]),':',e,' \a ######### pwm_motor.ChangeDutyCycle(0)'))
        if okay:
            if len(buf) != "":
                print str(port)+' '+buf
            else:
                print("\a *** No Data received from socket ***")
                cleanup_and_exit()
                break
        buf = '<'+str(port)+' '+time_str()+'>'
        while len(buf)<64:
            buf += '?'
        assert len(buf) == 64
        if np.random.random() < 0.01:
            clientsocket.send(buf)
        time.sleep(0.01)

except KeyboardInterrupt:
    print(d2s(os.path.basename(sys.argv[0]),':','KeyboardInterrupt \a'))
    cleanup_and_exit()

