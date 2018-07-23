from kzpy3.utils2 import *

net_folder = pname(opjh(__file__))
utils_folder = opj(pname(pname(net_folder)),'utils','a')

pythonpaths([opjh('kzpy3'),net_folder,utils_folder])
exec(identify_file_str)

#EOF
