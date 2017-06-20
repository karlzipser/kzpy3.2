from kzpy3.vis import *

fig = plt.figure(figsize=(20,3))
#ax = fig.add_axes([0, 0, 1, 1], frameon=False)

data_dir = opjh('Desktop/RPi3_data',sys.argv[1])

_,l=dir_as_dic_and_list(data_dir)
"""
for f in l:
    img = imread(opj(data_dir,f))
    plt.clf()
    plt.ion()
    mi(img)
    plt.show()
    plt.pause(0.03)

"""
def button_press_event(event):
    for x in range(np.int(np.floor(event.xdata))-30,np.int(np.floor(event.xdata))+30):
    	f = l[x]
        r = rand_control[x]
    	print f
     	img = imread(opj(data_dir,f))
        if r > 0:
            img[:,:,1:] *= 0.5
     	plt.figure(10)
     	plt.clf()
     	plt.ion()
     	mi(img,10)
     	plt.pause(0.01)
 	plt.figure(1)
 	

fig.canvas.mpl_connect('button_press_event', button_press_event)

timestamp = []
steer = []
speed = []
rps = []
left_range = []
right_range = []
rand_control = []
for m in l:
    n = m.split('_')
    p = n[2].split('=')[1]
    steer.append(p)
    p = n[3].split('=')[1]
    speed.append(p)
    p = n[4].split('=')[1]
    rps.append(p)
    p = n[5].split('=')[1]
    left_range.append(int(p))
    p = n[6].split('=')[1]
    right_range.append(p)
    p = n[7].split('=')[1]
    rand_control.append(10*int(p))

lrs = []
lrs.append(left_range[0])
for i in range(1,len(left_range)):
    lrs.append((left_range[i-1]+left_range[i])/2.0)

plt.ion()
plt.plot(steer,'b')
plt.show()
plt.plot(speed,'k')
plt.plot(rand_control,'r')
plt.plot(rps,'g')


a=input('w')

