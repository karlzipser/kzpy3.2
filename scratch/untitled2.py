from __future__ import division
from kzpy3.vis3 import *
assert(1/2 == 0.5)
import kzpy3.scratch.image as image

if 'color_index' not in locals():
    color_list = ['b','g','r','c','m','y','k',]
    color_index = 0

if 'L' not in locals():
    L = h5r("/Users/karlzipser/Desktop/model_car_data_July2018_lrc/locations/local/left_right_center/h5py/Mr_Black_25Jul18_14h44m55s_local_lrc/left_timestamp_metadata_right_ts.h5py")

DATA = L['steer'][:]

MX,MN = -2**16,2**16
imgtimer = Timer(0.666);imgtimer.trigger()
img = image.get_blank_image(1000,200) #########
b = z55(np.random.randn(30,40,3))

for ii in range(0,10000,9):

    data = zeros((1100,2))
    data[:,0] = range(1100)
    data[:,1] = DATA[ii:ii+1100]
    mn,mx=data[:,1].min(),data[:,1].max()
    if mn < MN:
        MN = mn
    if mx > MX:
        MX = mx
    if np.random.randint(100) == 0:
        MX = 500
        cr("MX=500")
    cs = z2_255(np.random.randn(len(data),3))
    cs*=0
    for i in range(3):
        cs[:,i] = 255

    for j in [2,3]:

        xys = image.get_float_pixels( #########
            xys=data.copy(),
            img_shape=shape(img),
            col=(1,1),
            row=(j,4),
            box=((0,1100.0),(MN,MX))
        )

        image.img_pts_plot(img,xys,cs) #########

    mci(img)
    img *= 0
    if imgtimer.check():
        rr=1+np.random.randint(5)
        rc=1+np.random.randint(5)
        imgtimer.reset()
    image.place_image_in_image2(img,b,row=(rr,5),col=(rc,5)) #########
    s = 0.9
    MX = s*MX + (1-s)*(MX-MN)/2.0
    MN = s*MN + (1-s)*(MX-MN)/2.0


#EOF
