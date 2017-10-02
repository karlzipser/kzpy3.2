from Parameters_Module import *




def Data_Packer(**Args):

	for we_are in ['the setup section']:

		_ = {}
		_[RUNS] = Runs()

	for we_are in ['function definitions']:

		def _next(**Args):
			batch_number = Args[BATCH_NUM]
			run_path = _[RUNS][SORTED_PATHS_OF_BATCHED][batch_number]
			Rn = All_runs[run_path]

			Data = Rn[READ](TOPICS=['steer','motor','left_image','right_image','acc_x_meo'])
			# convert data to items in return list

			name = fname(run_path)

			return name,images,metadata,targets


	for we_are in ['the place where we name the functions']:

		_[NEXT] = _next


	for we_are in ['the return section.']:
	
		return _


