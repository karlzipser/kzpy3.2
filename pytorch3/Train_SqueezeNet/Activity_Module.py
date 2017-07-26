from Parameters_Module import *
exec(identify_file_str)
from vis2 import *
import torch
import torch.nn.utils as nnutils

#img_saver = Image_to_Folder_Saver({'path':opjD('cameras0')})

_ = dictionary_access


def Net_Activity(*args):
    Args = args_to_dictionary(args)
    D = {}
    True
    for k in Args[activiations].keys():
        D[k] = Args[activiations][k].data.cpu().numpy()
    return D

#EOF
