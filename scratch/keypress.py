"""
ipython --pylab osx kzpy3/scratch/keypress.py
"""

from kzpy3.vis import *

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(np.random.rand(10))

def onclick(event):
    print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
        event.button, event.x, event.y, event.xdata, event.ydata)


def on_key(event):
    
    if event.key == 'left':
    	print('GO LEFT!!')
    elif event.key == 'right':
    	print('GO RIGHT!!')
    elif event.key == 'q':
    	plt.clf()
    	plt.close()
    	fig.canvas.mpl_disconnect(cid)
    	print('quit!!')
    	sys.exit(1)
    else:
    	print('you pressed', event.key, event.xdata, event.ydata)


cid = fig.canvas.mpl_connect('key_press_event', on_key)
a=input('afd')
while True:
	pass
#fig.canvas.mpl_disconnect(cid)