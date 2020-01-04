from kzpy3.vis3 import *
exec(identify_file_str)


graphics_timer = None

def graphics_function(N,M):
    global graphics_timer
    if graphics_timer == None:
        graphics_timer = Timer(M['Q']['runtime_parameters']['graphics_timer_time'])
    if graphics_timer.check():
        M['load']()
        graphics_timer = Timer(M['Q']['runtime_parameters']['graphics_timer_time'])
    else:
        return

    figure('loss')
    ab = N.extract('input',0)
    a = ab[0,0,0]
    b = ab[1,0,0]
    c = N.extract('output',0)[0]
    if False:
        print dp(a),dp(b),dp(c)

    clf()
    plot(N.losses,'.')
    m = meo(na(N.losses),M['Q']['runtime_parameters']['meo_num'])
    plot(m)
    ylim(
        M['Q']['runtime_parameters']['graphics_ylim'][0],
        M['Q']['runtime_parameters']['graphics_ylim'][1]
    )

    c = N.extract('input')
    t = N.extract('target_torch')
    d = N.extract('output')#;kprint(d,title='d')
    #for i in [0,3]:
    #    mi(c[i,:,:].transpose(),i,img_title=d2s(dp(t),dp(d)))
    mi(c[0,:,:].transpose(),0,img_title=d2s(dp(t),dp(d)))
    mi(c[3,:,:].transpose(),3)

    spause()


#EOF
