from kzpy3.utils.common import *

def using_platform():
    from sys import platform
    if platform == "linux" or platform == "linux2":
        return 'linux'
    elif platform == "darwin":
        return 'osx'
    else:
        spd2s('unknown system (not linux or osx)')
        assert False
def using_linux():
    if using_platform() == 'linux':
        return True
    return False
def using_osx():
    if using_platform() == 'osx':
        return True
    return False

if using_osx():
    pass #CS_('using OS X')
elif using_linux():
    pass #CS_('using linux')
else:
    print('using UNKNOWN system')

try:
    import rospy
    HAVE_ROS = True
    #CS_('HAVE_ROS = True')
except:
    HAVE_ROS = False
    #CS_('HAVE_ROS = False')

try:
    #cs('username =',username)
    if username == 'nvidia':
        HAVE_GPU = True
        #CS_('HAVE_GPU = True')
    else:
        unix('nvidia-smi',print_stdout=True)
        HAVE_GPU = True
        cr('*** warning, check HAVE_GPU ***',ra=1)
        #CS_('HAVE_GPU = True')
except:
    HAVE_GPU = False
    #CS_('HAVE_GPU = False')


#exec(identify_file_str)

#EOF