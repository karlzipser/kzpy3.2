import cortex
from kzpy3.vis import *
import nibabel as nib

data = (nib.load('/anaconda/share/pycortex/db/S12015/transforms/9Feb2015/reference.nii.gz')).get_data()
plt.imshow(data[:,:,15+8], 'gray')
xfm4 = [
        [
            -0.4995994678369924, 
            -0.019996737489212147, 
            -0.0006266201378814862, 
            56.16803995155992
        ], 
        [
            -0.020005037243645312, 
            0.49950927620830793, 
            0.009500055504327337, 
            42.09963292688167
        ], 
        [
            -0.00024604865717980104, 
            -0.009517489024347424, 
            0.4999092496743478, 
            8.028009364968176
        ], 
        [
            0.0, 
            0.0, 
            0.0, 
            1.0
        ]
    ]
xfm4=np.array(xfm4)
xfm3=xfm[:3,:3]
wmlst_xfm = xfm3.dot(wmlst.T)
wmpts_xfm = xfm3.dot(wmpts.T)
wmpts_xfm = wmpts_xfm.T
piapts_xfm = xfm3.dot(piapts.T)
piapts_xfm = piapts_xfm.T


from cortex import surfs
wmpts, polys = surfs.get_surf('S12015', 'wm', merge=True)
wmlst = []
for p in range(shape(wmpts)[0]):
	if wmpts_xfm[p,2] > 15 and wmpts_xfm[p,2] < 16:
		wmlst.append(wmpts_xfm[p,:])
wmlst = np.array(wmlst)
wmx = wmlst[:,0]
wmy = wmlst[:,1]
#plt.clf()
plt.plot(wmy+42,wmx+56,'.',markersize=2)
piapts, polys = surfs.get_surf('S12015', 'pia', merge=True)
pialst = []
for p in range(shape(piapts)[0]):
    if piapts_xfm[p,2] > 15 and piapts_xfm[p,2] < 16:
        pialst.append(piapts_xfm[p,:])
pialst = np.array(pialst)
piax = pialst[:,0]
piay = pialst[:,1]
#plt.clf()
plt.plot(piay+42,piax+56,'.',markersize=2)


for i in range(len(pialst)):
    if np.random.random(1)>0.95:
        clr = 'r'
    else:
        clr = 'r'
    plt.plot([pialst[i,0],wmlst[i,0]],[pialst[i,2],wmlst[i,2]],clr)
    #plt.plot([piay[i]+42,wmy[i]+42],[piax[i]+56,wmx[i]+56],clr)






wmlst = []
pialst = []
for p in range(shape(wmpts)[0]):
	if wmpts[p,1] > 15 and wmpts[p,1] < 16:
		wmlst.append(wmpts[p,:])
		pialst.append(piapts[p,:])
wmlst = np.array(wmlst)
pialst = np.array(pialst)
wmx = wmlst[:,0]
wmy = wmlst[:,1]
piax = pialst[:,0]
piay = pialst[:,1]
plt.figure(9)
plt.clf()
#plt.plot(wmx,wmy,'o')
#plt.plot(piax,piay,'o')
for i in range(len(piax)):
	if np.random.random(1)>0.95:
		clr = 'r'
	else:
		clr = 'b'
	plt.plot([pialst[i,0],wmlst[i,0]],[pialst[i,2],wmlst[i,2]],clr)


piapts, polys = surfs.get_surf('S12015', 'pia', merge=True)
pialst = []
for p in range(shape(piapts)[0]):
	if piapts[p,2] > 20 and piapts[p,2] < 21:
		pialst.append(piapts[p,:])
pialst = np.array(pialst)
piax = pialst[:,0]
piay = pialst[:,1]
#plt.clf()
plt.plot(piax,piay,'o')

flatpts, polys = surfs.get_surf('S12015', 'flat', merge=True)
flatlst = []
for p in range(shape(flatpts)[0]/2):
	if flatpts[p,2] > 20 and flatpts[p,2] < 30:
		flatlst.append(flatpts[p,:])
flatlst = np.array(flatlst)
flatx = flatlst[:,0]
flaty = flatlst[:,1]
plt.figure(2)
plt.plot(flatx,flaty,'o')

"""
https://surfer.nmr.mgh.harvard.edu/fswiki/VolumeRoiCorticalThickness
https://surfer.nmr.mgh.harvard.edu/fswiki/CreatingROIs#FromFunctionalActivationonSurface
https://surfer.nmr.mgh.harvard.edu/fswiki/FsFastTutorialV5.1/FsFastGroupLevel
https://surfer.nmr.mgh.harvard.edu/fswiki/FsTutorial/MultiModalFmriIndividual_tktools
"""


"""
tksurfer S12015 lh smoothwm
tksurfer S12015 rh smoothwm
mris_flatten -O fiducial /Users/karlzipser/freesurfer/subjects/S12015/surf/lh.flatten.patch.3d /Users/karlzipser/freesurfer/subjects/S12015/surf/lh.flat.patch
mris_flatten -O fiducial /Users/karlzipser/freesurfer/subjects/S12015/surf/rh.flatten.patch.3d /Users/karlzipser/freesurfer/subjects/S12015/surf/rh.flat.patch

mris_flatten /Users/karlzipser/freesurfer/subjects/S12015/surf/lh.flatten.patch.3d /Users/karlzipser/freesurfer/subjects/S12015/surf/lh.flat.patch
mris_flatten /Users/karlzipser/freesurfer/subjects/S12015/surf/rh.flatten.patch.3d /Users/karlzipser/freesurfer/subjects/S12015/surf/rh.flat.patch



# 29 Feb. 2016
# This shows the process needed for marking visual areas
import cortex
view = cortex.Volume.random("S12015","9Feb2015",cmap="hot")

#cortex.add_roi(view,'A2')

rois = cortex.get_roi_verts('S12015', roi='V1')
v1=rois['V1']

mapper = cortex.get_mapper('S12015','9Feb2015')
l,r = mapper.backwards(v1)
mask = l+r

#view.data = mask
#img = cortex.quickflat.make(view)
#mi(img[0],4)

#mi(mask.mean(axis=0),22)

import h5py
f = h5py.File('/Users/karlzipser/2015/10/2015-10/HVO_RF_mapping.736252.5459.mat','r')
h = f['HVO_RF_mapping']
selected_voxel_xyzs = h[u'selected_voxel_xyzs'][:,:]
selected_voxel_xyzs -= 1 # matlab to python indexing

rmask = zeros((60,106,106))+0.5

for i in range(shape(selected_voxel_xyzs)[1]):
	x,y,z = selected_voxel_xyzs[:,i]
	rmask[z,y,x] = 1
# rmask[y,z,x]
# 	rmask[z,x,y]
view.data = rmask
fig = cortex.quickflat.make_figure(view,depth=0.5,thick=32,sampler='trilinear')

img = cortex.quickflat.make(view)
plt.clf()
mi(img[0],4)
cortex.webshow((rmask,"S12015","9Feb2015"))

import nibabel as nib
"""


# mris_convert -p lh.flat.patch flat_lh.gii

"""
import cortex
from kzpy3.vis import *
plt.ion()
plt.show()
view = cortex.Volume.random("S12015","one",cmap="hot")
cortex.add_roi(view,'A1')
rois = cortex.get_roi_verts('S12015', roi='NEW12');rois
lh,rh = cortex.db.get_surf('S12015','flat')

img = np.zeros((500,500))
for i in range(len(rh[0])):
    x=rh[0][i,0]+250
    y=rh[0][i,1]+250
    if img[x,y] < 5:
    	img[x,y]+=1
plt.clf()
mi(img)

img = np.zeros((500,500))
for i in range(len(lh[0])):
    x=lh[0][i,0]+250
    y=lh[0][i,1]+250
    if img[x,y] < 5:
    	img[x,y]+=1
plt.clf()
mi(img,2)



import cortex
view = cortex.Volume.random("S1","fullhead",cmap="hot")

X,Y,Z = shape(view.data)
for x in range(X):
	for y in range(Y):
		for z in range(Z):
			view.data[x,y,z] = y
			if np.random.random(1) > 0.9:
				view.data[x,y,z] = 25
view.data[:,:,Y/2-4]=101
fig=cortex.quickflat.make_figure(view)
im[np.isnan(im)]=0
plt.figure(2);plt.clf()
mi(im,2)
#cortex.quickflat.make_png(opjD('temp2.png'),view)



from kzpy3.vis import *
plt.ion()
plt.show()
view = cortex.Volume.random("S1","fullhead",cmap="hot")
rois = cortex.get_roi_verts('S12015', roi='NEW12');rois
v1=rois['NEW12']

lh,rh = cortex.db.get_surf('S1','flat')

img = np.zeros((500,500))

for i in range(len(lh[0])):
    x=lh[0][i,0]+250
    y=lh[0][i,1]+250
    if img[x,y] < 5:
    	img[x,y]+=1

for i in range(len(v1)):
	j = v1[i]
	try:
	    x=lh[0][j,0]+250
	    y=lh[0][j,1]+250
	    img[x,y]=5
	except:
		pass

mapper = cortex.get_mapper('__S12015','one')
l,r = mapper.backwards(v1)
mask = l+r
plt.figure(20)
plt.clf()
mi(mask.mean(axis=0),20)

plt.figure(10)
plt.clf()
mi(img,10)



"""