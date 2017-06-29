
from kzpy3.utils2 import *
pythonpaths(['kzpy3'])
from vis2 import *


translation_dic = {'a':'apples','b':'build','c':'cats','d':'dogs'}
if __name__ == "__main__" and '__file__' in vars():
    argument_dictionary = args_to_dic({  'pargs':sys.argv[1:]  })
else:
    print('Running this within interactive python.')
    argument_dictionary = args_to_dic({  'pargs':"-a -1 -b 4 -c [1,2,9] -d {1:5,2:4}"  })
argument_dictionary = translate_args(
    {'argument_dictionary':argument_dictionary,
    'translation_dic':translation_dic})
print(argument_dictionary)




def Mouse(d):
	img = d['img']
	scale = d['scale']
	x_max = shape(img)[1]
	y_max = shape(img)[0]
	True
	D = {}
	D['type'] = 'Mouse_Event'
	D['Purpose'] = d2s(inspect.stack()[0][3],':','Mouse event handler.')
	D['t'] = time.time()
	D['color'] = (0,0,0)
	D['mode'] = 'inactive'
	D['points'] = None
	D['window_name'] = 'seg'
	def _event(event, x, y, buttons, user_param):
		if False:#done:
			return
		if event == cv2.EVENT_MOUSEMOVE:
			x = int(x / scale)
			y = int(y / scale)
			D['xy'] = (x,y)
			if D['mode'] == 'draw':
				D['points'].append(D['xy'])
			if x < x_max and x >= 0 and y < y_max and y >= 0:
				#img[y,x,:] = D['color']
				if D['points'] != None:
					if len(D['points']) > 1:
						cv2.line(img,D['points'][-2],D['points'][-1],D['color'])
				k = mci(img,title=D['window_name'],delay=1,scale=4.0)
				if k == ord(' '):
					pass
				pd2s(D['xy'],D['color'])
			else:
				pass
				#img[D['xy'][0],D['xy'][1]][:] = 0
		elif event == cv2.EVENT_LBUTTONDOWN:
			if D['mode'] == 'draw':
				D['mode'] = 'inactive'
				#cv2.polylines(img,np.array(D['points']),False,(255,255,255),1)
				#cv2.polylines(img, np.array(D['points']), False, D['color'], 1)
				cv2.fillPoly(img,np.array([D['points']],dtype=np.int32),255)
				D['points'] = None;print('set points to None')
				D['color'] = (0,0,0)
			elif D['mode'] == 'inactive':
				D['mode'] = 'draw'
				D['color'] = (255,0,0)
				D['points'] = []
		elif event == cv2.EVENT_LBUTTONUP:
			pass#D['color'] = [0,0,0]
		
	D['event'] = _event

	return D

img0 = imread(opjD('7863.png'))
img = img0.copy()
img[img>254] = 254 # reserve 255 for masks.
cv2.destroyAllWindows()
k = mci(img,title='seg',delay=1,scale=4.0)
me = Mouse({'img':img,'scale':4.0})
cv2.setMouseCallback('seg',me['event'])

if True:
	mask = img[:,:,0].copy()
	mask[mask<255] = 0
	mi(mask)



if False:
    try:
        pass
    except Exception as e:
        print("********** Exception ***********************")
        print(e.message, e.args)

	while(True):
		img_paths = sggo('/Volumes/SSD_2TB/cameras','*.png')
		img = imread(random.choice(img_paths))
		window_name = 'left right t0 t1'
		k = mci(img,title=window_name,delay=500,scale=4.0)
		if k == ord('q'):
			break



if True:
	# Load two images
	img2 = imread(opjD('7863.png'))
	img1 = imread(opjD('7843.png'))
	# I want to put logo on top-left corner, So I create a ROI
	rows,cols,channels = img2.shape
	roi = img1[0:rows, 0:cols ]
	# Now create a mask of logo and create its inverse mask also
	img2gray = cv2.cvtColor(imread(opjD('mask.png')),cv2.COLOR_RGB2GRAY)
	ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
	mask_inv = cv2.bitwise_not(mask)
	# Now black-out the area of logo in ROI
	img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
	# Take only region of logo from logo image.
	img2_fg = cv2.bitwise_and(img2,img2,mask = mask)
	# Put logo in ROI and modify the main image
	dst = cv2.add(img1_bg,img2_fg)
	img1[0:rows, 0:cols ] = dst
	mci(img1,scale=3.0)
	#cv2.imshow('res',imresize(img1,2.0))
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()




