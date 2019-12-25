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
                Values[ky] = v
        ctr += 1
        if ctr > ctr_mx:
            break
    if save:
        so(opj(path,'Runs'),Runs)
        so(opj(path,'Values'),Values)

    return Runs,Values



def test(Runs,Values):
    Os = {}
    for r in Runs.keys():
        p = opjD('Data',Runs[r],r,'original_timestamp_data.h5py')
        Os[r] = h5r(p)

    img = zeros((94,168*2,3),np.uint8)

    keys = Values.keys()
    np.random.shuffle(keys)
    while True:
        ky = keys.pop()
        f0 = ky[0][0]
        f1 = ky[1][0]
        i0 = ky[0][1]
        i1 = ky[1][1]
        if ky[0] in too_many or ky[1] in too_many:
            continue
        if Values[ky] < 0.25:
            print ky,Values[ky]


            img[:,:168,:] = Os[f0]['left_image']['vals'][i0]
            img[:,168:,:] = Os[f1]['left_image']['vals'][i1]
            mi(img,img_title=d2s(Values[ky]))
            spause()
            if raw_input('hit enter or q > ') == 'q':
                break
    




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







if __name__ == '__main__':

    if Arguments['create']:

        create_Runs_and_Values_files(Arguments['path'])

    if Arguments['test']:
        Runs = lo(opj(Arguments['path'],'Runs'))
        Values = lo(opj(Arguments['path'],'Values'))
        test(Runs,Values)

#EOF
