#!/usr/bin/env python

############################################
"""
python kzpy3/scratch/Template/template.py autostart 1
"""
############################################


############################################
# setup and menu start
from kzpy3.utils3 import *
import kzpy3.scratch.Template.default_values as default_values
P = default_values.P
P['ABORT'] = False
try:
    if Arguments['autostart'] in [1,'y','Y','yes']:
        os.system(d2n("gnome-terminal -x python kzpy3/Menu_app/menu2.py path ","kzpy3/scratch/Template"," dic P"))
        # Leading '/' in path messes up menu2.py; until fixed, using opjk() won't work.
except:
    pass
#
############################################


######################################
# e.g. using Arguments
"""
Default_arguments = {
    'a':123,
    'b':'temp',
}
for d in Default_arguments:
    assert d in P
    if d not in Arguments:
        Arguments[d] = Default_arguments[d]
"""
try:
    param = Arguments['param']
except:
    param = 'default value'
#
######################################


def topic_warning(t):
    cr("\n\nWarning!!!!!!!\n",d2n("topic '",t,"'"),"in both Topics['To Expose'][] and in Arguments[]")
    #raw_enter()

############################################
# Transfer argments to P, but warn if in 'To Expose' list becuase these can be adjusted by
# menu which will overwrite command line values even if they are not set in the menu.
for a in Arguments:
    if a in P['To Expose']['template']:
       topic_warning(a) 
    P[a] = Arguments[a]
print_Arguments()
raw_enter()
#
############################################

duration_timer = Timer()
freq_timer = Timer(1)
waiting_timer = Timer(1)








if __name__ == '__main__':

    print 'main loop'
    
    import kzpy3.Menu_app.menu2 as menu2

    parameter_file_load_timer = Timer(0.5)

    while P['ABORT'] == False:

        try:
            time.sleep(1)

            if parameter_file_load_timer.check():
                Topics = menu2.load_Topics(opjk("scratch/Template"),first_load=False,customer='template')
            if type(Topics) == dict:
                for t in Topics['To Expose']['template']:
                    if t in Arguments:
                        topic_warning(t)
                    if '!' in t:
                        pass
                    else:
                        P[t] = Topics[t]
            parameter_file_load_timer.reset()
            cg("P['a']+P['c'][3] =",P['a']+P['c'][3])
        except Exception as e:
            CS_(d2s('Main loop exception',e))

    cg("P['ABORT'] =",P['ABORT'],"\nRun duration =",dp(duration_timer.time()),"seconds.\nDone.\n")

#EOF
