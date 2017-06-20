
import kzpy3.teg9.data.utils.get_new_A as get_new_A
import kzpy3.teg9.data.utils.multi_preprocess_pkl_files_1 as multi_preprocess_pkl_files_1
bag_folders_dst_rgb1to4_path = '/media/karlzipser/ExtraDrive4/bair_car_data_new_28April2017/rgb_1to4'
bag_folders_dst_meta_path = '/media/karlzipser/ExtraDrive4/bair_car_data_new_28April2017/meta'# opjD('bair_car_data_new/meta')# '/media/karlzipser/ExtraDrive4/bair_car_data_new_28April2017/meta'
from kzpy3.vis import *


def pt_plot(xy,color='r'):
    plot(xy[0],xy[1],color+'.')

def pts_plot(xys,color='r'):
    for xy in xys:
        pt_plot(xy,color)

        
S = {}
S['Purpose'] = "This dictionary holds trajectories keyed by steer and motor data."
for s in range(0,105,5):
	for m in range(0,100,5):
		S[s,m] = {}
		S[s,m]['raw'] = []

N = lo(opjD('N.pkl'))
car_name = 'Mr_Black'
for run_name in N[car_name].keys():
	print(d2s(run_name,'started . . .'))
	if True: #try:
		traj = N[car_name][run_name]['self_trajectory']
		traj['data'] = get_new_A.get_new_A()
		try:
			multi_preprocess_pkl_files_1.multi_preprocess_pkl_files(
				traj['data'],
					opj(bag_folders_dst_meta_path,traj['run_name']),
					opj(bag_folders_dst_rgb1to4_path,traj['run_name']),
					load_images=False)
		except:
			print(d2s(run_name,"FILE NOT FOUND"))
			continue



		################




		"""
		def dTime_check():
			if time.time()
		def dTime(t):
			T = {}
			T
			T['start_time'] = time.time()
			T['check']
		"""







		xy = {}
		for side in ['left','right']:
			xy[side] = array([traj[side]['x'],traj[side]['y']]).transpose()
		colors = {'left':'r','right':'b'}

		steer = array(traj['data']['steer']).astype(int)
		motor = array(traj['data']['motor']).astype(int)
		state = array(traj['data']['state']).astype(int)
		if len(steer)<1:
			print(d2s(run_name,'lacks steer, continuing'))
			continue
		assert(len(steer)>0)
		assert(len(motor)>0)
		assert(len(state)>0)


		figure(1)
		timer = Timer(0.5)
		NN = 30
		MM = 3

		for i in range(0,len(xy['left'])-NN,1):

			if traj['camera_separation'][i] < 0.25 and motor[i] >= 55 and int(state[i]) in [1,3,5,6,7]:
				for side in ['left','right']:
					if True: #try:
						A = array(xy[side][i:(i+NN)])
						A = A - A[0]
						angs = []
						for j in range(1,MM+1):
						    angs.append(angle_between([0,1],A[j]))
						avg_ang = np.degrees(array(angs).mean())

						if A[1][0] > 0:
						    avg_ang *= -1.0
						B = rotatePolygon(A,-avg_ang)
						#print((b,type(b)))
						for b in B:
							for w in [0,1]:
								if math.isnan(b[w]):
									assert('nan found')
						if B[-1][1] > 0.3:
							s5,m5 = int(5*round(steer[i]/5.0)),int(5*round(motor[i]/5.0))
							S[s5,m5]['raw'].append(B)
						#print(len(S[s5,m5]['raw']))
					#except Exception as e:
					#	print("AAA********** Exception ***********************")
					#	print(e.message, e.args)
				    
						if timer.check():
						    if side == 'left':
								clf()
								xlim(-0.7,0.7)
								ylim(0,0.7)
						    pts_plot(B,colors[side])
						    if side == 'right':
						    	pause(0.000033)#raw_input('---')
						    	#raw_input('asdf')
					    		timer.reset()


	#except Exception as e:
	#	print("********** Exception ***********************")
	#	print(e.message, e.args)


for s in range(0,100,5):
	for m in range(0,100,5):
		med = np.median(array(S[s,m]['raw']),axis=0)
		S[s,m]['median'] = med


for ss in range(0,100,5):
	for m in range(50,100,5):
		for s in [ss]:
			print(s,m,len(S[s,m]['raw']))
			if 'median' in S[s,m]:
				if not is_number(S[s,m]['median']):
					pts_plot(S[s,m]['median'])
					pause(0.00001)
	clf()
	xlim(-2,2)
	ylim(0,2)




def traj_seg_length(pts):
	l = 0
	for i in range(1,len(pts)):
		l += length(pts[i]-pts[i-1])
	return l

