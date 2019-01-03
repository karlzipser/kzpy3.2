from kzpy3.utils3 import *



require_Arguments(['kpy','py'])

##############################################
#
CLASS_STRING = """import WWWWWWWW
exec(identify_file_str)

def XXXXXXXX(D):
	"XXXXXXXX"
	CLASS_TYPE = XXXXXXXX.__doc__
	D['depth'] = D[(PARENT_TYPE,'depth')] + 1
	indent = ''
	codefilename = d2n('(',fname(__file__),')')
"""

FUNCTION_STRING = """
	def f########(D,P):"""

FUNCTION_AUTO_UTILS_STRING = """
		doc = f########.__doc__
		cw(indent+CLASS_TYPE+'::'+doc,codefilename)
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
			classname = e[-1]
			break
	if classname != None:
		codelines[i] = CLASS_STRING.replace('XXXXXXXX',classname)
		cG('\t',modulename,'line',i,': classname ->',classname)

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
			newstring += "]:\n\t\tD[(",classname,"f.__doc__)] = f"
			#newstring += "\n\t\tcr(D[f.__doc__])"
			codelines[i] = newstring
	cG('\t',modulename,'line',i,': functions_into_D editing')
	
	list_of_strings_to_txt_file(opj(Arguments['py'],modulename+'.py'),codelines)

	#cg('Adjusted',modulename+'.kpy','to',modulename+'.py','in',timer.time(),'seconds.')

#EOF