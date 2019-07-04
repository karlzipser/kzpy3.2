from kzpy3.vis3 import *
from __future__ import division

if 'color_index' not in locals():
    color_list = ['b','g','r','c','m','y','k',]
    color_index = 0

if 'L' not in locals():
    L = h5r("/Users/karlzipser/Desktop/model_car_data_July2018_lrc/locations/local/left_right_center/h5py/Mr_Black_25Jul18_14h44m55s_local_lrc/left_timestamp_metadata_right_ts.h5py")

########################################################################################
########################################################################################
########################################################################################
####      


def get_float_pixelsA(xy_img_size,col,row):

    row_height = xy_img_size[1]/row[1]

    col_width  = xy_img_size[0]/col[1]

    xy_pixel_offset = ( col_width*(col[0]-1), #
                        row_height*(row[0]-1) )

    return row_height,col_width,xy_pixel_offset



def get_float_pixelsB(xys,box,xy_img_size,row_height,col_width,xy_pixel_offset):

    xy_real_mag = (box[0][1] - box[0][0],
                    box[1][1] - box[1][0])

    xy_real_to_pixels = (
        col_width/xy_real_mag[0],
        row_height/xy_real_mag[1])

    xys[:,0] *= xy_real_to_pixels[0]
    xys[:,1] *= xy_real_to_pixels[1]
    xys[:,0] -= xys[:,0].min()
    xys[:,1] -= xys[:,1].min()
    xys[:,0] += xy_pixel_offset[0]
    xys[:,1] += xy_pixel_offset[1]
    xys[:,1] = xy_img_size[1] - xys[:,1]

    for i in [0,1]:
        a = xys[:,i]
        a[ a < 0 ] = 0
        a[ a >= xy_img_size[i] ] = xy_img_size[i] - 1

    return xys








def img_pts_plot(img,xys,cs):
    img[ xys[:,1].astype(int), xys[:,0].astype(int), : ] = cs

def get_blank_image(x,y):
    return zeros((y,x,3)).astype(np.uint8)

def add_image(img,img_new,xy):
    pass



####
########################################################################################
########################################################################################
########################################################################################
DATA = L['steer'][:]
MX,MN = -2**16,2**16

img = get_blank_image(1000,200)

xy_img_size = (shape(img)[1],shape(img)[0])

row_height,col_width,xy_pixel_offset = get_float_pixelsA(xy_img_size,col=(1,1),row=(j,4))
 




for ii in range(0,10000,9):


    if 'gather data':
        if False:
            data = zeros((1000,2))
            data[:,0] = arange(0,1000)/100.
            data[:,1] = np.sin(data[:,0])
        data = zeros((1100,2))
        data[:,0] = range(1100)
        data[:,1] = DATA[ii:ii+1100]
        mn,mx=data[:,1].min(),data[:,1].max()
        if mn < MN:
            MN = mn
        if mx > MX:
            MX = mx
        if np.random.randint(100) == -1:
            MX = 500
            cr("MX=500")
        cs = z2_255(np.random.randn(len(data),3))
        cs*=0
        for i in range(3):
            cs[:,i] = 255#np.random.randint(255)

    for j in [2,3]:

        xys = get_float_pixels(
            xys=data.copy(),
            img_shape=shape(img),
            col=(1,1),
            row=(j,4),
            box=((0,1100.0),
                (MN,MX)))

        img_pts_plot(img,xys,cs)

    mci(img)
    s = 0.9
    MX = s*MX + (1-s)*(MX-MN)/2.0
    MN = s*MN + (1-s)*(MX-MN)/2.0


#EOF
