from kzpy3.vis import *

fig = plt.figure(figsize=(20,3))
#ax = fig.add_axes([0, 0, 1, 1], frameon=False)

# 0_1455048664.8_str=0_spd=0_rps=0_lrn=36_rrn=100_rnd=0_


def get_run_data(run_path):
    _,l=dir_as_dic_and_list(run_path)
    index = []
    timestamp = []
    steer = []
    speed = []
    rps = []
    left_range = []
    right_range = []
    rand_control = []
    for m in l:
        n = m.split('_')
        p = n[0]
        index.append(int(p))
        p = n[1]
        timestamp.append(float(p))
        p = n[2].split('=')[1]
        steer.append(float(p)/100.0)
        p = n[3].split('=')[1]
        speed.append(float(p)/100.0)
        p = n[4].split('=')[1]
        rps.append(float(p)/10.0)
        p = n[5].split('=')[1]
        left_range.append(int(p))
        p = n[6].split('=')[1]
        right_range.append(int(p))
        p = n[7].split('=')[1]
        rand_control.append(int(p))
    run_data_dic = {}
    run_data_dic['run_path'] = run_path
    run_data_dic['img_lst'] = l
    run_data_dic['index'] = index
    run_data_dic['timestamp'] = timestamp
    run_data_dic['steer'] = steer
    run_data_dic['speed'] = speed
    run_data_dic['rps'] = rps
    run_data_dic['left_range'] = left_range
    run_data_dic['right_range'] = right_range
    run_data_dic['rand_control'] = rand_control
    return run_data_dic



data_dir = '/Users/karlzipser/Desktop/RPi3_data/10Feb16_13h12m56s'

_,l=dir_as_dic_and_list(data_dir)




def button_press_event(event):
	f = l[np.int(np.floor(event.xdata))]
	print f
 	img = imread(opj(data_dir,f))
 	plt.figure(10)
 	plt.clf()
 	plt.ion()
 	mi(img,10)
 	plt.pause(0.001)
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
    rand_control.append(p)

lrs = []
lrs.append(left_range[0])
for i in range(1,len(left_range)):
    lrs.append((left_range[i-1]+left_range[i])/2.0)

ctr = 0
for f in l:
    img = imread(opj(data_dir,f))
    plt.clf()
    plt.ion()
    if rand_control[ctr] == '1':
        img[:,:,1:] *= 0.5
    mi(img)
    plt.show()
    plt.pause(0.03)
    ctr += 1

plt.ion()
plt.plot(steer,'b')
plt.show()
plt.plot(speed,'k')
plt.plot(left_range,'r')
plt.plot(right_range,'g')
plt.plot(rps,'y')


a=input('w')

