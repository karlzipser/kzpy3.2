
run "kzpy3/caf/training/y2016/m3/RPi3/train.py"

shape(net.params['conv1'][0].data[0,0,:,:])

solver.net.copy_from(opjD('bvlc_reference_caffenet.caffemodel'))

safe_solver_step(solver)

for k in solver.net.blobs.keys():
    print (k, solver.net.blobs[k].data.max())


