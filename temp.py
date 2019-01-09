from kzpy3.vis3 import *

if 'color_index' not in locals():
    color_list = ['b','g','r','c','m','y','k',]
    color_index = 0

########################################################################################
########################################################################################
########################################################################################
####
def get_float_pixels_from_xys(
            xys = zeros([10,2]),
            img_shape = (100,100,3),
            col = (1,1),
            row = (1,1),
            box_real = ((0,10.0),(-1.0,1.0))
):
    xy_img_size = (img_shape[0],img_shape[1])

    xy_real_mag = (box_real[0][1] - box_real[0][0],
                    box_real[1][1] - box_real[1][0])
                    
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

    #xys[:,1] = xy_img_size[1] - xys[:,1]
    for i in [0,1]:
        a = xys[:,i]
        a[ a<0 ] = 0
        a[ a>=xy_img_size[i] ] = xy_img_size[i]

    return xys


def function_pts_plot(img,xys,cs):
    img[ xys[:,1].astype(int), xys[:,0].astype(int), : ] = cs

def get_blank_image(x,y):
    return zeros((y,x,3)).astype(np.uint8)

####
########################################################################################
########################################################################################
########################################################################################

img = get_blank_image(163,369)

if 'gather data':
    data = zeros((1000,2))
    data[:,0] = arange(0,1000)/100.
    data[:,1] = np.sin(data[:,0])
    cs = z2_255(np.random.randn(len(data),3))

xys = get_float_pixels_from_xys(data,shape(img),col=(1,10),row=(1,10))

#img[ xys[:,0].astype(int), xys[:,1].astype(int), : ] = cs
function_pts_plot(img,xys,cs)

mi(img,1)
figure(2,figsize=(3,3))
pts_plot(xys)
spause()




#EOF