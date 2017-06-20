"Run d.py, then c.py, then keypress_rain.py or b.py"

from kzpy3.utils import *
import socket

localhost = '127.0.0.1' # 'localhost'
localport = 5000
remotehost = '127.0.0.1'
remoteport = 5001

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((localhost, localport))
serversocket.listen(5) # become a server socket, maximum 5 connections
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((remotehost, remoteport))
connection, address = serversocket.accept()



motor_freq = 50
motor_ds = 0
servo_freq = 50
servo_ds = 0

servo_pwm_right_max = 11
servo_pwm_left_min = 7.2
servo_pwm_center = 9.5

def steering_freq(mouse_x):
    if mouse_x < 0.5:
        return servo_pwm_center - 2 * mouse_x * (servo_pwm_center - servo_pwm_left_min)
    else:
        return servo_pwm_center + 2 * (mouse_x - 0.5) * (servo_pwm_right_max - servo_pwm_center) 

def process_buf(buf):
    if buf == 'q':
        return 'q'
    if buf == 'r':
        r = 'reverse'
    elif buf == 'd':
        r = 'drive'
    elif buf == ' ':
        r = 'break'
    elif buf == 'handshake':
        r = 'hs'
    else:
        r = str(steering_freq(eval(buf)[0]))
    print r
    return r





print("osx_server.py Server/Client Side:")

last_buf = False

while True:
    buf = connection.recv(64)
    if len(buf) > 0:
        last_buf = buf
        clientsocket.send(process_buf(buf))
        if buf == 'q':
            time.sleep(0.1)
            break
    elif last_buf:
        print 'here'      
        clientsocket.send(process_buf(last_buf))
    else:
        pass
    #time.sleep(0.3)


clientsocket.close()
serversocket.close()

