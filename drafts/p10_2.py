from kzpy3.vis3 import *
import kzpy3.misc.fit3d as fit3d
exec(identify_file_str)


def random_black_white_rectangle(width,height):
    a = np.random.randint(
        high=2,
        low=0,
        size=(height,width)
    )
    b = zeros((height,width,3))
    for i in range(3):
        b[:,:,i] = a
    d = z55(b)
    return(d)

def Random_black_white_rectangle_collection(
    max_width=20,
    width=8,
    height=16,
    num_rectangle_patterns=1,
    even_only=False
):
    rectangles = []
    for i in range(num_rectangle_patterns):
        rectangles.append(random_black_white_rectangle(width,height))
    R = {}
    for i in range(2,max_width+1):
        if i not in R:
            R[i] = []
        if even_only and not is_even(i):
            R[i] = R[i-1]
        else:
            for j in range(num_rectangle_patterns):
                c = cv2.resize(
                    rectangles[j],
                    (intr(width*i/4.),intr(height*i/4.)),
                    interpolation=0
                )
                R[i].append(c)
    R[1] = R[2]
    for i in range(max_width+1,100000):
        R[i] = R[max_width]
    return R


def paste_rectangles_into_drive_images(
    xys,
    I,
    R
):
    for xy in xys:
        x_,y_,rng,rectangle_pattern = xy[0],xy[1],xy[2],int(xy[3])
        x,y,disparity,width = fit3d.pt_in_2D_to_image_with_disparity_and_width(x_,y_,0.1)
        width = intr(width)
        if width > 0 and rng > 0.:
            f = R[width][rectangle_pattern]
            for s in ['L','R']:  
                if s == 'L':
                    x_ = x
                else:
                    x_ = x - disparity
                try:
                    I[s] = place_img_f_in_img_g(x_,y,f,I[s],bottom=1,center=1)
                except:
                    cr('place_img_f_in_img_g failure')


def setup():
    if '   BLOCK   set up rectangles':
        num_rectangle_patterns = 15
        R = Random_black_white_rectangle_collection( ###########
            num_rectangle_patterns=num_rectangle_patterns
        )
    if '   BLOCK   access file images':
        if 'O' not in locals():
            if using_osx():
                O = h5r('/Users/karlzipser/Desktop_19Feb19_08h49m53s/model_car_data_July2018_lrc/locations/local/left_right_center/h5py/Mr_Black_24Jul18_20h04m17s_local_lrc/original_timestamp_data.h5py')
            else:
                O = h5r('/home/karlzipser/Desktop/Data/1_TB_Samsung_n1/tu_8to12Oct2018/locations/local/left_right_center/h5py/tegra-ubuntu_08Oct18_19h15m15s/original_timestamp_data.h5py')
            Imgs = {}
            Imgs['L'] = O['left_image']['vals']
            Imgs['R'] = O['right_image']['vals']
    if '   BLOCK   set up ranges':
        xy_ranges = []
        for x_ in arange(-0.5,0.51,0.25):
            for y_ in arange(0.,13.1,0.25):
                q = rndint(num_rectangle_patterns)
                xy_ranges.append([x_,y_,np.sqrt(x_**2+y_**2),q])
        xy_ranges = na(xy_ranges)
        xy_ranges = xy_ranges[xy_ranges[:,2].argsort()]

        xys = []
        for r in rlen(xy_ranges):
            if np.random.random() < 0.11:
                xys.append(xy_ranges[r,:])
        xys = sort_by_column(xys,2,reverse=True) ##############
    return R,Imgs,xys

if __name__ == '__main__':


    R,Imgs,xys = setup()
    num_steps = 1
    for j in range(0,10000,num_steps):

        if '   BLOCK   select xy points':
            xys_ = []
            for xy in xys:
                rng = np.sqrt(xy[0]**2+xy[1]**2)
                if xy[1] < 0:
                    rng = -rng
                xy[2] = rng
                if rng > 0.72:
                    xys_.append(xy)
            xys = na(xys_)
            Xys = {}
            for when in ['now','prev']:
                Xys[when] = xys.copy()
                if when == 'prev':
                    Xys[when][:,1] += 0.0375

        if '   BLOCK   select images':
            i = 10000+j
            I = {
                'now':{'R':Imgs['R'][i].copy(),'L':Imgs['L'][i].copy()},
                'prev':{'R':Imgs['R'][i-1].copy(),'L':Imgs['L'][i-1].copy()},
            }


        if '   BLOCK   create quartet images': 
            for when in ['now','prev']:
                paste_rectangles_into_drive_images(
                    Xys[when],
                    I[when],
                    R
                )


        if '   BLOCK   move points backward':
            xys[:,1] -= 0.0375 * num_steps


        if '   BLOCK   graphics':
            for when in ['prev','now']:
                print when,j
                shape_ = np.shape(I[when]['L'])
                width,height = shape_[1],shape_[0]
                img_now = np.zeros((height,2*width+int(width/16),3),np.uint8) + 127
                img_now[:,:width,:] =   I[when]['R']
                img_now[:,-width:,:] =  I[when]['L']
                figure('when',figsize=(12,4))
                mi(img_now,'when')
                spause()
                if when == 'prev':
                    plot([0,50],[0,50],'r')
                    spause()
                    time.sleep(1.5)
                    raw_enter('prev')
                if when == 'now':
                    k = raw_enter("'q-enter' to quit, ")
                #if k == 'q':
                #    break
        
#EOF

