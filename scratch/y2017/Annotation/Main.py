###############################
#  for interactive terminal
import __main__ as main
if not hasattr(main,'__file__'):
	from kzpy3.utils2 import *
	pythonpaths([opjh('kzpy3'),opjh('kzpy3/scratch/y2017/Annotation')])
#
###############################

from Parameters_Module import *
from vis2 import *
exec(identify_file_str)

_ = dictionary_access

for a in Args.keys():
    _(P,a,equals,_(Args,a))

print(P)



def Mouse(*args):
	Args = args_to_dictionary(args) 
	imgv = Args['img']
	scalev = Args['scale']
	x_max = shape(imgv)[1]
	y_max = shape(imgv)[0]
	True
	D = {}
	D['dic_type'] = 'Mouse_Event'
	D['purpose'] = d2s(inspect.stack()[0][3],':','Mouse event handler.')
	D['t'] = time.time()
	D['color'] = (0,0,0)
	D['mode'] = 'inactive'
	D['points'] = None
	D['window_name'] = 'seg'
	def _event(event, x, y, buttons, user_param):
		if event == cv2.EVENT_MOUSEMOVE:
			x = int(x / scalev)
			y = int(y / scalev)
			D['xy'] = (x,y)
			if D['mode'] == 'draw':
				D['points'].append(D['xy'])
			if x < x_max and x >= 0 and y < y_max and y >= 0:
				if D['points'] != None:
					if len(D['points']) > 1:
						cv2.line(imgv,D['points'][-2],D['points'][-1],D['color'])
				#k = mci(imgv,title=D['window_name'],delay=33,scale=P[SCALE])
				#if k > 0:
				#	print k

			else:
				pass
		elif event == cv2.EVENT_LBUTTONDOWN:
			if D['mode'] == 'draw':
				D['mode'] = 'inactive'
				cv2.fillPoly(imgv,np.array([D['points']],dtype=np.int32),255)
				k = mci(imgv,title=D['window_name'],delay=1,scale=P[SCALE])
				D['points'] = None
				D['color'] = (0,0,0)
			elif D['mode'] == 'inactive':
				D['mode'] = 'draw'
				D['color'] = (255,0,0)
				D['points'] = []
		elif event == cv2.EVENT_LBUTTONUP:
			pass#D['color'] = [0,0,0]
	D['event'] = _event
	return D


def setup_image(*args):
	Args = args_to_dictionary(args)
	imgv = Args['img']
	True
	imgv[imgv>254] = 254 # reserve 255 for masks.
	cv2.destroyAllWindows()
	k = mci(imgv,title='seg',delay=1,scale=P[SCALE])
	me = Mouse('img',imgv, 'scale',P[SCALE])
	cv2.setMouseCallback('seg',me['event'])

def save_mask(*args):
	Args = args_to_dictionary(args)
	mask = Args['mask']
	path = Args['path']
	True
	mask[mask<255] = 0
	mask[:,:,1] = mask[:,:,0]
	mask[:,:,2] = mask[:,:,0]
	#mi(mask)
	imsave(path,mask)

def combine_images(*args):
	Args = args_to_dictionary(args)
	img1 = Args['img1']
	img2 = Args['img2']
	mask = Args['mask']
	True
	rows,cols,channels = img2.shape
	roi = img1[0:rows, 0:cols ]
	img2gray = cv2.cvtColor(mask,cv2.COLOR_RGB2GRAY)
	ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
	mask_inv = cv2.bitwise_not(mask)
	img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
	img2_fg = cv2.bitwise_and(img2,img2,mask = mask)
	dst = cv2.add(img1_bg,img2_fg)
	img1[0:rows, 0:cols ] = dst
	return img1
Image = {}
def annotation(*args):
	Args = args_to_dictionary(args)
	if 'i' not in Args:
		i = 0
	else:
		i = Args['i']
	True
	camera_imgs = sggo(P[IMAGES],'*.png')
	reverse = False
	while True:
		if i < 0:
			i = 0
		elif i > len(camera_imgs):
			i = len(camera_imgs)-1
		c = camera_imgs[i]
		masks = map(fname,sggo(P[MASKS],'*.png'))
		if fname(c) not in masks:
			print(d2s('annotating',c))
			Image['mask'] = imread(c)
			mask_copy = Image['mask'].copy()
			setup_image('img',Image['mask'])
			decision = 'y'
			while True:
				k = mci(Image['mask'],title='seg',delay=33,scale=P[SCALE])
				#print k
				if k == 114: # r
					Image['mask'] = mask_copy.copy()
					setup_image('img',Image['mask'])
				elif k == 115: # s
					pd2s('saving mask for',fname(c))
					save_mask('mask',Image['mask'], 'path',opj(P[MASKS],fname(c)))
					i += 1
					break
				elif k == 63233: # <down arrow>
					i += 1
					reverse = False
					break
				elif k == ord('q'):
					sys.exit()
				#elif k == 63232: # <up arrow>
				#	i -= 1
				#	reverse = True
				#	break
		else:
			print(d2s(c,'already has mask.'))
			i += 1

"""
13 = enter
114 = r
115 = s
"""

def test():
	camera_imgs = sggo(P[IMAGES],'*.png')
	masks = sggo(P[MASKS],'*.png')
	mask = random.choice(masks)
	img2 = imread(opj(P[IMAGES],fname(mask)))
	img1 = imread(random.choice(camera_imgs))
	mask = imread(mask)
	mi(combine_images('img1',img1, 'img2',img2, 'mask',mask),1)

def multitest():
	while True:
		test()
		pause(5)


if __name__ == '__main__':
	annotation()



#EOF