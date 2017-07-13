from kzpy3.misc.frames_readied_for_video import *

rgb_1to4_path = '/home/karlzipser/Desktop/bair_car_data/rgb_1to4/direct_Tilden_18Dec16_13h27m25s_Mr_Blue'
jpg_path = '/media/karlzipser/ExtraDrive1/direct_Tilden_18Dec16_13h27m25s_Mr_Blue_frames'

Done = True
if not Done:
	meta = load_obj('/media/karlzipser/bair_car_data_8/bcd/direct_Tilden_18Dec16_13h27m25s_Mr_Blue/.preprocessed2/left_image_bound_to_data.pkl')
	bag_pkl_files = sgg(opj(rgb_1to4_path,'*.bag.pkl'))	
	ctr = 0
	for i in range(6,len(bag_pkl_files)):
		bkf = bag_pkl_files[i]
		print bkf
		d = load_obj(bkf)
		left = d['left']
		ts = sorted(left.keys())
		for t in ts:
			img = left[t]
			state = meta[t]['state']
			if state != 6:
				img[:,:,1:] /= 4
			imsave(opj(jpg_path,d2p(ctr,'jpg')),img)
			if np.mod(ctr,20) == 0:
				mi(img)
				pause(0.01)
			ctr += 1

frames_to_video_with_ffmpeg(jpg_path)
	

