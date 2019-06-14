from kzpy3.vis3 import *
import threading

for a in [('wait',1),('path',None),('skip',0),('start',0)]:
	if a[0] not in Arguments:
		Arguments[a[0]] = a[1]

cap = cv2.VideoCapture(Arguments['path']) 



if (cap.isOpened()== False): 
	print("Error opening video file") 

frame_print_timer = Timer(1)
timer = Timer()

ctr = 0

frames = []
abort = False

def get_frames(cap):
	ctr = 0
	while True:
		
		if len(frames) < 100:
			ret,frame = cap.read()
			if ctr >= Arguments['skip'] or not ret:
				frames.append((ret,frame))
				ctr = 0
			else:
				ctr += 1
			if not ret:
				break
		if abort:
			print 'abort'
			break

cap.set(1,Arguments['start'])

threading.Thread(target=get_frames,args=[cap]).start()



while(cap.isOpened()): 

	if len(frames) < 1:
		time.sleep(0.1)
		continue

	ret,frame = frames.pop(0)

	if frame_print_timer.check():
		frame_print_timer.reset()
		print ctr, len(frames),dp(timer.time())

	ctr += 1

	if ret == True:

		cv2.imshow('Frame', frame) 

		k = cv2.waitKey(Arguments['wait'])

		if k & 0xFF == ord('q'):
			abort = True
			break

		elif k == ord('='):
			Arguments['wait'] += 1
			print Arguments['wait']

		elif k == ord('-'):
			Arguments['wait'] -= 1
			if Arguments['wait'] < 1:
				Arguments['wait'] = 1
			print Arguments['wait']




	else: 
		break

cap.release() 

cv2.destroyAllWindows()

# MoviePy

#EOF


