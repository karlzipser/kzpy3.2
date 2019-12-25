from kzpy3.vis3 import *

if 'affinity' not in locals():
    affinity = lo(opjD('affinity'))
    affinity = 1 - affinity

m = zeros((32,32),int)
n = zeros((32,32))

indicies = range(1024)

np.random.shuffle(indicies)

ctr = 0
for x in range(32):
    for y in range(32):
        m[x,y] = indicies[ctr]
        ctr += 1

mi(m)

def switcher(x,y):
    while True:
        """
        jx = x+np.random.randint(16)-8
        jy = y+np.random.randint(16)-8
        kx = x+np.random.randint(16)-8
        ky = y+np.random.randint(16)-8
        if jx < 0:
            jx = 0
        if jy < 0:
            jy = 0
        if kx < 0:
            kx = 0
        if ky < 0:
            ky = 0
        if jx >= 32:
            jx = 31
        if jy >= 32:
            jy = 31
        if kx >= 32:
            kx = 31
        if ky >= 32:
            ky = 31
        """
        jx = np.random.randint(32)
        jy = np.random.randint(32)
        kx = np.random.randint(32)
        ky = np.random.randint(32)
        if (jx != x or jy != y) and (kx != x or ky != y):
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
        d1 = np.sqrt((x-jx)**2+(y-jy)**2)
        d2 = np.sqrt((x-kx)**2+(y-ky)**2)
        if min(d1,d2) > 166:
            return 0
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


def probe_affinity():
    ctr = 0.
    a = 0.
    for x in range(31):
        for y in range(31):
            m0 = m[x,y]
            m1 = m[x+1,y]
            a += affinity[m0,m1]
            ctr += 1.0
            m0 = m[x,y]
            m1 = m[x,y+1]
            a += affinity[m0,m1]
            ctr += 1.0
    return a / ctr

ctr = 0
ctr_prev = 0
af = []
gtimer = Timer(1)
xytimer = Timer(130.00005)
for u in range(1000000):
    x,y = np.random.randint(32),np.random.randint(32)
    for i in range(1000000):#000):
        if xytimer.check():
            xytimer.reset()
            #x,y = np.random.randint(32),np.random.randint(32)
            x = np.random.choice([6,32-6])
            y = np.random.choice([6,32-6])
        #x,y = np.random.randint(32),np.random.randint(32)
        hz = Timer(1)
        run = Timer(1)
        #while not run.check():
        ctr += switcher(x,y)#16,16)#np.random.randint(32),np.random.randint(32))
        hz.freq()
        af.append(probe_affinity())
        if gtimer.check():
            gtimer.reset()
            figure(2)
            clf()
            plot(af,'r.')
            mi(m,'B')
            mi(n,'A')
            
            cg(ctr-ctr_prev,af[-1])
            ctr_prev = ctr
            t = []
            
            mm = m.flatten()
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
                    t.append(traj_img)
                #s = na(s)
            t = na(t)
            #v = vis_square2(z55(s),10,127)
            w = vis_square2(z55(t),10,127)
            mi(w,'rgb');#mi(w,'traj');spause()

            spause()
            


"""

def adfs(id,nearest,B):
    for n in nearest:
        
        vx = B[id]['x']-B[n]['x']
        vy = B[id]['y']-B[n]['y']
        d = np.sqrt(vx**2 + vy**2)
"""
