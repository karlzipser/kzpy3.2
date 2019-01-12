from __future__ import division
assert(1/2 == 0.5)

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

if True:
    b=bb.copy()
    #a=get_blank_image(1000,1100,(90,60,31))
    xy_left_top = (0,0)
    xy_scale = (30,30)
    place_image_in_image2(a,b,row=(2,5),col=(5,5));mi(a)

