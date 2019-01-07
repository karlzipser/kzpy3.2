#!/usr/bin/env python
from kzpy3.utils3 import *
exec(identify_file_str)

###############################################3
#
_ = {}
_['ABORT'] = False
_['load_timer_time'] = 2


_['start menu automatically'] = True

to_click = [
    'python kzpy3/VT_net2_/main.py run tegra-ubuntu_29Oct18_13h28m05s',
    "python kzpy3/Train_app/Sq40_initial_full_zeroing_and_projections/view_weights.py",
    "python kzpy3/Train_app/Sq40_initial_full_zeroing_and_projections_from_scratch/view_weights.py",
    "python kzpy3/Train_app/Sq40_initia_premetadata_zeroing/view_weights.py",
]

for c in to_click:
    _[c+'(click)'] = False

###############################################
_['customers'] = ['command_menu','M']
_['To Expose'] = {}
#


_['To Expose']['command_menu'] = sorted(_.keys())
_['a'] = 1;_['b'] = 2
_['To Expose']['M'] = 'a','b'
to_hide = ['To Expose','customers']
for h in to_hide:
	_['To Expose']['command_menu'].remove(h)



#EOF
