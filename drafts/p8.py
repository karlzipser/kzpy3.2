from kzpy3.vis3 import *
import kzpy3.misc.fit3d as fit3d
exec(identify_file_str)
"""
def abc(
    left_now,
    right_now,
    xy_ranges,
    R,
    need_to_sort_ranges=False
):
    if need_to_sort_ranges:
        xy_ranges = na(xy_ranges)
        xy_ranges = xy_ranges[xy_ranges[:,2].argsort()]
    I = {
        'L':{
            'now':left_now,
        },
        'R':{
            'now':right_now,
        },
    }
    for r in len(xy_ranges):
    
        x_,y_ = xy_ranges[r,0],xy_ranges[r,1]

        x,y,disparity,width = pt_in_2D_to_image_with_disparity_and_width(x_,y_,0.1)

        if width > 0:
            width = intr(width)
            if width < 1:
                width = 1
            f = R[width][np.random.choice(len(R[width]))]

            for s in ['L','R']:
                
                x_ = x

                if s == 'R':

                    x_ -= disparity

                good = True
                if x_ < 0 or x_ >= 168:
                    good = False
                elif y < 0 or y >= 94:
                    good = False

                if good: 
                    I[s][w] = place_img_f_in_img_g(x_,y,f,I[s],bottom=1,center=1)

    return I['L'],I['R']





def abc(
    left_now,
    right_now,
    left_prev,
    right_prev,
    xy_ranges,
    need_to_sort_ranges=False
):
    if need_to_sort_ranges:
        xy_ranges = na(xy_ranges)
        xy_ranges = xy_ranges[xy_ranges[:,2].argsort()]

    I = {
        'L':{
            'now':left_now,
            'prev':left_prev,
        },
        'R':{
            'now':right_now,
            'prev':right_prev,
        },
    }

    for r in len(xy_ranges):
    
        x_,y_ = xy_ranges[r,0],xy_ranges[r,1]

        x,y,disparity,width = pt_in_2D_to_image_with_disparity_and_width(x_,y_,0.1)

        if width > 0:
            width = intr(width)
            if width < 1:
                width = 1
            f = R[width][np.random.choice(len(R[width]))]

            for w in ['now','prev']:

                for s in ['L','R']:
                    
                    x_ = x

                    if s == 'R':

                        x_ -= disparity

                    good = True
                    if x_ < 0 or x_ >= 168:
                        good = False
                    elif y < 0 or y >= 94:
                        good = False

                    if good: 
                        I[s][w] = place_img_f_in_img_g(x_,y,f,I[s],bottom=1,center=1)

    return I['L']['now'],I['R']['now'],I['L']['prev'],I['R']['prev']
"""





def pt_in_2D_to_image(x_meters,y_meters):
    b = fit3d.Point3(x_meters,0,y_meters)
    c = fit3d.project(b, fit3d.mat)
    return c.x,c.y

def pt_in_2D_to_image_with_disparity(
    x_meters,
    y_meters,
    m_disparity=0.47885706 ,# from Mr. Blue
    b_disparity=-21.76993126
):
    b_ = fit3d.Point3(x_meters,0,y_meters)
    c = fit3d.project(b_, fit3d.mat)
    disparity = max(0,c.y*m_disparity+b_disparity)
    return c.x,c.y,disparity

def width_at_y(
    w,
    y,
    m_width = 4.97,
    b_width = -242.
):
    return max(0.,w*(m_width*y + b_width))

def pt_in_2D_to_image_with_disparity_and_width(
    x_meters,
    y_meters,
    width_meters,
    backup_parameter=1.
):
    x,y,disparity = pt_in_2D_to_image_with_disparity(x_meters,y_meters-backup_parameter)
    width = width_at_y(width_meters,y)
    return x,y,disparity,width


    

def random_black_white_rectangle(width,height,scale):
    a = np.random.randint(
        high=2,
        low=0,
        size=(height,width)
    )
    b = zeros((height,width,3))
    for i in range(3):
        b[:,:,i] = a
    c = cv2.resize(
        b,
        (intr(width*scale),intr(height*scale)),
        interpolation=0
    )
    d = z55(c)
    return(d)

def Random_black_white_rectangle_collection(
    max_width = 20,width=4,height=16
):
    R = {}
    for i in range(2,max_width+1):
        if i not in R:
            R[i] = []
        if not is_even(i):
            R[i] = R[i-1]
        else:
            for j in range(5):
                R[i].append(random_black_white_rectangle(width,height,i/4.))
    R[1] = R[2]
    for i in range(max_width+1,4*max_width):
        R[i] = R[max_width]
    return R



if __name__ == '__main__':

    R = Random_black_white_rectangle_collection()


    if 'O' not in locals():
        if using_osx():
            O=h5r('/Users/karlzipser/Desktop_19Feb19_08h49m53s/model_car_data_July2018_lrc/locations/local/left_right_center/h5py/Mr_Black_24Jul18_20h04m17s_local_lrc/original_timestamp_data.h5py')
        else:
            O = h5r('/home/karlzipser/Desktop/Data/1_TB_Samsung_n1/tu_8to12Oct2018/locations/local/left_right_center/h5py/tegra-ubuntu_08Oct18_19h15m15s/original_timestamp_data.h5py')
        Imgs = {}
        Imgs['L'] = O['left_image']['vals']
        Imgs['R'] = O['right_image']['vals']



    xy_ranges = []
    for x_ in arange(-0.5,0.51,0.25):
        for y_ in arange(0.,3.1,0.25):
            xy_ranges.append([x_,y_,np.sqrt(x_**2+y_**2)])

    xy_ranges = na(xy_ranges)
    xy_ranges = xy_ranges[xy_ranges[:,2].argsort()]

    for j in range(100):
        i = np.random.randint(5000,len(Imgs['L']))
        I = {'R':Imgs['R'][i],'L':Imgs['L'][i]}


        for r in range(len(xy_ranges)-1,0,-1):

            x_,y_ = xy_ranges[r,0],xy_ranges[r,1]
            x,y,disparity,width = \
                pt_in_2D_to_image_with_disparity_and_width(x_,y_,0.1)
            if width > 0 and np.random.random() < 0.15:
                width = intr(width)
                if width < 1:
                    width = 1
                f = R[width][np.random.choice(len(R[width]))]
            else:
                f = None
            for s in ['L','R']:
                fig = figure(s)
                if s == 'L':
                    xy_list = [[x,y]]
                else:
                    xy_list = [[x-disparity,y]]
                x = xy_list[0][0]
                y = xy_list[0][1]
                good = True
                if x < 0 or x >= 168:
                    good = False
                elif y < 0 or y >= 94:
                    good = False
                if good: 
                    if f != None:
                        I[s] = place_img_f_in_img_g(x,y,f,I[s],bottom=1,center=1)
        for s in ['L','R']:
            mi(I[s],s)
        spause()
        k = raw_enter()
        if k == 'q':
            break


#EOF

