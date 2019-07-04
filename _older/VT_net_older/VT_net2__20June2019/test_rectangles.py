from kzpy3.vis3 import *
import kzpy3.misc.fit3d as fit3d
import kzpy3.VT_net2__1June2019.rectangles as rectangles
exec(identify_file_str)


if __name__ == '__main__':

    num_rectangle_patterns = 4

    Imgs,xys = rectangles.test_setup(num_rectangle_patterns)

    R = rectangles.Random_black_white_rectangle_collection(
        num_rectangle_patterns=num_rectangle_patterns
    )

    num_steps = 1
    for j in range(0,10000,num_steps):

        if 'setup xys and r0 etc':
            xys_ = []
            for xy in xys:
                rng = np.sqrt(xy[0]**2+xy[1]**2)
                if xy[1] < 0:
                    rng = -rng
                xy[2] = rng
                if rng > 0.72:
                    xys_.append(xy)
            xys = na(xys_)

            i = 10000+j
            l0 = Imgs['L'][i].copy()
            r0 = Imgs['R'][i].copy()
            ln1 = Imgs['L'][i-1].copy()
            rn1 = Imgs['R'][i-1].copy()






        Xys = {
            'now':  xys,
            'prev': xys + 0.0375,
        }

        I = {
            'now':{
                'R':r0,
                'L':l0
            },
            'prev':{
                'R':rn1,
                'L':ln1
            },
        }

        for when in ['now','prev']:
            rectangles.paste_rectangles_into_drive_images(
                Xys[when],
                I[when],
                R
            )




        if '   BLOCK   move points backward':
            xys[:,1] -= 0.0375 * num_steps


        if '   BLOCK   graphics':
            for when in ['now']:#['prev','now']:
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
                    #time.sleep(1.5)
                    raw_enter('prev')
                if when == 'now':
                    k = raw_enter("'q-enter' to quit, ")

        
#EOF


