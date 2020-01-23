from kzpy3.vis3 import *

if 'affinity' not in locals():
    affinity = lo(opjD('affinity'))
    affinity = 1 - affinity

if 'm' not in locals():
    m = zeros((32,32),int)

n = zeros((32,32))
ctr = 0
ctr_prev = 0
af = [0]
#indicies = range(1024)


for x in range(32):
    for y in range(32):
        m[x,y] = -1

np.random.shuffle(indicies)

ctr = 0
for x in range(32):
    for y in range(32):
        if ctr >= len(indicies):
            pass
        else:
            m[x,y] = indicies[ctr]
        ctr += 1
m_prev = m.copy()
#mi(m)

def switcher(x,y,a,b):
    while True:
        jx = np.random.randint(32)
        jy = np.random.randint(32)
        kx = np.random.randint(32)
        ky = np.random.randint(32)
        if m[jx,jy] < 0:
            continue
        if m[kx,ky] < 0:
            continue
        d1 = np.sqrt((x-jx)**2+(y-jy)**2)
        d2 = np.sqrt((x-kx)**2+(y-ky)**2)
        if min(d1,d2) > a:#2:
            continue
        if max(d1,d2) > b:#6:
            continue
        elif (jx != x or jy != y) and (kx != x or ky != y):
            break
        else:
            pass#cr((x,y),(jx,jy),(kx,ky))
    #cm((x,y),(jx,jy),(kx,ky))

    m0 = m[x,y]
    m1 = m[jx,jy]
    m2 = m[kx,ky]

    a1 = affinity[m0,m1]
    a2 = affinity[m0,m2]

    if True:#max(a1,a2) > 0.8:# or np.random.rand() > 0.95:

        #cm((m0,m1,m2),(a1,a2),(d1,d2),max(a1,a2),ra=0)
        if a1 > a2 and d1 > d2:# or (a2 > a1 and d2 > d1):
            m[jx,jy] = m2
            m[kx,ky] = m1
            n[jx,jy] = affinity[m0,m2]
            return 1
        elif a2 > a1 and d2 > d1:
            m[jx,jy] = m2
            m[kx,ky] = m1
            n[kx,ky] = affinity[m0,m1]
            return 1
        if a1 > a2:# or (a2 > a1 and d2 > d1):
            n[jx,jy] = affinity[m0,m1]
            return 0
        elif a2 > a1:
            n[kx,ky] = affinity[m0,m2]
            return 0
    return 0


def probe_affinity(m):
    ctr = 0.
    a = 0.
    for x in range(31):
        for y in range(31):
            m0 = m[x,y]
            if m0 < 0:
                continue
            m1 = m[x+1,y]
            a += affinity[m0,m1]
            ctr += 1.0
            m0 = m[x,y]
            m1 = m[x,y+1]
            a += affinity[m0,m1]
            ctr += 1.0
    return a / ctr


m_best = m.copy()
gtimer = Timer(1)
save_timer = Timer(60*10)
for i in range(10000000):#000):
    if False:#save_timer.check():
        save_timer.reset()
        so(opjD('m'),m)
    #if xytimer.check():
    #    xytimer.reset()
        #x,y = np.random.randint(32),np.random.randint(32)
    #    x = np.random.choice([6,32-6])
    #    y = np.random.choice([6,32-6])
    x,y = np.random.randint(32),np.random.randint(32)
    hz = Timer(1)
    run = Timer(1)
    #while not run.check():
    ctr += switcher(x,y,80,160)#16,16)#np.random.randint(32),np.random.randint(32))
    hz.freq()
    af.append(probe_affinity(m))
    #cg(af[-1],max(af))
    if af[-1] > 0.9999*max(af):
        m_best = m.copy()
        #cm(0)
    else:
        m = m_best.copy()
        #cm(1)
    """
    if af[-2] > af[-1]:
        aaa = m.copy()
        m = m_prev.copy()
        m_prev = aaa
    else:
        m_prev = m.copy()
    """
    """
    if probe_affinity(m) > probe_affinity(m_prev):
        pass
    else:
        m = m_prev.copy()
    """
    if gtimer.check():
        gtimer.reset()
        figure(2)
        clf()
        plot(af[1:],'r.')
        #mi(m,'B')
        #mi(n,'A')
        
        cg(ctr-ctr_prev,af[-1])
        ctr_prev = ctr
        t = []
        
        mm = m.flatten()
        ctr2 = 0
        for cluster in rlen(cluster_list):
            #s = []
            
            #z = np.zeros((23,41,3))
            #n = rlen(cluster_list[cluster])
            #if len(n) < 6:
            #    continue
            #random.shuffle(n) 292
            for i in [0]:#n:
                C = cluster_list[mm[cluster]][i]
                other_name = C['name']
                other_index = C['index']
                #other_img = Images[other_name][other_index].copy()
                traj_img = Files[other_name][other_index].copy()
                #z += traj_img
                #s.append(other_img)
                if ctr2 >= len(indicies):
                    traj_img *= 0
                t.append(traj_img)
                ctr2 += 1
            #s = na(s)
        t = na(t)
        #v = vis_square2(z55(s),10,127)
        w = vis_square2(z55(t),2,127)
        mi(w,'rgb');#mi(w,'traj');spause()

        spause()
        


#EOF
