pfrom kzpy3.vis3 import *

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



def test(Runs,Values):
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
    while True:
        np.random.shuffle(value_keys)
        for n in value_keys:
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

#,a
def copy_to_latest(folder_path,require=''):
    latest = most_recent_file_in_folder(folder_path)
    cr(latest)
    if require not in latest:
        return False
    os.system(d2s('rm',opj(folder_path,'latest')))
    sys_str = d2s('cp',latest,opj(folder_path,'latest'))
    os.system(sys_str)
    clp(sys_str,'`--r')
    return True

#,b


def copy_to_latest2(networks):
    os.system(d2s('rm -r',opjD('LATEST')))
    for network in networks:
        LATEST = opjD('LATEST',network)#.'+time_str())
        os.system(d2s('mkdir -p',LATEST))
        print LATEST
        for q in ['weights','loss']:
            latest = most_recent_file_in_folder(opjD('Networks',network,q))
            sys_str = d2s('cp',latest,opj(LATEST))
            clp(sys_str,'`--r')
            os.system(sys_str)

    

net =  'Sq3'#'Sq7_ConDecon_test2.84X47'
for f in ['weights','loss']:
    fp = opjD('Networks',net,f)
    print fp
    copy_to_latest(fp)

scp -r -P 1022 karlzipser@bdd3.neuro.berkeley.edu:'Desktop/Networks/Sq3/weights/latest' Desktop/latest.weights

if False:#__name__ == '__main__':

    if Arguments['create']:

        create_Runs_and_Values_files(Arguments['path'])

    if Arguments['test']:
        Runs = lo(opj(Arguments['path'],'Runs'))
        Values = lo(opj(Arguments['path'],'Values'))
        test(Runs,Values)




scp -P 1022 karlzipser@bdd3.neuro.berkeley.edu:'Desktop/Networks/Sq7_ConDecon_test2.84x47/weights/net_06Jan20_17h03m17s.cuda.infer' Desktop/LATEST/Sq7_ConDecon_test2.84X47

scp -P 1022 karlzipser@bdd3.neuro.berkeley.edu:'Desktop/Networks/Sq7_ConDecon_test2.84x47/loss/net_06Jan20_17h08m18s.cuda.loss_avg.pkl'  Desktop/LATEST/Sq7_ConDecon_test2.84X47




scp -P 1022 karlzipser@bdd3.neuro.berkeley.edu:'Desktop/Networks/Sq3/loss/net_06Jan20_17h12m26s.cuda.loss_avg.pkl'  Desktop/LATEST/Sq3
scp -P 1022 karlzipser@bdd3.neuro.berkeley.edu:'Desktop/Networks/Sq3/weights/net_06Jan20_17h12m26s.cuda.infer'  Desktop/LATEST/Sq3

scp -P 1022 -r karlzipser@bdd3.neuro.berkeley.edu:'Desktop/LATEST'  Desktop

cp Desktop/LATEST/Sq3/*.infer Desktop/Networks/Sq3/weights




data = find_files_recursively(opjk(),'defaults.py',FILES_ONLY=True,ignore_underscore=True) 


l Sq7 --NET_TYPE abc



H = find_files_recursively(opjk(),'main.py',FILES_ONLY=True,ignore_underscore=True)
lst = []
for p in H['paths']:
    lst.append(d2n("alias ",p.split('/')[-1],"='python ",opj('~/kzpy3',p,"main.py'")))
list_of_strings_to_txt_file(opjk('misc/auto_aliases'),lst)    






def h(D,*args)


def d2s_spacer(args,spacer=' '):
    lst = []
    for e in args:
        lst.append(str(e))
    return spacer.join(lst)

def d2s_spacer(args,spacer=' '):
    lst = []
    for e in args:
        lst.append(str(e))
    return spacer.join(lst)
def d2s(*args):
    '''
    e.g.,
    
    d2s('I','like',1,'or',[2,3,4])
    
    yields
    
    'I like 1 or [2, 3, 4]'
    
    d2c(1,2,3) => '1,2,3'
    d2f('/',1,2,3) => '1/2/3'
    '''
    return d2s_spacer(args)



def c(D,*args,**kwargs):
    #print type(D),D
    assert type(D) == dict
    assert len(args) > 0
    a = args[0]
    #print a
    
    if a not in D:
        clp('warning, adding',a,'to dic','`--r')
        D[a] = {}

    if len(args) == 1:
        if 'eq' in kwargs:
            D[a] = kwargs['eq']
        return D[a]
    else:
        assert len(args) > 1
        if 'eq' in kwargs:
            return h(D[a],*args[1:],eq=kwargs['eq'])
        else:
            return h(D[a],*args[1:])



#EOF
