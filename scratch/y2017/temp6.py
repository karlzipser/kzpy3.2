from kzpy3.utils2 import *
pythonpaths(['kzpy3'])


for _name in ['src_directories','dst_directory']:
    exec(d2n(_name,'=',"'",_name,"'"))


def unify_directories_with_links(*args):
    keys = [src_directories,dst_directory]
    exec(dic_exec_str)
    if True:
    	unix('mkdir -p '+Args[dst_directory])
    	for d in Args[src_directories]:
    		paths = gg(opj(d,'*'))
    		for p in paths:
    			unix('ln -s '+p+' '+opj(Args[dst_directory],fname(p)),print_cmd=True)


unix('rm -r '+opjD('bdd_car_data_link_unified'))
unify_directories_with_links(
	src_directories,[opjD('bair_car_data_Main_Dataset/hdf5/segment_metadata'),opjD('bair_car_data_new_28April2017/hdf5/segment_metadata')],
	dst_directory,opjD('bdd_car_data_link_unified','hdf5','segment_metadata'))
unify_directories_with_links(
	src_directories,[opjD('bair_car_data_Main_Dataset/hdf5/runs'),opjD('bair_car_data_new_28April2017/hdf5/runs')],
	dst_directory,opjD('bdd_car_data_link_unified','hdf5','runs'))