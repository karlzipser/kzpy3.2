"""

To run:
ssh pi@192.168.43.20
sudo python kzpy3/RPi2/RPi_server.py
ipython --pylab osx kzpy3/RPi2/osx_gui_client.py ; reset

"""

from kzpy3.vis import *
#from kzpy3.RPi.utils import *
from  matplotlib.animation import FuncAnimation

USE_RPi = True
SOC = True



if SOC:
    print "Client Side:"
    import socket
    host = '192.168.43.20'
    #host = 'localhost'
    port = 5000
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((host, port))







fig = plt.figure(figsize=(5,5))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
#ax.set_xlim(0,1), ax.set_xticks([])
#ax.set_ylim(0,1), ax.set_yticks([])



img_path = opjh('scratch/2015/11/RPi_images/')
img_shape = False

if True:#USE_RPi:
    _,img_files = dir_as_dic_and_list(opj(img_path,'not_yet_viewed'))
    for f in img_files:
        print f
        unix(d2s('rm',opj(img_path,'not_yet_viewed',f)),False)

ctr = 0
def update(frame_number):
    global ctr
    global img_shape
    global steering_ds
    global motor_ds
    if SOC:
        mds = motor_ds
        if ctr < 5:
            mds = 0
            ctr += 1
        else:
            ctr = 0
        clientsocket.send(d2s((steering_ds,mds)))
        print((steering_ds,mds))
    try:
        _,img_files = dir_as_dic_and_list(opj(img_path,'not_yet_viewed'))
        img = imread(opj(img_path,'not_yet_viewed',img_files[-1]))
        img_shape = shape(img)
        for f in img_files[:-4]:
            unix(d2s('mv',opj(img_path,'not_yet_viewed',f),opj(img_path,'viewed')),False)
        if shape(img)[2] == 3:
            plt.clf()
            mi(img)
            #time.sleep(0.01)
        else:
            print('Empty frame.')
    except KeyboardInterrupt:
        print('Quitting now.')
        print('\nCleaning up.')
        sftp.close()
        transport.close()
        print('Done.')
        sys.exit(1)
    except:
        pass


def button_press_event(event):
    #print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
    #    event.button, event.x, event.y, event.xdata, event.ydata)
    print('[ ]')
    if SOC:
        clientsocket.send(' ')


def motion_notify_event(event):
    global steering_ds
    global motor_ds
    try:
        if event.xdata == None:
            steering_ds = 0
            motor_ds = 0
        else:
            x = event.xdata/(1.0*img_shape[1])
            y = 1.0 - event.ydata/(1.0*img_shape[0])
            steering_ds = get_steering_ds(x)
            #motor_ds = get_motor_ds(y)
        print(steering_ds,-1)
        if SOC:
            clientsocket.send(d2s((steering_ds,-1)))
    except:
        print('error!')

def key_press_event(event):
    global motor_ds
    if SOC:
        clientsocket.send(event.key)
    if event.key == 'a':
        if SOC:
            motor_ds = 7.2
            clientsocket.send(d2s((steering_ds,motor_ds)))
            print((steering_ds,mds))
    if event.key == 'q':
        if SOC:
            clientsocket.close()
        plt.clf()
        plt.close()
        fig.canvas.mpl_disconnect(cid)
        print('quit!!')
        sys.exit(1)
    else:
        print('['+event.key+']')

def figure_leave_event(event):
    print('figure_leave_event')
    if SOC:
        clientsocket.send('figure_leave_event')

def figure_enter_event(event):
    print('figure_enter_event')
    if SOC:
        clientsocket.send('figure_enter_event')

def axes_enter_event(event):
    print('axes_enter_event')
    if SOC:
        clientsocket.send('axes_enter_event')

def axes_leave_event(event):
    print('axes_leave_event')
    if SOC:
        clientsocket.send('axes_leave_event')


cid = fig.canvas.mpl_connect('key_press_event', key_press_event)
fig.canvas.mpl_connect('button_press_event', button_press_event)
fig.canvas.mpl_connect('motion_notify_event', motion_notify_event)
fig.canvas.mpl_connect('figure_leave_event', figure_leave_event)
fig.canvas.mpl_connect('figure_enter_event', figure_enter_event)
#fig.canvas.mpl_connect('axes_enter_event', axes_enter_event)
#fig.canvas.mpl_connect('axes_leave_event', axes_leave_event)





###########################


motor_ds = 0

steering_ds = 0

servo_pwm_right_max = 11.7
servo_pwm_left_min = 7.2
servo_pwm_center = 9.2

motor_pwm_max = 8

def get_steering_ds(mouse_x):
    if mouse_x < 0.5:
        return servo_pwm_center - 2 * (0.5 - mouse_x) * (servo_pwm_center - servo_pwm_left_min)
    else:
        return servo_pwm_center + 2 * (mouse_x - 0.5) * (servo_pwm_right_max - servo_pwm_center) 

def get_motor_ds(mouse_y):
    return motor_pwm_max - 1 + mouse_y

###########################







animation = FuncAnimation(fig, update, interval=33)

#plt.ion()
plt.show()


a=input('osx_gui_client:')
while True:
	pass
