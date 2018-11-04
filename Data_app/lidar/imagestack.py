#!/usr/bin/env python

from kzpy3.vis3 import *



def get_cv2_img(img):
    img = (256*z2o(img)).astype(np.uint8)
    s = shape(img)
    a = s[0]
    b = s[1]
    c = zeros((a,b,3),np.uint8)
    for i in range(3):
        c[:,:,i] = img
    return c



def Image_Stack(_,fields_to_show):

    D = {}

    Y = {}
    mx = 6290
    for d in range(0,mx):
        v = int(1024 * d / (1.0*mx))
        if v > 1023:
            v = 1023
        Y[d] = v

    j = 0
    for i in range(sorted(Y.keys())[-1]):
        if i in Y:
            j = Y[i]
        Y[i] = j

    D['Y'] = Y
    D['spacer'] = zeros((16,1024))+0.5
    D['Img_prev'] = {}
    D['fields_to_show'] = fields_to_show



    def _show(Image):

        if 'check in':
            Y = D['Y']
            spacer = D['spacer']
            Img_prev = D['Img_prev']

        #if True:
        try:

            img_stack = spacer.copy()
            
            corrupt_frame = False

            y = Image['y'][32,:]
            dy_bad_min = 2*np.pi / 1024.0 * 2
            dy_bad_max = 1.9*np.pi
            for i in range(1,len(y)):
                dy = y[i]-y[i-1]
                if dy > dy_bad_min and dy < dy_bad_max:
                    corrupt_frame = True

            g = (Image['y'][32,:]*1000).astype(int)

            h = zeros(1024,int)

            prev = 0
            for j in rlen(g):
                if g[j] in Y:
                    h[j] = Y[g[j]]
                    temp = h[j]-prev
                    if temp != 1:
                        print temp
                    if h[j]-prev == 2:
                        h[j] = h[j]-1
                    prev = h[j]

            imgs = []
            
            for fn_ in D['fields_to_show']:

                fn = fn_

                img = Image[fn]

                img_unshifted = img * 0

                for l in range(1024):
                    img_unshifted[:,h[l]] = img[:,l]

                if corrupt_frame:
                    if fn in Img_prev:
                        img_zeros = img_unshifted==0
                        img_unshifted[img_zeros] = Img_prev[fn][img_zeros]

                img = img_unshifted

                use_img = img

                Img_prev[fn] = use_img.copy()

                if corrupt_frame:
                    cr("corrupt frame",fn)

                img_stack = np.concatenate((img_stack,z2o(use_img),spacer))

                
            mci(get_cv2_img(img_stack),delay=100,title='data',scale=3)
            #mi(img_stack)
            #raw_enter()
        #else:
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            CS_('Exception!',emphasis=True)
            CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)

        if 'check out':
            D['Img_prev'] = Img_prev

    D['show'] = _show

    return D

#EOF