#!/usr/bin/env python

from kzpy3.vis3 import *
import sensor_msgs
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2
import rospy

if 'mode' in Arguments:
    MODE = Arguments['mode']
else:
    MODE = 'offline'

Names = {
    "x":"x","angle":"y","depth":"z","t":"t",
    "reflectivity":"reflectivity",
    "intensity":"intensity",
    "ring":"ring"}



def get_cv2_img(img):
    img = (256*z2o(img)).astype(np.uint8)
    s = shape(img)
    a = s[0]
    b = s[1]
    c = zeros((a,b,3),np.uint8)
    for i in range(3):
        c[:,:,i] = img
    return c



def Image_Stack(Names,fields_to_show):

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
    D['Names'] = Names
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

            y = Image[Names['angle']][32,:]
            dy_bad_min = 2*np.pi / 1024.0 * 2
            dy_bad_max = 1.9*np.pi
            for i in range(1,len(y)):
                dy = y[i]-y[i-1]
                if dy > dy_bad_min and dy < dy_bad_max:
                    corrupt_frame = True

            g = (Image[Names['angle']][32,:]*1000).astype(int)

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

                fn = Names[fn_]

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

if MODE == 'live':
    P = []
    calls = 0
    calls_prev = 0
    ABORT = False

    field_names=("x","y","z","t","reflectivity","intensity","ring")

    def points__callback(msg):
        if ABORT:
            return
        global P
        global calls
        calls += 1
        valv_temp = list(pc2.read_points(msg,skip_nans=False,field_names=field_names))
        valv_temp = na(valv_temp)
        valv_temp[np.isnan(valv_temp)] = 0
        P.append(valv_temp)




    if False:
        Images = lo('/home/karlzipser/Desktop/Images_03Nov18_12h32m24s.pkl' )
        for i in rlen(Images['reflectivity']):
            mci(get_cv2_img(Images['intensity'][i]),delay=100)

    if __name__ == '__main__':
        

        rospy.init_node('test_pointclouds')

        rospy.Subscriber('/os1_node/points', PointCloud2, points__callback)

        CA()

        ctr = 0

        Images = {}
        for q in field_names:
            Images[q] = []

        waiting = Timer(1)
        while calls < 1:
            waiting.message('waiting for data')
            time.sleep(0.01)

        timer = Timer(5*60)

        cg("processing ROSbag data...")

        while not timer.check():

            waiting.message(d2s('waiting for dataprocessing ROSbag data...',time_str()))

            try:
                calls_ = calls
                if calls_ > calls_prev:
                    p = P[-1]
                    a = np.resize(p,(1024,64,len(field_names)))
                    r = range(1,64,4)
                    b = a[:,r,:]
                    for i in rlen(field_names):
                        c = b[:,:,i]
                        d = cv2.resize(c.astype(float),(64,1024))
                        e = d.transpose(1,0)
                        Images[field_names[i]].append(e)
                    #spause()
                    calls_prev = calls_

            except:
                cs('exception',calls)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                CS_('Exception!',emphasis=True)
                CS_(d2s(exc_type,file_name,exc_tb.tb_lineno),emphasis=False)
        cg("Done.")
        if True:
            so(opjD('Images_'+time_str()),Images)












elif MODE == 'offline':

    fields_to_show = ("depth","reflectivity","intensity")
    #fields_to_show = sorted(Names.keys())#["x"]#,"intensity")

    
    ###############################
    #    
    Image_stack = Image_Stack(Names,fields_to_show)
    #
    ###############################
    

    if 'Images' not in locals():
        Images = lo('/home/karlzipser/Desktop/Images_03Nov18_12h32m24s.pkl' )
        #Images = lo("/home/karlzipser/Desktop/Images_04Nov18_00h04m14s.pkl")
        pass

    duration_timer = Timer(5)

    CA()

    for k in range(2,len(an_element(Images))):

        if duration_timer.check():
            cb("Duration timer check, breaking.")
            break

        Image = {}
        for q in Images.keys():
            Image[q] = Images[q][k]

        ###############################
        #    
        Image_stack['show'](Image)
        #
        ###############################

else:
    d2n("Error, unknown mode '",MODE,"'")
#EOF