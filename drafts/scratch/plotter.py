from kzpy3.vis3 import *
from __future__ import division
assert(1/2 == 0.5)

if 'color_index' not in locals():
    color_list = ['b','g','r','c','m','y','k',]
    color_index = 0

if 'L' not in locals():
    L = h5r("/Users/karlzipser/Desktop/model_car_data_July2018_lrc/locations/local/left_right_center/h5py/Mr_Black_25Jul18_14h44m55s_local_lrc/left_timestamp_metadata_right_ts.h5py")

########################################################################################
########################################################################################
########################################################################################
####
def get_float_pixels(
            xys,
            img_shape,
            col,
            row,
            box
):

    xy_img_size = (img_shape[1],img_shape[0])

    xy_real_mag = (box[0][1] - box[0][0],
                    box[1][1] - box[1][0])
                    
    row_height = xy_img_size[1]/(1.0*row[1])
    col_width  = xy_img_size[0]/(1.0*col[1])

    xy_real_to_pixels = (
        xy_img_size[0]/(1.0*xy_real_mag[0])/(1.0*col[1]),
        xy_img_size[1]/(1.0*xy_real_mag[1])/(1.0*row[1]))
    
    xy_pixel_offset = ( col_width*(col[0]-1),
                        row_height*(row[0]-1))

    xys[:,0] *= xy_real_to_pixels[0]
    xys[:,1] *= xy_real_to_pixels[1]
    xys[:,0] -= xys[:,0].min()
    xys[:,1] -= xys[:,1].min()
    xys[:,0] += xy_pixel_offset[0]
    xys[:,1] += xy_pixel_offset[1]

    xys[:,1] = xy_img_size[1] - xys[:,1]
    for i in [0,1]:
        a = xys[:,i]
        a[ a<0 ] = 0
        a[ a>=xy_img_size[i] ] = xy_img_size[i]-1

    return xys


def img_pts_plot(img,xys,cs):
    img[ xys[:,1].astype(int), xys[:,0].astype(int), : ] = cs

def get_blank_image(x,y,rgb=(0,0,0)):
    return zeros((y,x,3)).astype(np.uint8) + na(rgb).astype(np.uint8)



def place_image_in_image(a,b,xy_left_top,xyscale):
    if xyscale != None:
        assert type(xyscale) == tuple
        assert len(xyscale) == 2
        b = cv2.resize(b,xyscale)

    xy_left_top = na(xy_left_top).astype(int)
    a_xy_size = na((shape(a)[1],shape(a)[0])).astype(int)
    b_xy_size = na((shape(b)[1],shape(b)[0])).astype(int)

    xy_bottom_right = xy_left_top + b_xy_size

    try:
        a[xy_left_top[1]:xy_bottom_right[1],xy_left_top[0]:xy_bottom_right[0]] = b
    except Exception as e:
        cr("*** Error in placing image b into image a ***")
        cr("xy_left_top =",xy_left_top)
        cr("xyscale =",xyscale)
        cr("a_xy_size =",a_xy_size)
        cr("b_xy_size =",b_xy_size)
        cr("xy_bottom_right =",xy_bottom_right)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        CS_('Exception!',emphasis=True)
        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)    




def place_image_in_image(a,b,xy_left_top,xy_scale):
    if xy_scale != None:
        assert type(xy_scale) == tuple
        assert len(xy_scale) == 2
        b = cv2.resize(b,xy_scale)

    xy_left_top = na(xy_left_top).astype(int)
    a_xy_size = na((shape(a)[1],shape(a)[0])).astype(int)
    print shape(b)
    b_xy_size = na((shape(b)[1],shape(b)[0])).astype(int)
    xy_bottom_right = xy_left_top + b_xy_size

    try:
        a[xy_left_top[1]:xy_bottom_right[1],xy_left_top[0]:xy_bottom_right[0]] = b
    except Exception as e:
        cr("*** Error in placing image b into image a ***")
        cr("xy_left_top =",xy_left_top)
        cr("xy_scale =",xy_scale)
        cr("a_xy_size =",a_xy_size)
        cr("b_xy_size =",b_xy_size)
        cr("xy_bottom_right =",xy_bottom_right)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        CS_('Exception!',emphasis=True)
        CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)    


def place_image_in_image2(a,b,row,col):

    a_xy_size = na((shape(a)[1],shape(a)[0]))
    b_xy_size = na((shape(b)[1],shape(b)[0]))

    row_height = a_xy_size[1]/row[1]
    col_width  = a_xy_size[0]/col[1]

    b_aspect_ratio = b_xy_size[0]/b_xy_size[1]
    col_row_aspect_ratio = col_width/row_height

    xy_scale = 0
    if b_aspect_ratio >= col_row_aspect_ratio:
        xy_scale = (int(col_width),int(col_width/b_aspect_ratio))
        cr('a')
    else:
        cr('b')
        xy_scale = (int(row_height*b_aspect_ratio),int(row_height))

    xy_left_top = ((col[0]-1)*col_width,(row[0]-1)*row_height)

    print (int(col_width),int(col_width*b_aspect_ratio))
    print (int(row_height*b_aspect_ratio),int(row_height))
    print shape(b),b_xy_size,xy_scale
    place_image_in_image(a,b,((col[0]-1)*col_width,(row[0]-1)*row_height),xy_scale)

####
########################################################################################
########################################################################################
########################################################################################
DATA = L['steer'][:]
MX,MN = -2**16,2**16
for ii in range(0,10000,9):
    if 'fresh image':# == False:
        img = get_blank_image(1000,200)

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
