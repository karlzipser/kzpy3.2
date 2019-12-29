from kzpy3.vis3 import *
import Menu.main
exec(identify_file_str)

########################################
########################################
###
M = Menu.main.start_Dic(
    dic_project_path=pname(opjh(__file__)), 
    Arguments={'menu':False,'read_only':True}
)
M['load']()
###
########################################
########################################


graphics_timer = Timer(M['Q']['other_parameters']['graphics_timer_time'])

def graphics(N):
    global graphics_timer
    if graphics_timer.check():
        
        M['load']()
        
        graphics_timer = Timer(M['Q']['other_parameters']['graphics_timer_time'])#M['Q']['other_parameters']['graphics_timer_time']

    else:
        return

    figure('loss')
    ab = N.extract('camera_input',0)
    a = ab[0,0,0]
    b = ab[1,0,0]
    c = N.extract('final_output',0)[0]
    print dp(a),dp(b),dp(c)

    clf()
    plot(N.losses,'.')
    m = meo(na(N.losses),33)
    plot(m)
    ylim(0,1.)
    spause()




#EOF
