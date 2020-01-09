from kzpy3.utils3 import *
import torch

# TX1 .cuda ctr = 6414
# TX1 .cpu ctr = 3123
# Macbook .cpu 4123
# TX2 .cuda ctr = 3571
# TX2 .cpu ctr = 2588

timer = Timer(10)
a = torch.from_numpy(rnd((100,100,100))).cuda()
ctr = 0
while not timer.check():
	b = a + a
	ctr += 1

cg('ctr =',ctr)