###start
from kzpy3.vis3 import *
"""
https://stackoverflow.com/questions/76134/how-do-i-reverse-project-2d-points-into-3d
http://pyopengl.sourceforge.net/documentation/installation.html
"""

try:
    print len(encoders)
except:
    cs("Loading L and O...")
    L = h5r(opjD("model_car_data_July2018_lrc/locations/local/left_right_center/h5py/Mr_Black_25Jul18_19h55m13s/left_timestamp_metadata_right_ts.h5py"))
    O = h5r(opjD("model_car_data_July2018_lrc/locations/local/left_right_center/h5py/Mr_Black_25Jul18_19h55m13s/original_timestamp_data.h5py"))
    headings = L['gyro_heading_x'][:]
    encoders = L['encoder'][:]






def angle_between(v1, v2):
    """http://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python
    Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))



def rotatePoint(centerPoint,point,angle):
    """http://stackoverflow.com/questions/20023209/function-for-rotating-2d-objects
    Rotates a point around another centerPoint. Angle is in degrees.
    Rotation is counter-clockwise"""
    angle = math.radians(angle)
    temp_point = point[0]-centerPoint[0] , point[1]-centerPoint[1]
    temp_point = ( temp_point[0]*math.cos(angle)-temp_point[1]*math.sin(angle) , temp_point[0]*math.sin(angle)+temp_point[1]*math.cos(angle))
    temp_point = temp_point[0]+centerPoint[0] , temp_point[1]+centerPoint[1]
    return temp_point



def rotatePolygon(polygon,theta):
    """http://stackoverflow.com/questions/20023209/function-for-rotating-2d-objects
    Rotates the given polygon which consists of corners represented as (x,y),
    around the ORIGIN, clock-wise, theta degrees"""
    theta = math.radians(theta)
    rotatedPolygon = []
    for corner in polygon :
        rotatedPolygon.append(( corner[0]*math.cos(theta)-corner[1]*math.sin(theta) , corner[0]*math.sin(theta)+corner[1]*math.cos(theta)) )
    return rotatedPolygon



def vec(heading,encoder):
	velocity = encoder/2.3 # rough guess
	a = [0,1]
	a = array(rotatePoint([0,0],a,heading))
	a *= velocity/30.0
	return array(a)




figure(99)
clf()
plt_square()
l = 4
xylim(-l,l,-l,l)
xy = array([0.0,0.0])
xys=[]
CA()

hz_timer = Timer(1)

if True:
    for i in range(10300,len(headings),1):
        heading = headings[i]
        encoder = encoders[i]
        v = vec(heading,encoder)
        xy += v
        xys.append(array(xy))
        if np.mod(i,10):
            graphics = True
        else:
            graphics = False
        if len(xys) > 90+30:
            first_time = True
            for j in range(-(90+30),-1,1):
                xl = xys[j][0];yl = xys[j][1]
                if first_time:
                    img_index = j
                    if graphics:
                        figure(99)
                        clf()
                        xylim(-l+xl,l+xl,-l+yl,l+yl)
                        plt_square()
                        first_time = False
                if j >= -90:
                    c = 'b'
                else:
                    c = 'r'
                plot(xl,yl,c+'.')
                
            if graphics:
                mci(O['left_image']['vals'][i-90],scale=2,delay=1)#,'left camera')
                spause()
            hz_timer.freq()

            """
            theta_ = angle_clockwise((0,1), (R[aruco_heading_x][vals][-1],R[aruco_heading_y][vals][-1]))
            xy_ = na([x_,y_])
            pts_pov_ = na(rotatePolygon(pts_-xy_,theta_))
            """

"""
use:

    grep -lr rotate * | xargs grep -lr heading

check out:

    ~/_kzpy3_older/kzpy_8Sept2018/Localization_app/localizer_listener.py

https://stackoverflow.com/questions/973473/getting-a-list-of-all-subdirectories-in-the-current-directory
"""


bags = sggo('/media/karlzipser/rosbags/new/Mr_Blue_Back_24Sep18_21h38m22s/*.too_small')
for b in bags:
    os.system(d2s("mv",b,b.replace('.too_small','')))



O=h5r('/media/karlzipser/rosbags/h5py/Mr_Blue_Back_24Sep18_21h17m55s/original_timestamp_data.h5py')
L=h5r('/media/karlzipser/rosbags/h5py/Mr_Blue_Back_24Sep18_21h17m55s/left_timestamp_metadata_right_ts.h5py')
fc0=L['FC0'][:]

###stop












offset = 750
a = na(range(offset,1024)+range(0,offset))

y = (a/1024.*6290).astype(int)

indicies = [Y[v] for v in y]

a_shift = zeros(1024)
a_shift[indicies] = a
plot(a,'.');plot(a_shift,'.')



CA()

# q=p.flatten('F')

offset = 200

p=zeros((64,1024))

p[:,:] = [range(offset,1024)+range(0,offset)]

b = p[0:64:4,:]

c.reshape(16,1024)

y = (a[8,:]/1024.*6290).astype(int)

figure(1);plot(y,'g')

indicies = [Y[v] for v in y]

a_shift = zeros((64,1024))

a_shift[:,indicies] = a

mi(a,'a')
mi(a_shift,'a_shift')













def advance(lst,e,min_len=1):


lst=[1,2,3,4,3,5,6]
e='a'

min_len=3
len_lst = len(lst)
print len_lst
if len_lst < min_len:
    print 1
    pass
elif len_lst > 1.2*min_len:
    print 2
    lst = lst[-min_len:]
    print len(lst)
else:
    print 3
    lst.pop(0)
    print len(lst)
lst.append(e)
print 4


def advance(lst,e,min_len=1):
    lst.append(e)
    if len(lst)>1.2*min_len:
        lst = lst[-min_len:]

n = 3000
img = D['real'][n][:]
img[28,:] = img[27,:]
img[29,:] = img[30,:]
mn,mx = -0.5,0.7
img = np.log10(img+0.001)
img[img>mx] = mx
img[img<mn] = mn
img = cv2.resize(img,(256,94))
a1 = 128-168/2
a2 = 128+168/2
img = img[:,a1:a2]
if 'temporary (?)':
    img[0,0] = mx; img[0,1] = mn
img = (z2o(img)*255).astype(np.uint8)






O=h5r('/media/karlzipser/rosbags/h5py/tegra-ubuntu_12Nov18_20h56m16s/original_timestamp_data.h5py' )
p=O['points']
v=p['vals']

xy1 = 0
xy2 = 1
z = 2
rng = 3
angle = 4
intensity = 5

for i in range(4000,7000):
    s = v[i,:,:].astype(np.float32) # (16384, 6)
    r = s[:256*16,rng]
    r1 = r.reshape((256,16)).transpose(1,0)
    r2 = cv2.resize(r1,(256,64))
    mci((z2o(r2)*255).astype(np.uint8),delay=33,scale=4.0,color_mode=cv2.COLOR_GRAY2BGR,title='ZED')








for f in sggo('/home/karlzipser/Desktop/Depth_images_15_16Nov2018','*'):
    sys_str = d2s("ln -s",f,'/media/karlzipser/1_TB_Samsung_n1/_.Depth_images.log.resize.flip.left_ts/'+fname(f))
    print sys_str
    os.system(sys_str)



PROJECT_DIR = '/kzpy3/scratch/VT_b/'
if PROJECT_DIR[0] == '/':
    PROJECT_DIR = PROJECT_DIR[1:]
if PROJECT_DIR[-1] == '/':
    PROJECT_DIR = PROJECT_DIR[:-1]
PROJECT_IMP = PROJECT_DIR.replace('/','.')



#EOF