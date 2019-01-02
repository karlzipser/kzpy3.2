from kzpy3.utils3 import *

assert 'kpy' in Arguments
assert 'py' in Arguments

##############################################
#
CLASS_STRING = """import WWWWWWWW
exec(identify_file_str)

def XXXXXXXX():
	"XXXXXXXX"
	D = WWWWWWWW.WWWWWWWW()
	CLASS_TYPE = XXXXXXXX.__doc__
	PARENT_TYPE = 'WWWWWWWW'
	dkeys = D.keys()
	for k in dkeys:
		if type(k) != tuple:
			tup = (PARENT_TYPE,k)
			D[tup] = D[k]
	D['entry timer'] = None
	codefilename = d2n('(',fname(__file__),')')
	print '';print ''
	cy('Class',CLASS_TYPE,codefilename)
"""

FUNCTION_STRING = """
	def f########(P):"""

FUNCTION_AUTO_UTILS_STRING = """
		doc = f########.__doc__
		def parent(P):
			tup = (PARENT_TYPE,doc)
			cg('\t\t',tup,D[tup],codefilename)
			return D[tup](P)
		cm('\tfunction',CLASS_TYPE+'::'+doc,codefilename)
			"""

#
##############################################
timer = Timer()
for path in sggo(Arguments['kpy'],'*'):
	modulename = fname(path).split('.')[0]
	cw(opj(Arguments['py'],modulename+'.py'))
	timer.reset()
	codelines = txt_file_to_list_of_strings(path)#opjk('scratch/States/'+modulename+'.kpy'))

	classname = None
	for i in rlen(codelines):
		if '[< Class,' in codelines[i]:
			e = codelines[i].split(',')
			classname = e[-2]
			classparent = e[-1]
			break
	if classname != None:
		codelines[i] = CLASS_STRING.replace('XXXXXXXX',classname).replace('WWWWWWWW',classparent)
		cG('\t',modulename,'line',i,': classname ->',classname,'classparent ->',classparent)

		if True:#if classparent != 'None':
			#codelines[i] = codelines[i].replace("D['depth'] += 1","D['depth'] = 0")
			codelines[i] = codelines[i].replace("import None","")
			codelines[i] = codelines[i].replace("None.None()",'{}')
			cG('\t',modulename,'line',i,': classparent editing')

	function_number = 0
	for i in rlen(codelines):
		if "[< def_Function(P):" in codelines[i]:
			function_number += 1
			codelines[i] = FUNCTION_STRING.replace('########',str(function_number))
			cG('\t',modulename,'line',i,': f'+str(function_number),'editing')

	function_number = 0
	for i in rlen(codelines):
		if "[< function_auto-utils" in codelines[i]:
			function_number += 1
			codelines[i] = FUNCTION_AUTO_UTILS_STRING.replace('########',str(function_number))
			cG('\t',modulename,'line',i,': auto-utils editing')

	for i in rlen(codelines):
		if "[<put_functions_into_D" in codelines[i]:
			newstring = "\tfor f in ["
			for j in range(1,1+function_number):
				newstring += d2n("f",j,',')
			newstring += "]:\n\t\tD[f.__doc__] = f"
			#newstring += "\n\t\tcr(D[f.__doc__])"
			codelines[i] = newstring
	cG('\t',modulename,'line',i,': functions_into_D editing')
	
	list_of_strings_to_txt_file(opj(Arguments['py'],modulename+'.py'),codelines)

	#cg('Adjusted',modulename+'.kpy','to',modulename+'.py','in',timer.time(),'seconds.')

#EOF