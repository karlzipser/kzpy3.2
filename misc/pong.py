from kzpy3.vis3 import *
import sys, termios, tty, os, time
 
#  say("Play Pong!")

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch




P = {}
P['box height'] = 200
P['box width'] = 500
P['img'] = zeros((P['box height'],P['box width']),np.uint8)

P['paddle height'] = 50
P['paddle width'] = 10
P['paddle'] = {}
P['paddle']['left'] = {}
P['paddle']['left']['x position'] = P['paddle width']/2
P['paddle']['left']['y position'] = P['box height']/2
P['paddle']['right'] = {}
P['paddle']['right']['x position'] = P['box width']-P['paddle width']/2
P['paddle']['right']['y position'] = P['box height']/2
P['paddle']['left']['dy'] =5
P['paddle']['right']['dy'] = -5
P['paddle']['left']['key'] = 'q'
P['paddle']['right']['key'] = 'p'


P['ball radius'] = 5
P['ball x position'] = P['paddle width']/2
P['ball y position'] = P['box height']/2
P['ball dx'] = 8.0
P['ball dy'] = 0.4


print """
PONG INSTRUCTIONS:
	1) resize graphics screen to position and desired size,
	2) press < space bar > to begin,
	3) press < space bar > to pause/continue game.
"""

c = 0
started = False
pause = True
while 27 != c:
	c = mci(P['img'])
	time.sleep(0.01)

	if started == False:
		#print c,ord(' ')
		if ord(' ') == c:
			started = True
			#clear_screen()
		else:
			time.sleep(0.1)
			continue
	if ord(' ') == c:
		print 'space'
		if pause:
			pause = False
		else:
			pause = True
	if pause:
		continue

	if ord('s') == c:
		say("Score!!!")

		c = mci(P['img'])
	P['img'] = P['img']*0

	for side in ['left','right']:
		#print P['paddle'][side]['key']

		if ord(P['paddle'][side]['key']) == c:
			P['paddle'][side]['dy'] *= -1

		P['paddle'][side]['y position'] += P['paddle'][side]['dy']
		x = P['paddle'][side]['x position']
		y = P['paddle'][side]['y position']
		pw = P['paddle width']
		ph = P['paddle height']
		img = P['img']
		img[y-ph/2:y+ph/2,x-pw/2:x+pw/2] = 127

	by = int(P['ball y position'])
	bx = int(P['ball x position'])
	br = P['ball radius']
	P['img'][by-br:by+br,bx-br:bx+br] = 255

	if ord('f') == c:
		P['ball dx'] *= -1.
		P['ball dy'] *= -1.

	P['ball y position'] += P['ball dy']
	P['ball x position'] += P['ball dx']
	P['img'][0,1] = 0
	P['img'][0,0] = 255

	#c = mci(P['img'])




