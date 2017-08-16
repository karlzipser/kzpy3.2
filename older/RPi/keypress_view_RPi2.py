"""

on Mac:
ipython --pylab osx kzpy3/RPi/keypress_view_RPi2.py; reset

for RPi
set laptop wifi to phone mobile hotspot
ssh pi@192.168.43.20 in two tapbs
sudo python kzpy3/RPi/camera_control.py
sudo python kzpy3/RPi/command_listener3.py


"""

from kzpy3.vis import *
from kzpy3.RPi.utils import *
from  matplotlib.animation import FuncAnimation

sftp = get_sftp(opjh('pw_RPi.txt'))

distal_command_file_path = '/home/pi/Desktop/distal_command.txt'
local_command_file_path = '/Users/karlzipser/Desktop/local_command.txt'

fig = plt.figure(figsize=(7,7))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(0,1), ax.set_xticks([])
ax.set_ylim(0,1), ax.set_yticks([])

last_cmd ='no command yet'

img_path = opjh('scratch/2015/11/RPi_images/')

_,img_files = dir_as_dic_and_list(opj(img_path,'not_yet_viewed'))
for f in img_files:
    print f
    unix(d2s('rm',opj(img_path,'not_yet_viewed',f)),False)

def update(frame_number):
    global last_cmd
    try:
        _,img_files = dir_as_dic_and_list(opj(img_path,'not_yet_viewed'))
        img = imread(opj(img_path,'not_yet_viewed',img_files[-1]))
        for f in img_files[:-4]:
            unix(d2s('mv',opj(img_path,'not_yet_viewed',f),opj(img_path,'viewed')),False)
        if shape(img)[2] == 3:
            plt.clf()
            mi(img)
            time.sleep(0.01)
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
    

def onclick(event):
    print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
        event.button, event.x, event.y, event.xdata, event.ydata)

list_of_strings_to_txt_file(local_command_file_path,['no command yet...'])
sftp.put(local_command_file_path, distal_command_file_path)



def on_key(event):
    list_of_strings_to_txt_file(local_command_file_path,[d2s(event.key,time.time())])
    sftp.put(local_command_file_path, distal_command_file_path)

    if event.key == 'left':
        pass
    	#print('GO LEFT!!')
    elif event.key == 'right':
        pass
    	#print('GO RIGHT!!')
    elif event.key == 'q':
    	plt.clf()
    	plt.close()
    	fig.canvas.mpl_disconnect(cid)
    	print('quit...')
        #print '\033[2J'
    	sys.exit(1)
    else:
        pass
    	#print('you pressed', event.key, event.xdata, event.ydata)


cid = fig.canvas.mpl_connect('key_press_event', on_key)

animation = FuncAnimation(fig, update, interval=10)
plt.show()

print("""
    *** keypress_view_RPi2.py ***
    Start this before starting command_listener.py
    To make command, put mouse on display window and press command keys...
        [<-] left
        [->] right
        [up arrow] straight
        [space bar] motor
        [q]  quit
""")


a=input('...')

"""
while True:
    time.sleep(1)
    print(time.time() - time_of_last_keypress)
    if (time.time() - time_of_last_keypress > 1):
        print('handshake')
        time_of_last_keypress = time.time()
"""

