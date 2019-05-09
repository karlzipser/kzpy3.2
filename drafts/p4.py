from kzpy3.vis3 import *
import kzpy3.misc.fit3d as fit3d

if 'O' not in locals():
    if using_osx():
        O=h5r('/Users/karlzipser/Desktop_19Feb19_08h49m53s/model_car_data_July2018_lrc/locations/local/left_right_center/h5py/Mr_Black_24Jul18_20h04m17s_local_lrc/original_timestamp_data.h5py')
    else:
        O = h5r('/home/karlzipser/Desktop/Data/1_TB_Samsung_n1/tu_8to12Oct2018/locations/local/left_right_center/h5py/tegra-ubuntu_08Oct18_19h15m15s/original_timestamp_data.h5py')
    I = {}
    I['L'] = O['left_image']['vals']
    I['R'] = O['right_image']['vals']


def pt_in_2D_to_image(x2d,y2d):
    b = fit3d.Point3(x2d,0,y2d)
    c = fit3d.project(b, fit3d.mat)
    return c.x,c.y

def pt_in_2D_to_image_with_disparity(x2d,y2d):
    m = 0.47885706 # from Mr. Blue
    b = -21.76993126
    b_ = fit3d.Point3(x2d,0,y2d)
    c = fit3d.project(b_, fit3d.mat)
    disparity = max(0,c.y*m+b)
    return c.x,c.y,disparity

def width_at_y(w,y):
    m = 4.97
    b = -242.
    return max(0.,w*(m*y + b))


def pt_in_2D_to_image_with_disparity_and_width(x_meters,y_meters,width_meters):
    x,y,disparity = pt_in_2D_to_image_with_disparity(x_meters,y_meters)
    width = width_at_y(width_meters,y)
    return x,y,disparity,width

def paste_img_into_img(a,b,a_base_center):
    shape_a = shape(a)
    shape_b = shape(b)
    a_width = shape_a[1]
    

m = 0.47885706 # from Mr. Blue
b = -21.76993126

backup_parameter = 1.0

if False:
    for j in range(100):
        i = np.random.randint(5000,len(I['L']))
        mi(I['R'][i],'R')
        mi(I['L'][i],'L')
        for x_ in arange(-0.5,0.51,0.25):
            for y_ in arange(0.,3.1,0.25):
                x,y = pt_in_2D_to_image(x_,y_-backup_parameter)
                for s in ['L','R']:
                    fig = figure(s)
                    if s == 'L':
                        xy_list = [[x,y]]
                    else:
                        dx = max(0,y*m+b)
                        xy_list = [[x-dx,y]]
                    x = xy_list[0][0]
                    y = xy_list[0][1]
                    good = True
                    if x < 0 or x >= 168:
                        good = False
                    elif y < 0 or y >= 94:
                        good = False
                    if good:
                        plot(x,y,'r.')

                    if s == 'R':
                        cg(dx)
        spause()
        raw_enter()



if True:
    D = {}
    D['dx'] = []
    D['y'] = []
    for y_ in arange(1.,30.,0.1):
        x0,y = pt_in_2D_to_image(0,y_-backup_parameter)
        x1,y = pt_in_2D_to_image(1.,y_-backup_parameter)
        D['dx'].append(x1-x0)
        D['y'].append(y)
    clf()
    plot(D['y'],D['dx'],'.')

    def line(x,m,b):
        return m * x + b

    popt, pcov = curve_fit(line, D['y'], D['dx'])

    h = range(94)
    d = []
    for q in h:
        d.append( popt[0]*q+popt[1])
    plot(h,d,'k')
    m = 4.97
    b = -242.

 
#EOF


