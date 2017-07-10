# git clone https://github.com/karlzipser/kzpy3.2.git

from kzpy3.vis import *
img = imread(opjD('temp.png')) # load some image
img = img.mean(axis=2)
mi(img)

y = 0*img
y[20:40,20:40] = 0.1 # these should be more graded than only two steps
y[27:30,27:33] = 0.4

b = 0*img
b[60:70,20:40] = 0.1
b[63:68,29:33] = 1.0

c = yb_color_modulation_of_grayscale_image(img,y,b,False)
mi(c)
