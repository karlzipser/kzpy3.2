#!/usr/bin/env python
"""
python kzpy3/Cars/n26Dec18/scripts/summarize_networks.py src ~/Desktop/ dst ~/Desktop/ print_only False
"""
from kzpy3.utils3 import *
exec(identify_file_str)
#Arguments['src'] = opjD()
#Arguments['dst'] = opjm('rosbags')
setup_Default_Arguments(
    {
        'src': opjD(),
        'dst' = opjm('rosbags'),
        'print_only': False,
    }
)
print_Arguments()
src = Arguments['src']
dst = Arguments['dst']
print_only = False

if 'print_only' in Arguments:
    print_only = Arguments['print_only']
    if print_only == 'False':
        print_only = False

net_folders = sggo(src,'Networks','*')
Nets = {}
for n in net_folders:
    if len(sggo(n,'weights')) == 1:
        weight_files = sort_dir_by_ctime(opj(n,'weights'))
        if len(weight_files) > 5:
            l=len(weight_files)
            l5=int(l/5)
            wrange = range(0,l,l5)
            wrange[-1] = l-1
            selected_weights_files = []
            for w in wrange:
                selected_weights_files.append(weight_files[w])
            Nets[fname(n)] = selected_weights_files

for n in Nets:
    ndst = opj(dst,'Network_Weights',n)
    os_str = d2s('mkdir -p',ndst)
    cg(os_str)
    if not print_only:
        cr('writing...')
        os.system(os_str)
    for w in Nets[n]:
        os_str = d2s("cp -p",w,opj(ndst,fname(w)))
        cb(os_str)
        if not print_only:
            cr('writing...')
            os.system(os_str)
if print_only:
    cr("print_only, no files written.")


