from kzpy3.utils import *
pythonpaths(['kzpy3','kzpy3/teg9'])

location = '/media/karlzipser/ExtraDrive4/bair_car_data_new_28April2017'  #"/media/karlzipser/ExtraDrive4" #opjD()
ignore_lst = []#['/media/karlzipser/ExtraDrive4/bair_car_data_new_28April2017/meta_bkp','/media/karlzipser/ExtraDrive4/meta','/media/karlzipser/ExtraDrive4/meta_bkp']
runs = {}
info = [['preprocessed_data*.pkl','preprocessed_data'],
    ['left_image_bound_to_data*.pkl','left_image_bound_to_data'],
    ['Bag_Folder*.pkl','Bag_Folder'],
    ['marker_data.pkl','marker_data'],
    ['trajectory.pkl','trajectory'],
    ['*.bag','bag'],
    ['*.bag.pkl','bag_pkl']]

for file_pattern,file_key in info:
    print(file_pattern,file_key)
    files = find_files_recursively(location,file_pattern)
    for p in files['paths'].keys():
        if str_contains_one(p,ignore_lst):
            continue
        r = fname(p)
        if r not in runs:
            runs[r] = {}
        if file_key not in runs[r]:
            runs[r][file_key] = []
        for f in files['paths'][p]:
            runs[r][file_key].append(opj(files['place'],p,f))

#    caffe2_z2_color_direct_local_01Jan13_00h01m07s_Mr_Yellow_A/Bag_Folder.pkl


locations = {}
for r in runs:
    for f in runs[r]:
        for q in runs[r][f]:
            L = opj(location,q.replace(location,'').split('/')[0])
            if L not in locations:
                locations[L] = 0
            locations[opj(location,q.replace(location,'').split('/')[0])] += len(runs[r][f])
pprint(locations)


marker_processing_necessary = []
ready_for_marker_processing = []
for r in sorted(runs.keys()):
    ns = []
    for file_pattern,file_key in info:
        n = 0
        if file_key in runs[r]:
            n = len(runs[r][file_key])
            #print(d2s('\t',file_key,len(runs[r][file_key])))
            #print runs[r][file_key]
        ns.append(n)
    c = 'white'
    for i in [0,1,2,3]:
        if ns[i] == 0:
            c = 'yellow'
            break
    cprint(d2n(ns,'\t',r),c)

pprint(marker_processing_necessary)
