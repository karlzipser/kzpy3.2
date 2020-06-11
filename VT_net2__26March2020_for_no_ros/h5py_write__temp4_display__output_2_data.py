from kzpy3.vis3 import *

#,a


Arguments = {
    'run_name':'tegra-ubuntu_31Oct18_16h06m32s',
}


Colors = {'direct':'b','left':'r','right':'g'}

if True:

    def vec(heading,encoder,motor,sample_frequency=30.,vel_encoding_coeficient=1.0/2.6): #2.3): #3.33
        velocity = encoder * vel_encoding_coeficient # rough guess
        if motor < 49:
            velocity *= -1.0
        a = [0,1]
        a = array(rotatePoint([0,0],a,heading))
        a *= velocity/sample_frequency
        return array(a)


    if 'O' not in locals():
        L,O,__flip = open_run2(Arguments['run_name'])


    if 'Pts' not in locals():
        Pts = {
            'left':{},
            'right':{},
            'direct':{},
        }
        for k in Pts:
            for i in range(10):
                Pts[k][i] = []



        Pts['xy'] = [na([0,0])]

        for i in rlen(L['motor']):
            a = vec(
                L['gyro_heading_x_meo'][i],
                L['encoder_meo'][i],
                L['motor'][i],
            )
            Pts['xy'].append(Pts['xy'][-1]+a)








start = -2*30
end = start + 2.5*minutes*30; end = int(end)
step = 30/3
d = 50
marker_size = 40


start = 6500
end = 10000

CA()


for fig in [0]:#range(5):

    pts_plot(Pts['xy'][start:end],'k')
    for i in range(start,end):#200000+6500,1):

        if True:
            XY = Pts['xy'][i]
            #figure(1,figsize=(16,16));clf();
            plot((-41,-40),(3,3),'k',linewidth=1)
        

        if fig in [3,4]:
            for k in ['left','right']:
                xy = Pts[k+'9_meo'][i+start:i+end:step]
                plot(xy[:,0],xy[:,1],Colors[k]+'-',linewidth=3)




        cy(i)
        if False:
            for j in range(i+start,i+end,1):


                cg(i,j)

                if fig in [0]:
                    xy = na([Pts['direct0_meo'][j]])
                    plot(xy[:,0],xy[:,1],'k.')

                if j % step != 0:
                    continue
                
                if fig in [1,2,3]: # dead-reckoning trajectory
                    for k in ['left','right']:
                        m = []
                        for l in range(10):
                            xy = Pts[k+str(l)+'_meo'][j+l]
                            m.append(xy)
                        pts_plot(m,Colors[k],sym='-')



                if fig in [2,3,4]: # markers
                    for k in ['left','right']:
                        a = min(np.abs(Pts['angles_meo'][k][j]),40)
                        marker_size = int(a/2.)
                        pts_plot(Pts[k+'9_meo'][j],Colors[k],sym='.',ms=marker_size)


        
        plt_square()

        spause()

        if False:
            e = 15
            figure(2);clf();plt_square(); xylim(-e,e,-e/4,2*e)
            A = Pts['direct9_meo'][i+start] - Pts['direct9_meo'][i+start-2]
            alpha = angle_clockwise((0,1),A)
            for k in Colors:
                pts_plot(
                    rotatePolygon(
                        Pts[k+'9_meo'][i+start:i+end:step] -Pts['direct9_meo'][i+start-1],alpha),
                    Colors[k],sym='.-')



        break

    spause()
    #plt.savefig(opjD('fig'+str(fig)+'a.pdf'),format='pdf')
    #xylim(-47,-37,0,9)
    #plt.savefig(opjD('fig'+str(fig)+'b.pdf'),format='pdf')
    








#,b

#EOF
