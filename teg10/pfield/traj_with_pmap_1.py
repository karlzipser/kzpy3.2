from kzpy3.utils import *
pythonpaths(['kzpy3','kzpy3/teg9'])

from vis import *
import math

from data.markers_clockwise import markers_clockwise

Origin = int(1000/300.*300)
Mult = 1000/300.*50

pfield = zeros((2*Origin,2*Origin))
marker_ids_all = []
marker_angles_dic = {}
marker_angles = 2*np.pi*np.arange(len(markers_clockwise))/(1.0*len(markers_clockwise))
marker_xys = {}
for r in [4.0,4.2,4.4]:
    marker_xys[r] = []
    for i in range(len(markers_clockwise)):
        a = marker_angles[i]
        marker_angles_dic[markers_clockwise[i]] = a
        x = r*107/100.*np.sin(a)
        y = r*107/100.*np.cos(a)
        marker_xys[r].append([x,y])




def meters_to_pixels(x,y):
    return (int(-Mult*x)+Origin),(int(Mult*y)+Origin)


markers_xy_dic = {}


pfield *= 0
gm = makeGaussian(3*Mult,1*Mult)
gc = makeGaussian(6*Mult,1.6*Mult)
gs = makeGaussian(0.8*Mult,0.24*Mult)
gcar = makeGaussian(4*Mult,4/3.*Mult)
for j in range(len(markers_clockwise)):
    m = markers_clockwise[j]
    xy = marker_xys[4.0][j]
    markers_xy_dic[m] = xy
    xp,yp = meters_to_pixels(xy[0],xy[1])
    iadd(gm,pfield,(xp,yp))
    iadd(5*gs,pfield,(xp,yp))

    #iadd(5*gs,pfield,(xp,yp))
for j in range(len(markers_clockwise)):
    m = markers_clockwise[j]
    xy = marker_xys[4.0][j]
    markers_xy_dic[m] = xy
    xp,yp = meters_to_pixels(0.75*xy[0],0.75*xy[1])
    isub(gm,pfield,(xp,yp))
iadd(4*gc,pfield,(Origin,Origin))


pfield -= pfield.min()
pfield /= pfield.max()




mi(pfield,'pfield')
figure(3);plot(pfield[:,Origin])
PFIELD = pfield.copy()






N = lo(opjD('N.pkl'))
traj = N['Mr_Black']['direct_rewrite_test_28Apr17_17h23m15s_Mr_Black']['self_trajectory']















Pts = zeros( (len(traj['left']['x']),2) )
Pts[:,0] = traj['left']['x']
Pts[:,1] = traj['left']['y']

pts = Pts.copy()

def get_sample_points(pts,angles,n=3):

    sample_points = []
    potential_values = []

    heading = normalized_vector_from_pts(pts[-n:,:])
    heading *= 0.5 # 50 cm, about the length of the car
    if pts[-n,0] > pts[-1,0]:
        heading *= -1
    #if pts[-3,1] > pts[-1,1]:
    #    heading *= -1

    for a in angles:

        sample_points.append( rotatePoint([0,0],heading,a) )
    #figure(3)
    #pts_plot(pts)
    for k in range(len(sample_points)):
        f = sample_points[k]
        #plot([pts[-1,0],pts[-1,0]+f[0]],[pts[-1,1],pts[-1,1]+f[1]])
    #figure(1)
    for sp in sample_points:
        pix = meters_to_pixels(sp[0]+pts[-1,0],sp[1]+pts[-1,1])
        #plot(pix[0],pix[1],'kx')
        potential_values.append(pfield[pix[0],pix[1]])

    return sample_points,potential_values







def interpret_potential_values(potential_values):
    min_potential_index = potential_values.index(min(potential_values))
    max_potential_index = potential_values.index(max(potential_values))
    middle_index = int(len(potential_values)/2)

    d = 99.0/(1.0*len(potential_values)-1)
    steer_angles = np.floor(99-arange(0,100,d))
    dp = potential_values[max_potential_index] - potential_values[min_potential_index]
    
    p = min(1,dp/max( (0.6-max(0,potential_values[max_potential_index]-0.8)) ,0.2) )
    steer = int((p*steer_angles[min_potential_index]+(1-p)*49.0))
    return steer







angles = range(-30,31,10)
#angles = -1*array(angles)
pix_prev = [Origin,Origin]
mi(pfield,1)
xylim(-4,4,-4,4)
figure(2)
clf()
#xylim(0,7,1.5,1.57)
ctr = 0
for i in range(5000,len(pts),3):
    if traj['left']['t_vel'][i] > 0.4:
        pt = pts[i]
        pix = meters_to_pixels(pt[0],pt[1])
        sample_points,potential_values = get_sample_points(pts[i:i+6],angles,6)
        sp = sample_points[0]
        sp_pix = meters_to_pixels(sp[0]+pt[0],sp[1]+pt[1])
        if ctr ==0 or ctr > 3:
            figure(1)
            mi(pfield,img_title=d2s(i))
            if ctr > 0:
                isub(gcar,pfield,(pix_prev[1],pix_prev[0]))
            iadd(gcar,pfield,(pix[1],pix[0]))
            pix_prev = array(pix).copy()
            figure(2)
            clf()
            xylim(-0.1,6.1,-0.1,1.1)
            ctr = 0
        figure(1)
        plot(pix[1],pix[0],'r.')
        plot(sp_pix[1],sp_pix[0],'g.')
        figure(2)
        plot(potential_values,'r.-')
        title(interpret_potential_values(potential_values))

        ctr += 1
        
        pause(0.1)
        raw_input("dafds")#pause(0.03)

