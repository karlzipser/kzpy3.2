"""
ipython --pylab osx kzpy3/RPi2/keypress_rain.py
"""

from kzpy3.vis import *
from  matplotlib.animation import FuncAnimation




print "Client Side:"
import socket
host = '127.0.0.1' # 'localhost'
port = 5000
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((host, port))







fig = plt.figure(figsize=(1,1))

def update(frame_number):
    try:
        pass
    except KeyboardInterrupt:
        print('Quitting now.')
        print('\nCleaning up.')
        sftp.close()
        transport.close()
        print('Done.')
        sys.exit(1)



def onclick(event):
    print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
        event.button, event.x, event.y, event.xdata, event.ydata)

def on_key(event):
    print "on_key"
    
    print event.key
    clientsocket.send(event.key)
    if event.key == 'q':
        clientsocket.close()
        plt.clf()
        plt.close()
        fig.canvas.mpl_disconnect(cid)
        print('quit!!')
        sys.exit(1)
    else:
        print(event.key, event.xdata, event.ydata)




cid = fig.canvas.mpl_connect('key_press_event', on_key)

animation = FuncAnimation(fig, update, interval=10)
plt.show()





a=input('afd')
while True:
	pass
