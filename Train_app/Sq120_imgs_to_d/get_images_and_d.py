from kzpy3.vis3 import *

setup_Default_Arguments(
    {
        'path':opjD(),
        'create':0,
        'test':0,
    }
)

kprint(Arguments)


def create_Runs_and_Values_files(path,ctr_mx=100000000,save=True):
    files = sggo(opjD('Interval_data/*.pkl'))

    Runs = {}
    Values = {}

    ctr = 0
    

    for x in rlen(files):
        kprint(x,title='file number')
        I = lo(files[x])
        for n in I.keys():
            Values[n] = {}
            for i in I[n]:
                f0 = i[0][0]
                f1 = i[1][0]
                i0 = i[0][1]
                i1 = i[1][1]
                v = i[2]
                for j in [0,1]:
                    f = i[j][0]
                    if f not in Runs:
                        H = find_files_recursively(opjD('Data'),f,DIRS_ONLY=True)
                        Runs[f] = H['paths'].keys()[0]
                srt = sorted([f0,f1])
                if srt[0] == f0:
                    ky = ((f0,i0),(f1,i1))
                else:
                    ky = ((f1,i1),(f0,i0))
                Values[n][ky] = v
        ctr += 1
        if ctr > ctr_mx:
            break
    if save:
        so(opj(path,'Runs'),Runs)
        so(opj(path,'Values'),Values)

    return Runs,Values

#,a
def create_Runs_and_Values_files2(path,ctr_mx=100000000,save=True):
    files = sggo(opjD('Interval_data/*.pkl'))

    Runs = {}
    Values = {}

    ctr = 0
    
    Es = {}


    r = range(len(files))
    np.random.shuffle(r)
    print r
    for x in r:#range(len(files):
        total,reject = 0,0
        kprint(x,title='file number')
        I = lo(files[x])
        for n in I.keys():
            if n not in Values:
                Values[n] = {}
            for i in I[n]:
                f0 = i[0][0]
                f1 = i[1][0]
                i0 = i[0][1]
                i1 = i[1][1]
                v = i[2]
                do_reject = False
                for j in [0,1]:
                    f = i[j][0]
                    if f not in Runs:
                        H = find_files_recursively(opjD('Data'),f,DIRS_ONLY=True)
                        Runs[f] = H['paths'].keys()[0]
                        #print Runs[f]
                        #print f
                        #print H
                        L = h5r(opjD('Data',Runs[f],f,'left_timestamp_metadata_right_ts.h5py'))
                        Es[f] = L['encoder'][:]
                        #Es[f][:int(rnd()*len(Es[f]))] *= 0
                        L.close()
                        #clf();plot(Es[f]);plt.title(f);spause();raw_enter()
                    
                    #cy(f,i[j][1])
                    if Es[f][i[j][1]] < 0.1:
                        do_reject = True
                total += 1
                if do_reject:
                    reject += 1
                else:
                    srt = sorted([f0,f1])
                    if srt[0] == f0:
                        ky = ((f0,i0),(f1,i1))
                    else:
                        ky = ((f1,i1),(f0,i0))
                    Values[n][ky] = v

        clp(files[x],total,reject,int(100*reject/(1.*total)),'%')#;raw_enter()
        ctr += 1
        if ctr > ctr_mx:
            break
    if save:
        so(opj(path,'Runs'),Runs)
        so(opj(path,'Values'),Values)

    return Runs,Values
#,b



def test(Runs,Values,category_number):
    Os = {}
    for r in Runs.keys():
        p = opjD('Data',Runs[r],r,'original_timestamp_data.h5py')
        Os[r] = h5r(p)

    img = zeros((94,168*2,3),np.uint8)

    Keys = {}
    for n in Values.keys():
        Keys[n] = Values[n].keys()
        np.random.shuffle(Keys[n])

    value_keys = Values.keys()
    n = category_number
    while True:
        np.random.shuffle(value_keys)
        #for n in value_keys:
        ky = Keys[n][randint(len(Keys[n]))]
        f0 = ky[0][0]
        f1 = ky[1][0]
        i0 = ky[0][1]
        i1 = ky[1][1]
        img[:,:168,:] = Os[f0]['left_image']['vals'][i0]
        img[:,168:,:] = Os[f1]['left_image']['vals'][i1]
        mi(img,img_title=d2s(n,'     ',Values[n][ky]))
        spause()
        if raw_input('hit enter or q > ') == 'q':
            break



def Images_and_Value_Getter(Runs,Values):
    D = {}
    Os = {}
    for r in Runs.keys():
        p = opjD('Data',Runs[r],r,'original_timestamp_data.h5py')
        Os[r] = h5r(p)

    img = zeros((94,168*2,3),np.uint8)

    Keys = {}
    for n in Values.keys():
        Keys[n] = Values[n].keys()
        np.random.shuffle(Keys[n])

    def function_get():
        FLIP = random.choice([0,1])
        n = np.random.choice(Values.keys())
        ky = Keys[n][randint(len(Keys[n]))]
        f0 = ky[0][0]
        f1 = ky[1][0]
        i0 = ky[0][1]
        i1 = ky[1][1]
        ref_img = Os[f0]['left_image']['vals'][i0]
        other_img = Os[f1]['left_image']['vals'][i1]
        return ref_img,other_img,n,Values[n][ky]

    D['get'] = function_get

    return D


if False:
    IVG = Images_and_Value_Getter(Runs,Values)
    img = zeros((94,168*2,3),np.uint8)
    while True:
        r,o,n,v = IVG['get']()
        img[:,:168,:] = r
        img[:,168:,:] = o
        mi(img,img_title=d2s(n,'     ',v))
        spause()
        if raw_input('hit enter or q > ') == 'q':
            break





if False:
    l = 1000000
    a = range(l)
    t = Timer(5)
    ctr = 0
    while not t.check():
        b = a[randint(l)]#np.random.choice(a)
        ctr += 1
    print ctr

    Counts = {}
    too_many = []
    limit = 10
    for v in Values:
        for i in [0,1]:
            r = v[i]
            if r not in Counts:
                Counts[r] = 0
            Counts[r] += 1
            if Counts[r] > limit:
                too_many.append(r)
    too_many = list(set(too_many))

    Counts = {}
    too_many = []
    limit = 10
    for v in Values:
        for i in [0,1]:
            r = v[i]
            if r not in Counts:
                Counts[r] = 0
            Counts[r] += 1
            if Counts[r] > limit:
                too_many.append(r)
    too_many = list(set(too_many))





if False:#__name__ == '__main__':

    if Arguments['create']:

        create_Runs_and_Values_files(Arguments['path'])

    if Arguments['test']:
        Runs = lo(opj(Arguments['path'],'Runs'))
        Values = lo(opj(Arguments['path'],'Values'))
        test(Runs,Values)

#EOF
