from kzpy3.vis3 import *

if 'color_index' not in locals():
    color_list = ['b','g','r','c','m','y','k',]
    color_index = 0

if 'L' not in locals():
    L = h5r("/Users/karlzipser/Desktop/model_car_data_July2018_lrc/locations/local/left_right_center/h5py/Mr_Black_25Jul18_14h44m55s_local_lrc/left_timestamp_metadata_right_ts.h5py")
########################################################################################
########################################################################################
########################################################################################
####
def get_float_pixels_from_xys(
            xys = zeros([10,2]),
            img_shape = (100,100,3),
            col = (1,1),
            row = (1,1),
            box = ((0,10.0),(-1.0,1.0))
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


def function_pts_plot(img,xys,cs):
    img[ xys[:,1].astype(int), xys[:,0].astype(int), : ] = cs

def get_blank_image(x,y):
    return zeros((y,x,3)).astype(np.uint8)

def add_image(img,img_new,xy):
    pass

####
########################################################################################
########################################################################################
########################################################################################

if 'fresh image':# == False:
    img = get_blank_image(1000,100)

if 'gather data':
    data = zeros((1000,2))
    data[:,0] = arange(0,1000)/100.
    data[:,1] = np.sin(data[:,0])
    #data = zeros((1100,2))
    #data[:,0] = range(1100)
    #data[:,1] = 50+0*L['gyro_x'][2000:3100]
    cs = z2_255(np.random.randn(len(data),3))
    cs*=0
    for i in range(3):
        cs[:,i] = np.random.randint(255)

if 'transform to pixel scale':
    xys = get_float_pixels_from_xys(data,shape(img),col=(1,1),row=(1,1),box = ((0,10.0),(-1.0,1.0)))#,box=((0,1100.0),(-50.0,50.0)))

if 'plot':
    function_pts_plot(img,xys,cs)
    mci(img,1)


# col=(1,1),row=(1,1),box=((0,10.0),(-1.0,1.0)),clr=(128,250,99)


#EOF