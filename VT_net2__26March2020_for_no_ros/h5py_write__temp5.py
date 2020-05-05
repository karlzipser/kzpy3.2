#,a

from kzpy3.VT_net2__26March2020_for_no_ros.h5py_write__temp5__init import *



start = 0#-1*30
end = start + 3*30
step = 30/3
d = 8


for i in range(6300,200000,1):


    XY = Pts['xy'][i]
    


    figure(1)
    clf()
    plt_square()
    xylim(XY[0]-d,XY[0]+d,XY[1]-d,XY[1]+d)



    if True:

        xy = na(Pts['xy'][i+start:i+end:step])
        plot(xy[:,0],xy[:,1],'c'+'.-')

        for a in [0,3,6,9]:
            xy = na(Pts['direct_meo'][a][i+start:i+end:step])
            plot(xy[:,0],xy[:,1],'b'+'-')
            #xy = na(Pts['direct'][a][i+start:i+end:step])
            #plot(xy[:,0],xy[:,1],'b'+'x-')



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

    
    if True:
        A = Pts['xy'][i]
        k = i-1
        while True:
            B = Pts['xy'][k]
            pd = pts_dist(A,B)
            if pd > 0.5:
                #print k,i,dp(pd)
                break
            else:
                k -= 1
        xy = na(Pts['xy'][k:i+1])
        plot(xy[:,0],xy[:,1],'k')
        xy = xy[range(0,len(xy),3)]
        plot(xy[:,0],xy[:,1],'k.')

        #h = normalized_vector_from_pts(xy)
        m,b = curve_fit(f___,xy[:,0],xy[:,1])[0]
        xs = na([XY[0]-20,XY[0]+20])
        ys = m * xs + b
        plot(xs,ys,'k:')

        alpha = 90-angle_clockwise((0,1),(m,1))
        cg(alpha)

    if True:
        e = 15
        figure(2);clf();plt_square(); xylim(-e,e,-e,e)#-e/4,2*e)
        #A = Pts['direct_meo'][9][i+start] - Pts['direct_meo'][9][i+start-2]
        #alpha = angle_clockwise((0,1),A)
        for k in Colors:
            pts_plot(
                rotatePolygon(
                    Pts[k+'_meo'][9][i+start:i+end:step] - Pts['xy'][i], alpha),
                Colors[k],sym='.-')

    img = O['left_image']['vals'][i]
    img = cv2.resize(img,(168*2,94*2))
    img[:,168,:] = int((127+255)/2)
    mci(img,title='left_image',scale=1.)
    spause()
    
# width of path
# angles over various distances
# input future navigation commands

    spause()    

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
