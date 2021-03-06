


def dist(A,B):
    return np.sqrt( (A[0]-B[0])**2 + (A[1]-B[1])**2 )

def distance_decimate_vector(v,d):
    ref = v[0,:]
    u = [ref]
    for i in range(0,len(v)-1):
        e = dist(v[i],v[i+1])
        if dist(ref,v[i]) >= d:
        	ref = v[i]
        	u.append(ref)
    u.append(v[-1])
    return na(u)



P = {}

from kzpy3.Learn.get_data.runs import All_runs

for r in All_runs['validate']:
    P[r] = find_files_recursively(opjD('Data'),r,DIRS_ONLY=True)

P = {'Mr_Black_24Sep18_18h52m26s': {'parent_folders': ['h5py'],
  'paths': {'2_TB_Samsung_n3/preprocessed_5Oct2018_500GB/bdd_car_data_late_Sept2018_lrc/locations/local/left_right_center/h5py': ['Mr_Black_24Sep18_18h52m26s']},
  'pattern': 'Mr_Black_24Sep18_18h52m26s',
  'src': '/home/karlzipser/Desktop/Data/'},
 'tegra-ubuntu_01Nov18_13h46m55s': {'parent_folders': ['h5py'],
  'paths': {'1_TB_Samsung_n1/left_direct_stop__31Oct_to_1Nov2018/locations/local/left_direct_stop/h5py': ['tegra-ubuntu_01Nov18_13h46m55s']},
  'pattern': 'tegra-ubuntu_01Nov18_13h46m55s',
  'src': '/home/karlzipser/Desktop/Data/'},
 'tegra-ubuntu_07Oct18_18h24m28s': {'parent_folders': ['h5py'],
  'paths': {'2_TB_Samsung_n3/preprocessed_5Oct2018_500GB/bdd_model_car_data_early_8Oct2018_lrc_LIDAR/locations/local/left_right_center/h5py': ['tegra-ubuntu_07Oct18_18h24m28s']},
  'pattern': 'tegra-ubuntu_07Oct18_18h24m28s',
  'src': '/home/karlzipser/Desktop/Data/'},
 'tegra-ubuntu_12Nov18_20h56m16s': {'parent_folders': ['h5py'],
  'paths': {'2_TB_Samsung_n3/rosbags__preprocessed_data/tu_15to16Nov2018/locations/local/left_direct_stop/h5py': ['tegra-ubuntu_12Nov18_20h56m16s']},
  'pattern': 'tegra-ubuntu_12Nov18_20h56m16s',
  'src': '/home/karlzipser/Desktop/Data/'},
 'tegra-ubuntu_12Oct18_11h11m30s': {'parent_folders': ['h5py'],
  'paths': {'1_TB_Samsung_n1/tu_8to12Oct2018/locations/local/left_right_center/h5py': ['tegra-ubuntu_12Oct18_11h11m30s']},
  'pattern': 'tegra-ubuntu_12Oct18_11h11m30s',
  'src': '/home/karlzipser/Desktop/Data/'},
 'tegra-ubuntu_16Nov18_15h59m28s': {'parent_folders': ['h5py'],
  'paths': {'2_TB_Samsung_n3/rosbags__preprocessed_data/tu_15to16Nov2018/locations/local/left_direct_stop/h5py': ['tegra-ubuntu_16Nov18_15h59m28s']},
  'pattern': 'tegra-ubuntu_16Nov18_15h59m28s',
  'src': '/home/karlzipser/Desktop/Data/'},
 'tegra-ubuntu_17Oct18_12h11m22s': {'parent_folders': ['h5py'],
  'paths': {'1_TB_Samsung_n1/tu_16to18Oct2018/locations/local/left_right_center/h5py': ['tegra-ubuntu_17Oct18_12h11m22s']},
  'pattern': 'tegra-ubuntu_17Oct18_12h11m22s',
  'src': '/home/karlzipser/Desktop/Data/'},
 'tegra-ubuntu_25Oct18_10h21m55s': {'parent_folders': ['h5py'],
  'paths': {'1_TB_Samsung_n1/tu_25to26Oct2018/locations/local/left_right_center/h5py': ['tegra-ubuntu_25Oct18_10h21m55s']},
  'pattern': 'tegra-ubuntu_25Oct18_10h21m55s',
  'src': '/home/karlzipser/Desktop/Data/'},
 'tegra-ubuntu_25Oct18_15h43m36s': {'parent_folders': ['h5py'],
  'paths': {'1_TB_Samsung_n1/tu_25to26Oct2018/locations/local/left_right_center/h5py': ['tegra-ubuntu_25Oct18_15h43m36s']},
  'pattern': 'tegra-ubuntu_25Oct18_15h43m36s',
  'src': '/home/karlzipser/Desktop/Data/'}}

Q = {}
l = []
for r in P:
    O = P[r]
    Q[r] = opj(O['src'],a_key(O['paths']), O['pattern'])
    clp("mkdir -p",Q[r])
    clp("scp -P 1022 -r karlzipser@bdd3.neuro.berkeley.edu:'"+opj(Q[r],'*')+"'",  Q[r])
    print ''



#,a

Arguments = {
    'run_name':'tegra-ubuntu_31Oct18_16h06m32s',
}

def vec(heading,encoder,motor,sample_frequency=30.,vel_encoding_coeficient=1.0/2.6): #2.3): #3.33
    velocity = encoder * vel_encoding_coeficient # rough guess
    if motor < 49:
        velocity *= -1.0
    a = [0,1]
    a = array(rotatePoint([0,0],a,heading))
    a *= velocity/sample_frequency
    return array(a)


if 'o' not in locals():
  o = {}
assert type(o) is dict


if 'O' not in o:

  o['L'],o['O'],__flip = open_run2(Arguments['run_name'])

  o['xy'] = [na([0,0])]

  L = o['L']
  for i in rlen(L['motor']):
      a = vec(
          L['gyro_heading_x_meo'][i],
          L['encoder_meo'][i],
          L['motor'][i],
      )
      o['xy'].append(o['xy'][-1]+a)

  o['S'] = lo(opjD('Data/outer_contours/output_2_data/train/tegra-ubuntu_31Oct18_16h06m32s.pkl'))


figure(1)
clf()
plt_square()
for i in range(6000,8000,20):
  b = o['S'][i]
  xy = b['outer_countours_rotated_left']
  plot(xy[:,0],xy[:,1],ms=3)
  plot([-1,1],[0,0],'k:')
  plot([0,0],[-1,1],'k:')
  spause()
  time.sleep(0.3)

#,b


