folders = sggo('/media/karlzipser/rosbags/Mr_Orange_30August2017/new/*')

ctr = 1
for f in folders:
    print f
    new_name = d2n('Mr_Orange_30August2017_',ctr)
    new_f = opj(pname(f),new_name)
    print new_f
    ctr += 1
    unix(d2s('mv',f,new_f))