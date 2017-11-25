# Setting up reprocessing of aruco data, 22 Nov. 2017


isdir = os.path.isdir

def folder_to_dic(D,top):
	try:
		D[fname(top)] = {}
		items = sggo(top,'*')

		for i in items:
			if isdir(i):
				
				D[fname(top)][fname(i)] = {}
				D[fname(top)][fname(i)] = folder_to_dic(D[fname(top)][fname(i)],i)
			else:
				D[fname(top)][fname(i)] = dp(os.path.getsize(i)/(10.0**6))
	except Exception as e:
		print("**********folder_to_dic Exception ***********************")
		print(e.message, e.args)
	return D[fname(top)]





def ls_dic(D,tabs=0):
	tabstr = ''
	for i in range(tabs):
		tabstr += '\t'
	for k in D.keys():
		if type(D[k]) != dict:
			pd2s(tabstr,k,':',D[k])
		else:
			pd2s(tabstr,k,':')
			ls_dic(D[k],tabs=tabs+1)
			




def look_for_bag_files(D,Q,current,path=''):
	path = opj(path,current)
	for k in D.keys():
		if type(D[k]) != dict:
			if type(k) == str:
				if k.split('.')[-1] == 'bag':
					#print current,'---->',k
					Q[current] = path
		else:
			look_for_bag_files(D[k],Q,k,path)	


D={}
ExtraDrive1 = folder_to_dic(D,'/media/karlzipser/ExtraDrive1')
D={}
ExtraDrive2 = folder_to_dic(D,'/media/karlzipser/ExtraDrive2')
D={}
ExtraDrive3 = folder_to_dic(D,'/media/karlzipser/ExtraDrive3')
D={}
ExtraDrive4 = folder_to_dic(D,'/media/karlzipser/ExtraDrive4')

Q = {}
look_for_bag_files(ExtraDrive1,Q,'/media/karlzipser/ExtraDrive1')
look_for_bag_files(ExtraDrive2,Q,'/media/karlzipser/ExtraDrive2')
look_for_bag_files(ExtraDrive3,Q,'/media/karlzipser/ExtraDrive3')
look_for_bag_files(ExtraDrive4,Q,'/media/karlzipser/ExtraDrive4')




all_runs = []
folders = sggo(opjD('all_aruco','*'))
for f in folders:
	runs = sggo(f,'h5py','*')
	for r in runs:
		all_runs.append(fname(r))

so(all_runs,opjD('all_aruco_runs'))



#test with cmd/motor and cmd/steer
python kzpy3/Data_app/Main.py SRC '/media/karlzipser/ExtraDrive1/not_backed_up/A/new'  DST '/media/karlzipser/2_TB_Samsung/A/h5py'




all_aruco_runs = lo('/home/karlzipser/Desktop/all_aruco_runs.pkl')
ExtraDrive_bag_files = lo('/home/karlzipser/Desktop/ExtraDrive_bag_files.pkl')
ExtraDrive_aruco_bag_folders = {}
lacking = 0
for a in all_aruco_runs:
	if a in ExtraDrive_bag_files:
		ExtraDrive_aruco_bag_folders[a] = ExtraDrive_bag_files[a]
	else:
		print 'lacking '+a
		lacking += 1
pd2s('lacked',dp(100.0*lacking/(1.0*len(all_aruco_runs))),'%')




links = {'ExtraDrive1':'/media/karlzipser/2_TB_Samsung/ExtraDrive1/new',
	'ExtraDrive2':'/media/karlzipser/2_TB_Samsung_n2/ExtraDrive2/new',
	'ExtraDrive3':'/media/karlzipser/1_TB_Samsung_n1/ExtraDrive3/new',
	'ExtraDrive4':'/media/karlzipser/1_TB_Samsung_n2/ExtraDrive4/new'}
for k in ExtraDrive_aruco_bag_folders.keys():
	for l in links.keys():
		if l in ExtraDrive_aruco_bag_folders[k]:
			unix_str = d2s('ln -s',ExtraDrive_aruco_bag_folders[k],opj(links[l],k))
			print unix_str
			unix(unix_str,False)
			break





# 23 Nov. 2017
all_runs = []
runs = sggo('/home/karlzipser/Desktop/bair_car_data_new_28April2017/hdf5/runs','*')
for r in runs:
	if 'flip' not in r:
		all_runs.append(fname(r).split('.')[0])

so(all_runs,opjD('all_Fern_aruco_runs'))

all_aruco_runs = lo('/home/karlzipser/Desktop/all_Fern_aruco_runs.pkl')
ExtraDrive_bag_files = lo('/home/karlzipser/Desktop/ExtraDrive_bag_files.pkl')
ExtraDrive_aruco_bag_folders = {}
lacking = 0
for a in all_aruco_runs:
	if a in ExtraDrive_bag_files:
		ExtraDrive_aruco_bag_folders[a] = ExtraDrive_bag_files[a]
	else:
		print 'lacking '+a
		lacking += 1
pd2s('lacked',dp(100.0*lacking/(1.0*len(all_aruco_runs))),'%')


#
##################################################
# 24 Nov. 2017
o=lo('/home/karlzipser/Desktop/BAIR_CAR_DATA_DISKS.pkl' )

bair_car_data_disks = {}

for p in o:
	disk = p.keys()[0]
	bair_car_data_disks[disk] = p[disk]

Q = {}
look_for_bag_files(bair_car_data_disks,Q,'/media/karlzipser')

so(opjD('bair_car_data_disks_bag_files'),Q)

bair_car_data_disks_bag_files = Q

all_Fern_aruco_runs = lo('/home/karlzipser/Desktop/all_Fern_aruco_runs.pkl' )

bair_car_data_bag_folders = {}
lacking = 0
for a in all_Fern_aruco_runs:
	if a in bair_car_data_disks_bag_files:
		bair_car_data_bag_folders[a] = bair_car_data_disks_bag_files[a]
	else:
		print 'lacking '+a
		lacking += 1
pd2s('lacked',dp(100.0*lacking/(1.0*len(all_Fern_aruco_runs))),'%')

so(opjD('bair_car_data_bag_folders'),bair_car_data_bag_folders)

disk_names = []
for d in bair_car_data_bag_folders:
	disk_names.append(bair_car_data_bag_folders[d].split('/')[3])
disk_names = sorted(disk_names)
print(set(disk_names)) # set(['bair_car_data_14', 'bair_car_data_16', 'bair_car_data_8', 'bair_car_data_12', 'bdd_data_11a'])
#
##################################################
#

dst_disk = '2_TB_Samsung_n3'
src_disk = 'bair_car_data_8'
bair_car_data_bag_folders = lo('/home/karlzipser/Desktop/bair_car_data_bag_folders.pkl' )
for f in bair_car_data_bag_folders:
	if src_disk in bair_car_data_bag_folders[f]:
		unix_str = d2s('ln -s',bair_car_data_bag_folders[f],opjm(dst_disk,'new'))
		print unix_str
		unix(unix_str,False)













#################################################
#
set(raise_aruco_1).intersection(set(bdd_car_data_Sept2017_aruco_demo))


top = '/media/karlzipser/2_TB_Samsung/full_raised'#'/home/karlzipser/Desktop/raise_aruco_1'#'/home/karlzipser/Desktop/sorting_data'#'/media/karlzipser/2_TB_Samsung/sorting_data' #  
D={};E=folder_to_dic(D,top)
runs = []
#for i in D.keys():
for j in D.keys():
	if 'h5py' in D[j]:
		runs += D[j]['h5py'].keys()
runs_on_external = runs
#runs_on_computer = runs

len(set(runs_on_external).intersection(set(runs_on_computer)))

# 20 Nov. 2017

O = h5r('/home/karlzipser/Desktop/direct_local_arena_16_17_Sept_with_aruco/direct_local_16Sep17_14h35m25s_Mr_Lt_Blue/original_timestamp_data.h5py')
l = len(O['left_image']['vals'][:])
timer = Timer()
for i in range(1000):
	img = O['left_image']['vals'][np.random.randint(l)]
print timer.time() # = 0.295176029205


timer = Timer()
for i in range(1000):
	img = cv2.flip(O['left_image']['vals'][1500],1)
print timer.time() # = 0.260668992996

folder = '/home/karlzipser/Desktop/bdd_car_data_Sept2017_aruco_demo_4'
Aruco_Steering_Trajectories = sggo(folder,'Aruco_Steering_Trajectories/*.pkl')

for a in Aruco_Steering_Trajectories:
	run_name = a.split('/')[-1].split('.')[0]
	unix_str = d2s('mv',opj('/home/karlzipser/Desktop/bdd_car_data_Sept2017_aruco_demo/h5py',run_name),opj(folder,'h5py'))
	print unix_str
	unix(unix_str,False)

# 20 Nov. 2017

folder = '/home/karlzipser/Desktop/full_raised'
observer_folder = '/home/karlzipser/Desktop/full_raised_observer'
runs = sggo(folder,'h5py/*')

for a in runs:
	run_name = fname(a)
	F = h5r(opj(a,'left_timestamp_metadata_right_ts.h5py'))
	print run_name,'state' in F.keys()
	if 'state' in F.keys():
		observer = False
	else:
		observer = True
	F.close()
	if observer:
		unix_str = d2s('mv',a,opj(observer_folder,'h5py'))
		print unix_str
		unix(unix_str,False)
#
##################################################

