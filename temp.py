


########################################################################################
########################################################################################
########################################################################################
####
def get_xys(
            xys = zeros([10,2]),
            img_shape = (100,100,3),
            col = (1,1),
            row = (1,1),
            box_real = ((0,10.0),(-1.0,1.0)),
    ):

    #assert len(img_shape) == 2

    xy_img_size = (img_shape[0],img_shape[1])

    xy_real_mag = (box_real[0][1] - box_real[0][0],
                    box_real[1][1] - box_real[1][0])
                    
    row_height = xy_img_size[1]/(1.0*row[1])
    col_width  = xy_img_size[0]/(1.0*col[1])

    xy_real_to_pixels = (
        xy_img_size[0]/(1.0*xy_real_mag[0])/(1.0*col[1]),
        xy_img_size[1]/(1.0*xy_real_mag[1])/(1.0*row[1]),
    )

    xy_pixel_offset = (
                        col_width*(col[0]-1),
                        row_height*(row[0]-1),
    )


    xys[:,0] *= xy_real_to_pixels[0]
    xys[:,1] *= xy_real_to_pixels[1]
    xys[:,0] -= xys[:,0].min()
    xys[:,1] -= xys[:,1].min()
    xys[:,0] += xy_pixel_offset[0]
    xys[:,1] += xy_pixel_offset[1]

    return xys

####
########################################################################################
########################################################################################
########################################################################################



if 'color_index' not in locals():
    color_list = ['b','g','r','c','m','y','k',]
    color_index = 0
    data = zeros((100,2))
    data[:,0] = arange(0,100)/10.
    data[:,1] = np.sin(data[:,0])
    img = zeros((200,87,3),np.uint8)

xys = get_xys(data,shape(img))

if color_index >= len(color_list):
    color_index = 0
pts_plot(xys,color_list[color_index])
color_index += 1


