
from kzpy3.utils2 import *
pythonpaths(['kzpy3'])
from vis2 import *


translation_dic = {'a':'apples','b':'build','c':'cats','d':'dogs'}
if __name__ == "__main__" and '__file__' in vars():
    argument_dictionary = args_to_dic({  'pargs':sys.argv[1:]  })
else:
    print('Running this within interactive python.')
    argument_dictionary = args_to_dic({  'pargs':"-a -1 -b 4 -c '[1,2,9]' -d '{1:5,2:4}'"  })
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
				k = mci(img,title=window_name,delay=1,scale=4.0)
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

img = img0.copy()
img[img>254] = 254 # reserve 255 for masks.
cv2.destroyAllWindows()
k = mci(img,title=window_name,delay=1,scale=4.0)
me = Mouse({'img':img,'scale':4.0})
cv2.setMouseCallback(window_name,me['event'])






def on_mouse(self, event, x, y, buttons, user_param):
    global t
    if done:
        return
    if event == cv2.EVENT_MOUSEMOVE:
        self.current = (x, y)
    elif event == cv2.EVENT_LBUTTONDOWN:
        if time.time() - t < 0.2:
            print("Completing polygon with %d points." % len(self.points))
            self.done = True
        t = time.time()
        print("Adding point #%d with position(%d,%d)" % (len(self.points), x, y))
        self.points.append((x, y))




def Bounding_Box(d):
    D = {}
    D['xy'] = d['xy']
    
    D['type'] = 'Bounding_Box'
    D['Purpose'] = d2s(inspect.stack()[0][3],':','Bounding_Box for car segmentation.')
    return D


bounding_box = Bounding_Box({'xy:})

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






#EOF
