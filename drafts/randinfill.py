#,a

from kzpy3.vis3 import *


def randinfill(img_lst,num_samples):
	shape_image = shape(img_lst[0])
	for img in img_lst:
		for y in range(shape_image[0]):
			for x in range(shape_image[1]):
				#print y,x
				if num_samples[y,x] == 0:
					found = False
					xx = x
					yy = y
					while not found:
						dx = random.choice([-1,0,1])
						dy = random.choice([-1,0,1])
						if xx+dx >= 0 and yy+dy >= 0 and xx+dx < shape_image[1] and yy+dy < shape_image[0]:
							xx = xx+dx
							yy = yy+dy
							if num_samples[yy,xx] > 0:
								#print (yy,xx),(yy,xx)
								img[y,x] = img[yy,xx]
								found = True
#,b

if __name__ == '__main__':
	img0 = imread(opjD('img.png'))[:,:,0]
	img = img0.copy()
	shape_image = shape(img)
	num_samples = 0*img + 1
	for x in range(0,shape_image[1],3):
		#print x
		num_samples[:,x,] = 0
	img = img*num_samples
	a=[img,img.copy()]
	randinfill(a,num_samples)

	mi(img0,0)
	mi(a[0],1)
	mi(a[1],2)
	spause()
	raw_enter()
