

#,a
 
Arguments = {
    'run': 'tegra-ubuntu_12Oct18_11h11m30s',#'tegra-ubuntu_07Oct18_18h24m28s'#'tegra-ubuntu_17Oct18_12h11m22s'#'tegra-ubuntu_16Nov18_15h59m28s'
    # 'tegra-ubuntu_12Nov18_20h56m16s',#'tegra-ubuntu_31Oct18_16h06m32s'#  ,
}

def vec(heading,encoder,motor,sample_frequency=30.,vel_encoding_coeficient=1.0/2.6): #2.3): #3.33
    velocity = encoder * vel_encoding_coeficient # rough guess
    if motor < 49:
        velocity *= -1.0
    a = [0,1]
    a = array(rotatePoint([0,0],a,heading))
    a *= velocity/sample_frequency
    return array(a)

Colors = {'direct':'b','left':'r','right':'g'}

if 'o' not in locals():
  o = {}
assert type(o) is dict


if 'O' not in o:

  if len(sggo(opjD('Data/train/h5py',Arguments['run']))) > 0:
      run_type = 'train'
      assert(False)
  elif len(sggo(opjD('Data/validate/h5py',Arguments['run']))) > 0:
      run_type = 'validate'
  else:
      clp(Arguments['run'],'not found')
      assert False

  o['L'],o['O'],__flip = open_run2(Arguments['run'])

  o['xy'] = [na([0,0])]

  L = o['L']
  for i in range(10000): #  rlen(L['motor']):
      a = vec(
          L['gyro_heading_x_meo'][i],
          L['encoder_meo'][i],
          L['motor'][i],
      )
      o['xy'].append(o['xy'][-1]+a)

  o['S'] = lo(opjD('Data/outer_contours/output_2_data',run_type,Arguments['run']))


figure(1)
clf()
plt_square()
for i in range(7500,10000,1):
  if not L['drive_mode'][i]:
    cr(i,'d')
    continue
  if L['motor'][i] < 54 or L['encoder'][i] < 2.0:
    cr(i,'e')
    continue
  if i not in o['S']:
    cr(i)
    continue
  else:
    cm(i,ra=0)
    x,y  = o['xy'][i][0],o['xy'][i][1]
  clf();plt_square();xylim(x-20,x+20,y-20,y+20)
  b = o['S'][i]
  for s in ['left','right']:
    xy = b['outer_countours_rotated_'+s] + o['xy'][i]
    pts_plot(xy,color=Colors[s],sym='-')
    #plot(xy[:,0],xy[:,1],ms=3)
  plot(na([-10,10])+x,na([0,0])+y,'k:')
  plot(na([0,0])+x,na([-10,10])+y,'k:')


  for s in ['left','right']:
    for j in rlen(b['outer_countours_rotated_'+s]):
      a = b['angles_'+s][j]
      a = min(np.abs(a),400)
      marker_size = int(a/2.)
      pts_plot(b['outer_countours_rotated_'+s][j] + o['xy'][i],Colors[s],sym='.',ms=marker_size)


  spause()
  mci(o['O']['left_image']['vals'][i],title='left_image',scale=3.0)
  time.sleep(0.05)

#,b


