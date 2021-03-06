from kzpy3.vis3 import *
exec(identify_file_str)

CA()

graphics_timer = None


def graphics_function(N,M,X):
    global graphics_timer
    if graphics_timer == None:
        graphics_timer = Timer(M['Q']['runtime_parameters']['graphics_timer_time'])
    if graphics_timer.check():
        M['load']()
        graphics_timer = Timer(M['Q']['runtime_parameters']['graphics_timer_time'])
    else:
        return

    figure('loss')
    """
    ab = N.extract('input',0)
    a = ab[0,0,0]
    b = ab[1,0,0]
    c = N.extract('output',0)[0,0,0]
    t = N.extract('target',0)[0,0,0]
    if True:
        diff = np.abs(dp(c)-dp(t))
        if diff < 0.2:
            color = '`wgb'
        else:
            color = '`wrb'
        clp( diff,color, dp(a),dp(b),dp(c),dp(t),'`' )
    """
    clf()
    plot(N.losses,'.')
    m = meo(na(N.losses),M['Q']['runtime_parameters']['meo_num'])
    plot(m)
    ylim(
        M['Q']['runtime_parameters']['graphics_ylim'][0],
        M['Q']['runtime_parameters']['graphics_ylim'][1]
    )


    c = N.extract('input')[:3,:,:]
    t = N.extract('target')[:3,:,:]
    d = N.extract('output')[:3,:,:]
    #mi(c[0,:,:])#,0,img_title=d2s(dp(t),dp(d)))
    mi(z55(c.transpose(2,1,0)),'input')
    mi(z55(d.transpose(2,1,0)),'output')
    mi(z55(t.transpose(2,1,0)),'target')
    #mi(d.transpose(2,1,0)[:,:,1],9)
    #figure('d');clf();plot(d.transpose(2,1,0)[10,:,1])
    #print shape(c)

    if False:
        d = N.extract('output')[3:6,:,:]
        mi(z55(d.transpose(2,1,0)),'output-1')
        d = N.extract('output')[6:9,:,:]
        mi(z55(d.transpose(2,1,0)),'output-2')

    if False:
        c = N.extract('input')[3:6,:,:]
        mi(z55(c.transpose(2,1,0)),'input-1')
        c = N.extract('input')[6:9,:,:]
        mi(z55(c.transpose(2,1,0)),'input-2')

    if False:
        ctr = 0
        for r in X['data_tracker'].keys():
            ctr += 1
            clp('\t',ctr,r,len(X['data_tracker'][r].keys()))
        print '\n'

    spause()


#EOF
