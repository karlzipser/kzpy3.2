from argparse import ArgumentParser
"""
e.g.s,

python kzpy3/caf2/main.py --deploy --model m4d3_example_model2

python kzpy3/caf2/main.py --train 2000 --model m4d3_example_model2

python kzpy3/caf2/main.py --model m4d3_example_model2 --define
"""

#############################################################
#
if __name__ == '__main__':
	parser = ArgumentParser('Caffe model.\n')
	parser.add_argument("--model",type=str, help="--train")
	parser.add_argument("--define", action="store_true", help="--define")
	parser.add_argument("--train", type=int, help="--train")
	parser.add_argument("--test", type=int, help="--test")
	parser.add_argument("--deploy", action="store_true", help="Deploy model")
	parser.add_argument("--latest", action="store_true", help="Load latest model")
	args = parser.parse_args()
	if args.model:
		exec("from kzpy3.caf2.models."+args.model+".model import *")
		print dis['model_name']
	if args.define:
		print('--define.')
		define()
	if args.train:
		print('--train.')
		solver = setup_solver(dis['model_name'])
		if args.latest:
			print('--latest')
			solver = load_latest(solver,dis['model_name'],'.caffemodel')
		collect_train_data()
		train_solver(solver,args.train)
	if args.test:
		solver = setup_solver(dis['model_name'])
		if args.latest:
			print('--latest')
			solver = load_latest(solver,dis['model_name'])
		collect_test_data()
		test_solver(solver,args.test)
	if args.deploy:
		print 'deploy it!'
#
#############################################################
