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
    D[activiations] = {}
    D[imgs] = {}

    for k in Args[activiations].keys():
        D[activiations][k] = Args[activiations][k].data.cpu().numpy()
        D[imgs][k] = {}
        for moment_indexv in range(shape(D[activiations][k])[0]):
            try:
                D[imgs][k][moment_indexv] = vis_square(D[activiations][k][moment_indexv],padval=0.5)
            except Exception as e:
                    print("********** Exception ***********************")
                    print(e.message, e.args)
                    print k
    def _function_view(*args):
        Args = args_to_dictionary(args)
        True
        for k in D[imgs].keys():
            try:
                mi(D[imgs][k][Args[moment_index]],k); pause(0.00001)
            except Exception as e:
                    print("********** Exception ***********************")
                    print(e.message, e.args)
                    print k
    D[view] = _function_view
#                


    return D





#EOF
