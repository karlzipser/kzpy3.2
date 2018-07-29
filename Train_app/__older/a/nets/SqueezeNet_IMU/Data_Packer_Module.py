from Parameters_Module import *
from vis2 import *

rnd = np.random.random((94, 168, 1))

def Data_Packer(**Args):

	for we_are in ['the setup section']:

		D = {}
		D[RUNS] = Args[RUNS]
		D[DATA] = None
	for we_are in ['function definitions']:

		def _next():

			
			Rn = D[RUNS][GET_RUN]()

			D[DATA] = Rn[READ](TOPICS=['state','steer','motor','left_image','right_image'])
			while D[DATA] == None:

				D[DATA] = Rn[READ](TOPICS=['state','steer','motor','left_image','right_image'])

			name = fname(Rn[PATH])

			
			images = []
			for t in range(P[N_FRAMES]):
				for s in ['left_image','right_image']:
					for c in [0,1,2]:
						images.append(np.expand_dims(D[DATA][s][t][:,:,c],axis=2))
			


			

			metadata = [1]

			targets = list(D[DATA]['steer']/99.0)+list(D[DATA]['motor']/99.0)
			
			return name,images,metadata,targets


	for we_are in ['the place where we name the functions']:

		D[NEXT] = _next

	for we_are in ['the return section.']:
	
		return D


