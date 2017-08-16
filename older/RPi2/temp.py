"""
RPi_sessions_path = opjh('Desktop/RPi_data')
sessions_dic,_ = dir_as_dic_and_list(RPi_sessions_path)
for k in sessions_dic:
    sessions_dic[k] = {}
    _,jpg_lst = dir_as_dic_and_list(opj(RPi_sessions_path,k,'jpg'))
    sessions_dic[k]['name_list'] = jpg_lst
    sessions_dic[k]['name_dic'] = {}
    for f in sessions_dic[k]['name_list']:
        sessions_dic[k]['name_dic'][f] = {}
    for d in reversed(
        txt_file_to_list_of_strings(opj(RPi_sessions_path,k,'session_list-'+k+'.txt'))):
        f = d.split(' ')[0]
        c = d.split(' ')[-4:]
        if f in sessions_dic[k]['name_dic']:
            for i in range(len(c)):
                c[i] = int(c[i])
            sessions_dic[k]['name_dic'][f]['cmd'] = c
            sessions_dic[k]['name_dic'][f]['img'] = opj(RPi_sessions_path,k,'jpg',f)

def rnd_img_name(sessions_dic):
    ses = sessions_dic.keys()
    lses = len(ses)
    k = ses[np.random.randint(lses)]
    lnm = len(sessions_dic[k]['name_list'])
    i = np.random.randint(lnm)
    f = sessions_dic[k]['name_list'][i]
    return (k,i,f)


k,i,f=rnd_img_name(sessions_dic)

print sessions_dic[k]['name_dic'][f]['cmd']
print sessions_dic[k]['name_dic'][f]['img']
"""









def get_sessions_dic(RPi_sessions_path):
    sessions_dic,_ = dir_as_dic_and_list(RPi_sessions_path)
    for k in sessions_dic:
        sessions_dic[k] = {}
        _,jpg_lst = dir_as_dic_and_list(opj(RPi_sessions_path,k,'jpg'))
        sessions_dic[k]['name_list'] = jpg_lst
        sessions_dic[k]['name_dic'] = {}
        for f in sessions_dic[k]['name_list']:
            sessions_dic[k]['name_dic'][f] = {}
        for d in reversed(
            txt_file_to_list_of_strings(opj(RPi_sessions_path,k,'session_list-'+k+'.txt'))):
            f = d.split(' ')[0]
            c = d.split(' ')[-4:]
            if f in sessions_dic[k]['name_dic']:
                for i in range(len(c)):
                    c[i] = int(c[i])
                sessions_dic[k]['name_dic'][f]['cmd'] = c
                sessions_dic[k]['name_dic'][f]['img'] = opj(RPi_sessions_path,k,'jpg',f)
    return sessions_dic
def rnd_img_name(sessions_dic):
    ses = sessions_dic.keys()
    lses = len(ses)
    k = ses[np.random.randint(lses)]
    lnm = len(sessions_dic[k]['name_list'])
    i = np.random.randint(lnm)
    f = sessions_dic[k]['name_list'][i]
    return (k,i,f)
def get_img_lst_and_target_lst(sessions_dic):
    success = False
    while success == False:
        try:
            success = True
            k,i,f = rnd_img_name(sessions_dic)
            rng = range(i,i+20)
            flst = []
            clst = []
            for j in rng:
                f = sessions_dic[k]['name_list'][j]
                c = sessions_dic[k]['name_dic'][f]['cmd']
                if c[0] < 1:
                    success = False
                    print 'Failed!!!'
                    break
                else:
                    flst.append(f)
                    clst.append(c)
            if success:
                print 'success'
                for q in zip(flst,clst):
                    print q
                img_lst = []
                for f in flst[:9]:
                    if type(sessions_dic[k]['name_dic'][f]['img']) == str:
                        img = imread(sessions_dic[k]['name_dic'][f]['img'])
                        sessions_dic[k]['name_dic'][f]['img'] = img
                    img_lst.append(sessions_dic[k]['name_dic'][f]['img'])    
        except:
            success = False
    target_lst = []
    for c in clst:
        target_lst.append((c[3]/10.0 - 7.2) / (11.7-7.2))
    return img_lst,target_lst

sessions_dic = get_sessions_dic(opjh('Desktop/RPi_data'))
img_lst,target_lst = get_img_lst_and_target_lst(sessions_dic)
for t in target_lst:
    print t
for img in img_lst:
    plt.clf()
    mi(img[:,:,1])
    plt.ion()
    plt.show()
    plt.pause(0.2)

