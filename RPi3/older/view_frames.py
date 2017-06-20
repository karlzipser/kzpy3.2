from kzpy3.vis import *
import numpy as np
import matplotlib.pyplot as plt
from  matplotlib.animation import FuncAnimation

fig = plt.figure(figsize=(7,7))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(0,1), ax.set_xticks([])
ax.set_ylim(0,1), ax.set_yticks([])

def delete_not_yet_viewed():
    _,img_files = dir_as_dic_and_list(opj(img_path,'not_yet_viewed'))
    for f in img_files:
        print f
        unix(d2s('rm',opj(img_path,'not_yet_viewed',f)),False)


def rand_img():
    return np.random.random((225,300))

img_path = opjh('Desktop/temp')
img_dic = {}
RAND_IMG = False

def update(frame_number):
    global last_cmd
    global img_dic
    global RAND_IMG
    #print last_cmd
    #start_time = time.time()

    try:
        _,img_files = dir_as_dic_and_list(opj(img_path,'not_yet_viewed'))
        if img_files[-2] not in img_dic:
            img_dic[img_files[-2]] = True
            img = imread(opj(img_path,'not_yet_viewed',img_files[-2])) # opjD('image1.jpg'))#opj(img_path,f))
            RAND_IMG = False
            for f in img_files[:-4]:
                unix(d2s('mv',opj(img_path,'not_yet_viewed',f),opj(img_path,'viewed')),False)
        else:
            if not RAND_IMG:
                img = rand_img()
                RAND_IMG = True
                plt.clf()
                mi(img)
        if shape(img)[2] == 3:
            if not RAND_IMG:
                plt.clf()
                mi(img)
        else:
            print('Empty frame.')

    except KeyboardInterrupt:
        print('Quitting now.')
        sys.exit(1)
    except Exception, e:
        print(d2s(os.path.basename(sys.argv[0]),':',e))
        #img = rand_img()
        #plt.clf()
        #mi(img)

delete_not_yet_viewed()

animation = FuncAnimation(fig, update, interval=20)

plt.show()


a=input('...')
while True:
	pass
