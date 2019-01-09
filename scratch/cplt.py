
########################################################################################
########################################################################################
########################################################################################
#### pip install screeninfo

def Cv2Plot(
        img,
        x_pixels_per=1,
        y_pixels_per=1,
        x_origin=None,
        y_origin=None
    ):

    height_in_pixels = shape(img)[0]
    width_in_pixels = shape(img)[1]

    if x_origin == None:
        x_origin = 0.5
    if y_origin == None:
        y_origin = 0.5
    D = {}
    D['verbose'] = False
    D['image'] = img
    assert len(shape(img)) == 3
    assert type(img[0,0,0]) == np.uint8

    def function_show(autocontrast=True,delay=1,title='image',scale=1.0):
        img = D['image']
        if autocontrast:
            img = z2_255_by_channel(img) # make copy?
        mci(img,scale=scale,delay=delay,title=title)

    def function_safe(px,py):
        if px >= 0:
            if py >= 0:
                if py < height_in_pixels:
                    if px < width_in_pixels:
                        return True
        if D['verbose']:
            cr('not safe')
        return False

    def function_get_pixel(x,y):
        px = x * x_pixels_per
        py = -y * y_pixels_per
        px += x_origin * width_in_pixels
        py += y_origin * height_in_pixels
        if D['verbose']:
            cb(x,y,"->",px,py)
        return intr(px),intr(py)

    def function_plot_point_xy_version(x,y,c=[255,255,255],add_mode=False):
        px,py = D['get pixel'](x,y)
        if D['safe?'](px,py):
            if not add_mode:
                D['image'][py,px,:] = c
            else:
                D['image'][py,px,:] += na(c,np.uint8)

    def function_pts_plot(xys,c=[255,255,255],add_mode=False):
        if type(c) == str:
            if add_mode:
                n = 1
            else:
                n = 255
            if c == 'r':
                c = [n,0,0]
            elif c == 'g':
                c = [0,n,0]
            elif c == 'b':
                c = [0,0,n]  
            else:
                cr('warning, unknown color:',c)
                c = [255,255,255]
        for i in rlen(xys):
            D['plot point (xy_version)'](xys[i,0],xys[i,1],c,add_mode)

    def function_clear():
        D['image'] *= 0
        
    D['show'] = function_show
    D['safe?'] = function_safe
    D['plot point (xy_version)'] = function_plot_point_xy_version
    D['get pixel'] = function_get_pixel
    D['pts_plot'] = function_pts_plot
    D['clear'] = function_clear
    return D
####
########################################################################################
########################################################################################
########################################################################################
CA()
img = z2_255(np.random.randn(500,1000,3))
C = Cv2Plot(img,2,10,0.1,0.3)
a = 4.0
f = 0.2
n = 1000
ctr = 0
timer = Timer(10)
while not timer.check():
    xys = zeros((n,2))
    xys[:,0] = na(range(n))
    xys[:,1] = a*np.sin(f*(xys[:,0]-ctr))
    xys[:,0] /= 2.5
    C['clear']()
    C['pts_plot'](xys,[255,255,255])
    C['pts_plot'](xys/2.0+0.1,[255,255,0])
    C['show']()
    if ctr == 0:
        cv2.moveWindow('image',0,0)
    ctr += 1
    #clf();pts_plot(xys);spause()




#EOF
