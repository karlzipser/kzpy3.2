from kzpy3.utils3 import *
exec(identify_file_str)



P = {}

P['ABORT'] = False

P['flex_weight_file_path'] = most_recent_file_in_folder(opjD('net_flex/weights'))

P['flex_network_output_sample'] = 0

flex_names = []
for fb in ['F']:
    for lr in ['L','C','R']:
        for i in [0,1,2,3]:
            flex_names.append(d2n(fb,lr,i))



