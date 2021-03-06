from kzpy3.vis3 import *
exec(identify_file_str)


graphics_timer = None

def graphics(N,M):
    global graphics_timer
    if graphics_timer == None:
        graphics_timer = Timer(M['Q']['other_parameters']['graphics_timer_time'])
    if graphics_timer.check():
        M['load']()
        graphics_timer = Timer(M['Q']['other_parameters']['graphics_timer_time'])
    else:
        return

    figure('loss')
    ab = N.extract('camera_input',0)
    a = ab[0,0,0]
    b = ab[1,0,0]
    c = N.extract('final_output',0)[0]
    if False:
        print dp(a),dp(b),dp(c)

    clf()
    plot(N.losses,'.')
    m = meo(na(N.losses),M['Q']['other_parameters']['meo_num'])
    plot(m)
    ylim(
        M['Q']['other_parameters']['graphics_ylim'][0],
        M['Q']['other_parameters']['graphics_ylim'][1]
    )

    c = N.extract('camera_input')
    d = N.extract('final_output')#;kprint(d,title='d')
    for i in [0,3]:
        mi(c[i,:,:].transpose(),i,img_title=d2s(d))

    spause()




#EOF
