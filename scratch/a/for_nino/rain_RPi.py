"""
animate timelapse frames matrix
"""
from kzpy3.vis import *
from matplotlib.animation import FuncAnimation

"""
[1447274072.87,1447274073.01,1447274073.4,1447274073.14,1447274073.27,1447274073.53]

"""

"""
def load_img_folder_to_dict(img_folder):
    '''Assume that *.* selects only images.'''
    img_fns = gg(opj(img_folder,'*.*'))
    imgs = {}
    for f in img_fns:
        imgs[f.split('/')[-1]] = imread(f)
    return imgs

def load_img_folder_to_list(img_folder):
    return dict_to_sorted_list(load_img_folder_to_dict(img_folder))


t = (2009, 2, 17, 17, 3, 38, 1, 48, 0)
secs = time.mktime( t )
print "time.mktime(t) : %f" %  secs
print "asctime(localtime(secs)): %s" % time.asctime(time.localtime(secs))


"""


def dict_to_float_sorted_list(d):
    l = []
    ks = sorted(d.keys())
    for k in ks:
        l.append(d[k])
    return l


def load_txt_folder_to_dict(img_folder):
    ''' '''
    img_fns = gg(opj(img_folder,'*.txt'))
    imgs = {}
    for f in img_fns:
        imgs[f.split('/')[-1]] = txt_file_to_list_of_strings(f)
    return imgs


def frames_and_times(frames_dic):
    frames_dic_sortable = {}
    for k in frames_dic.keys():
    	ctr = k.split('.')[0]
    	t = k.split('.')[1]
    	t2 = k.split('.')[2]
    	if t in frames_dic_sortable:
    		print(d2s(t,t2,'in dic already'))
    	frames_dic_sortable[np.float(t+'.'+t2)] = frames_dic[k]
    frames = dict_to_float_sorted_list(frames_dic_sortable)
    frame_times = []
    ks = sorted(frames_dic_sortable.keys())
    for k in ks:
        frame_times.append(k)       
    return frames,frame_times

def commands_and_times(commands_dic):
    commands_dic_sortable = {}
    for k in commands_dic.keys():
        t = np.float(k.split('.txt')[0])
        if t in commands_dic_sortable:
            print(d2s(t,'in dic already'))
        commands_dic_sortable[t] = commands_dic[k]
    commands = dict_to_float_sorted_list(commands_dic_sortable)
    command_times = []
    ks = sorted(commands_dic_sortable.keys())
    for k in ks:
        command_times.append(k)       
    return commands,command_times


def commands_in_frame_sync(frame_times,command_times,commands):
    binned_commands = []
    for i in range(len(frame_times)-1):
        command = False
        ts = frame_times[i:i+2]
        for j in range(len(command_times)):
            if command_times[j] >= ts[0] and command_times[j] < ts[1]:
                command = commands[j]
                break
        binned_commands.append(command)
    binned_commands.append(False)
    return binned_commands


def binned_commands_to_servo_floats(binned_commands):
    sf = []

    for b in binned_commands:
        f = 0.0;
        if b:
            print(b)
            if b[0].split(' ')[0] != 'motor':
                f = np.float(b[0].split(' ')[0])
            elif b[0].split(' ')[0] == 'motor':
                f = -100
        sf.append(f)
    return sf

def servo_floats_to_left_right(servo_floats):
    lr = []

    p = False
    for f in servo_floats:
        d = ''
        if f > 0:
            if p:
                if f > p:
                    d = 'right'
                else:
                    d = 'left'
            p = f
        elif f == -100:
            d = '___'
        lr.append(d)
    return lr


"""
frames_dic = load_img_folder_to_dict(opjh('Desktop/DATA/VIEWED'))# 'scratch/2015/11/RPi_images/viewed'))# 'scratch/2015/10/8/timelapse.1444316394'))
frames,frame_times = frames_and_times(frames_dic)
commands_dic = load_txt_folder_to_dict('/Users/karlzipser/Desktop/DATA/EXEC')
commands,command_times = commands_and_times(commands_dic)
binned_commands = commands_in_frame_sync(frame_times,command_times,commands)
sf = binned_commands_to_servo_floats(binned_commands)
lr = servo_floats_to_left_right(sf)

N = 20
T = 3
good_commands_indicies = []
dts = []
for i in range(N,len(frame_times)):
    dt = frame_times[i]-frame_times[i-N]
    dts.append(dt)
    if len(lr[i]) > 0 and dt < T:
        good_commands_indicies.append(i)

path = opjh('scratch/2015/11/23/RPi_frames0')
unix('mkdir -p '+path)
for i in range(len(frames)):
    print i
    f = zscore(frames[i].mean(axis=2),thresh=2.5)
    imsave(opj(path,d2n(i,'.jpeg')),f)


train = []

for i in good_commands_indicies:
    
    train.append([])
    for j in range(1,N-1):
        #print (i,i-j)
        train[-1].append(i-j)
    print((lr[i],train[-1]))

train2 = {}
for i in range(18):
    train2[i] = []

for l in train:
    c = lr[l[0]+1]
    if c == '___':
        label = 0
    elif c == 'left':
        label = 1
    elif c == 'right':
        label = 2
    else:
        sys.exit('ERROR')
    print label
    for i in range(len(l)):
        train2[i].append(d2s(opj(path,d2n(l[i],'.jpeg')),label))

train3 = {}
for i in range(18):
    train3[i] = []

for i in range(1000):
    r = range(len(train2[0]))
    random.shuffle(r)
    for j in r:
        for k in train2.keys():
            train3[k].append(train2[k][j])

for k in train3.keys():
    list_of_strings_to_txt_file(opjh('scratch/2015/11/26',d2n('train_',k,'.txt')),train3[k])




binned_servo_commands = []
binned_motor_commands = []
servo_current = 9.5
for c in sf:
    if c > 0:
        servo_current = c
        binned_motor_commands.append(0.0)
    elif c == -100:
        binned_motor_commands.append(1.0)
    else:
        binned_motor_commands.append(0.0)
    binned_servo_commands.append(servo_current)




path = opjh('scratch/2015/11/28/RPi_frames1')
unix('mkdir -p '+path)

for i in range(len(frames)):
    s = d2f('-',i,binned_motor_commands[i],binned_servo_commands[i],frame_times[i],'.jpeg')
    f = zscore(frames[i].mean(axis=2),thresh=2.5)
    imsave(opj(path,s),f)
    print(s)


"""

p = '/Users/karlzipser/scratch/2015/11/28/RPi_frames1'
d,l=dir_as_dic_and_list(p)

n_frames = len(frames)


def even_frames(frame_number):
    frame_number += 250
    fn = l[frame_number]
    print(frame_number)
    plt.clf()
    if binned_commands[frame_number]:
        title = binned_commands[frame_number]
    else:
        title = ""
    title = fn.split('-')[1:3]#lr[frame_number]
    frame = imread(opj(p,fn))
    f = frame#zscore(frame.mean(),thresh=2.5)
    mi(f,img_title=title)#d2s(frame_number,np.int(frame_times[frame_number]-frame_times[0]),binned_commands[frame_number]))
    if frame_number == n_frames-1:
        plt.close()


"""
def even_frames(frame_number):
    frame_number += 250
    print(frame_number)
    plt.clf()
    if binned_commands[frame_number]:
        title = binned_commands[frame_number]
    else:
        title = ""
    title = lr[frame_number]
    f = zscore(frames[frame_number].mean(axis=2),thresh=2.5)
    mi(f,img_title=title)#d2s(frame_number,np.int(frame_times[frame_number]-frame_times[0]),binned_commands[frame_number]))
    if frame_number == n_frames-1:
        plt.close()

def even_frames(frame_number):
    print(frame_number)
    if binned_commands[frame_number]:
        plt.clf()
        mi(frames[frame_number],img_title=binned_commands[frame_number])#d2s(frame_number,np.int(frame_times[frame_number]-frame_times[0]),binned_commands[frame_number]))
    if frame_number == n_frames-1:
        plt.close()




fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(np.random.rand(10))

def onclick(event):
    print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
        event.button, event.x, event.y, event.xdata, event.ydata)


def on_key(event):
    
    if event.key == 'left':
        print('GO LEFT!!')
        plt.clf()
        plt.plot(np.random.rand(10))

    elif event.key == 'right':
        print('GO RIGHT!!')
        
    elif event.key == 'q':
        plt.clf()
        plt.close()
        fig.canvas.mpl_disconnect(cid)
        print('quit!!')
        damn()#sys.exit(1)
    else:
        print('you pressed', event.key, event.xdata, event.ydata)


cid = fig.canvas.mpl_connect('key_press_event', on_key)
a=input('afd')



"""
fig = plt.figure(1,figsize=(9,9))

animation = FuncAnimation(fig, even_frames, frames=n_frames, interval=1000, repeat=False)

plt.show()

print('done....')


