from kzpy3.utils import *

def mark_ctimes():
	dirs = next(os.walk('.'))[1]
	for d in dirs:
		print d
		_,l = dir_as_dic_and_list(d)
		clst = []
		for m in l:
			c = os.path.getctime(opj(d,m))
			clst.append(d2s(c,m))
		list_of_strings_to_txt_file('ctimes_'+d+'.txt',clst)

if __name__ == '__main__':
	mark_ctimes()