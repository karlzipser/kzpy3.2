#,a

from kzpy3.VT_net2__26March2020_for_no_ros.h5py_write__temp5__init import *

alpha_prev = 0
alpha = 0

start = -3*30
end = start + 9*30
step = 30/3
d = 8

istep = 30


path = opjD(d2p('istep',time_str()))
#path = os.path.realpath(path)
#path = os.path.realpath(path)
os.system('mkdir -p ' + path)


for i in range(6700,200000,istep):



    if L['motor'][i] < 54 or L['encoder'][i] < 2.0:
        cm(i,'motor/encoder')
        continue


    if True:
        
        #A = Pts['xy'][i]

        A = Pts['direct_meo'][9][i-90]
        i_back = i-1-90
        while True:
            #B = Pts['xy'][i_back]
            B = Pts['direct_meo'][9][i_back]
            pd = pts_dist(A,B)
            if pd > 0.5:
                #print k,i,dp(pd)
                break
            else:
                i_back -= 1

        if i - i_back > 200:
            cm(i,'i_back')
            continue
        #xy = na(Pts['xy'][i_back:i+1])

        if True:
            XY = Pts['xy'][i]
            figure(1)
            clf()
            plt_square()
            xylim(XY[0]-d,XY[0]+d,XY[1]-d,XY[1]+d)

        if True:
            xy_xy = na(Pts['xy'][i+start:i+end:step])
            plot(xy_xy[:,0],xy_xy[:,1],'c'+'.-')
        if True:
            #xy = na(Pts['direct_meo'][9][i_back:i+1-90:1])
            xy = na(Pts['xy'][i_back+90:i+1:1])
            plot(xy[:,0],xy[:,1],'kx')

            #xy = xy[range(i_back,len(xy),1)]
            #plot(xy[:,0],xy[:,1],'k.')

    if True:
        m,b = curve_fit(f___,xy[:,0],xy[:,1])[0]
        xs = na([XY[0]-20,XY[0]+20])
        ys = m * xs + b
        plot(xs,ys,'k:')

        alpha_prev = alpha
        alpha = angle_clockwise((1,0),(1,m))
        if np.abs(alpha - alpha_prev) > 5:
            cs = '`wrb'
            ra = True
        else:
            cs = '`m'
            ra = False
        

    
    if True:
        e = 8
        figure(2);clf();plt_square(); xylim(-e,e,-e,e)#-e/4,2*e)
        #A = Pts['direct_meo'][9][i+start] - Pts['direct_meo'][9][i+start-2]
        #alpha = angle_clockwise((0,1),A)
        for q,sym,lne in [(9,'o','-')]:#[(1,',',':'),(4,'.','-'),(9,'o','-'),]:#4,9]:
            for k in Colors:
                rotated_points = rotatePolygon(
                        Pts[k+'_meo'][q][i+start:i+end:step] - A, alpha - 90)

                pts_plot(rotated_points[:-start/step],Colors[k],sym='x:')
                pts_plot(rotated_points[-start/step:],Colors[k],sym='.-')


    if True:
        e = 3
        figure(3);clf();plt_square(); xylim(-e,e,-0.5,e*2)#-e/4,2*e)



        for k in Colors:

            h = []
            for l in range(10):
                h.append(Pts[k+'_meo'][l][i])
            h = na(h)

            rotated_points = rotatePolygon(
                    h - Pts['direct_meo'][0][i], alpha - 90)

            pts_plot(rotated_points,Colors[k],sym='.-')


    img = O['left_image']['vals'][i]
    #img = cv2.resize(img,(168*2,94*2))
    #img[:,168,:] = int((127+255)/2)
    mci(img,title='left_image',scale=1.)
    spause()


    if True:
        imsave(opj(path,d2p(i,'png')),img,format='png')
        plt.savefig(opj(path,d2p(i,'pdf')),format='pdf')
    clp(i,ra=False)#ra)
    







# width of path
# angles over various distances
# input future navigation commands

    if False:
        for k in Colors.keys():
            xy = Pts[k+'9_meo'][i+start:i+end:step]
            plot(xy[:,0],xy[:,1],Colors[k]+'.-')

    if False:
        for j in range(i+start,i+end,step):

            if Pts['angles_meo']['left'][j] < -40:
                pts_plot(Pts['left9_meo'][j],'r',sym='o')
            elif Pts['angles_meo']['left'][j] < -20:
                pts_plot(Pts['left9_meo'][j],'r',sym='.')

            if Pts['angles_meo']['right'][j] > 40:
                pts_plot(Pts['right9_meo'][j],'g',sym='o')
            elif Pts['angles_meo']['right'][j] > 20:
                pts_plot(Pts['right9_meo'][j],'g',sym='.')

            E = Pts['left9_meo'][j]#+step]
            R = Pts['right9_meo'][j]#+step]
            D = Pts['direct9_meo'][j]
            plot_line(R,D,'g:')
            plot_line(E,D,'r:')   

#,b

def f___(x,A,B):
    return A*x+B
    #xy = Pts['direct9_meo'][i+start:i+start + 3*30:step]
    #h = normalized_vector_from_pts(xy)
    #m,b = curve_fit(f___,xy[:,0],xy[:,1])[0]
    #xs = na([XY[0]-20,XY[0]+20])
    #ys = m * xs + b
    #plot(xs,ys,'c')
    #plot([XY[0],XY[0]+ 10*h[0]],[XY[1],XY[1]+ 10*h[1]],'c')
    #plot([XY[0],XY[0]+ m*h[0]],[XY[1],XY[1]+ 10*h[1]],'b')
#EOF
