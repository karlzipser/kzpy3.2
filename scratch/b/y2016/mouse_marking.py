from kzpy3.vis import *
from  matplotlib.animation import FuncAnimation
from kzpy3.RPi3.view_drive_data_essentials import *

all_runs_dic = load_obj('/Users/karlzipser/Desktop/RPi3_data/all_runs_dics/runs_scl_100_RGB')
k = sorted(all_runs_dic.keys())

fig = plt.figure('workspace')#figsize=(5,5))
#ax = fig.add_axes([0, 0, 300, 225], frameon=False)

X = 0
Y = 0
BUTTON = False
ctr = 0
img = zeros((225,300))
def update(frame_number):
    global ctr
    global img
    #plt.clf()
    #plt.imshow(img)
    mi(img)
    ctr += 1
    try:
        plot(X,Y,'rx')
        if BUTTON:
            print((X,Y))
            img = imread(opj(all_runs_dic[k[0]]['run_path'],all_runs_dic[k[0]]['img_lst'][ctr]))
            if ctr > 0:
                plot([X,150],[Y,225],'r-')
    except KeyboardInterrupt:
        print('Quitting now.')
        print('Done.')
        sys.exit(1)
    except:
        pass
def button_press_event(event):
    global BUTTON,X,Y
    BUTTON = True
    X = event.xdata
    Y = event.ydata
    print event.xdata,event.x
def button_release_event(event):
    global BUTTON
    BUTTON = False
def motion_notify_event(event):
    global X,Y
    try:
        if event.xdata == None:
            pass
        else:
            X = event.xdata
            Y = event.ydata
            #print(x,y)
    except Exception,e:
        print(e)
def key_press_event(event):
    print event.key
def figure_leave_event(event):
    global BUTTON
    BUTTON = False
    print('figure_leave_event')
def figure_enter_event(event):
    print('figure_enter_event')
def axes_enter_event(event):
    print('axes_enter_event')
def axes_leave_event(event):
    global BUTTON
    BUTTON = False
    print('axes_leave_event')


cid = fig.canvas.mpl_connect('key_press_event', key_press_event)
fig.canvas.mpl_connect('button_press_event', button_press_event)
fig.canvas.mpl_connect('button_release_event', button_release_event)
fig.canvas.mpl_connect('motion_notify_event', motion_notify_event)
fig.canvas.mpl_connect('figure_leave_event', figure_leave_event)
fig.canvas.mpl_connect('figure_enter_event', figure_enter_event)
#fig.canvas.mpl_connect('axes_enter_event', axes_enter_event)
#fig.canvas.mpl_connect('axes_leave_event', axes_leave_event)







animation = FuncAnimation(fig, update, interval=10)

#plt.ion()
plt.show()


a=input('osx_gui_client:')
while True:
	pass
