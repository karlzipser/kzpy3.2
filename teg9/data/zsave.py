from kzpy3.utils2 import *


def text_to_file(txt,path):
	text_to_file_({'txt':txt,'path':path})
	#with open(path, "w") as text_file:
	#	text_file.write("{0}".format(txt))

def text_to_file_(d):
	txt = d['txt']
	path = d['path']
	with open(path, "w") as text_file:
		text_file.write("{0}".format(txt))

def img_to_img_uint8(img):
	return (255.0*z2o(img)).astype(np.uint8)

def zsave_obj(obj, path=None ):
	if path != None:
		print path
	if callable(obj):
		text_to_file('<function>',path+'.fun')
	elif type(obj) == str:
		text_to_file(obj,path+'.txt')
	elif fname(path) == 'img_uint8':
		imsave(path+'.png',obj)
	elif type(obj) == dict:
		assert(path != None)
		unix('mkdir -p '+path)
		for k in obj.keys():
			zsave_obj(obj[k],opj(path,k))
	else:
		save_obj(obj,path)

def zload_obj(path,ctr=0):
	
	print path,ctr
	obj = {}
	txt = sggo(path,'*.txt')
	fun = sggo(path,'*.fun')
	pkl = sggo(path,'*.pkl')
	img_uint8 = sggo(path,'*.png')
	all_files = sggo(path,'*')
	dic = []
	for a in all_files:
		if os.path.isdir(a):
			dic.append(a)
	print dic
	#print txt
	#print fun
	#print pkl
	#print img_uint8
	#print dic
	raw_input('hit enter')
	for k in txt:
		q = '\n'.join(txt_file_to_list_of_strings(k))
		n = fname(k).split('.')[0]
		obj[n] = q
	for k in fun:
		n = fname(k).split('.')[0]
		obj[n] = '<function>'
	for k in pkl:
		n = fname(k).split('.')[0]
		obj[n] = load_obj(k)
	for k in img_uint8:
		n = fname(k).split('.')[0]
		obj[n] = imread(k)
	for k in dic:
		n = fname(k)
		print(dic,n,k,ctr)
		obj[n] = zload_obj(k,ctr+1)

	raw_input('hit enter')
	return obj

def restore_functions(src,dst):
	for k in src.keys():
		if callable(src[k]):
			dst[k] = src[k]
		elif type(src[k]) == dict:
			restore_functions(src[k],dst[k])
		else:
			pass

			