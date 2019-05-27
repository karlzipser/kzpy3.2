from kzpy3.vis3 import *

for a in [('wait',30),('path',None)]:
	if a[0] not in Arguments:
		Arguments[a[0]] = a[1]

cap = cv2.VideoCapture(Arguments['path']) 

if (cap.isOpened()== False): 
	print("Error opening video file") 

frame_print_timer = Timer(1)
timer = Timer()

ctr = 0

while(cap.isOpened()): 

	ret, frame = cap.read()

	if frame_print_timer.check():
		frame_print_timer.reset()
		print ctr, dp(timer.time())

	ctr += 1

	if ret == True: 

		cv2.imshow('Frame', frame) 

		k = cv2.waitKey(Arguments['wait'])

		if k & 0xFF == ord('q'): 
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


