from kzpy3.utils3 import *



##############################################
#
CLASS_STRING = """import WWWWWWWW
exec(identify_file_str)

def XXXXXXXX():
	"XXXXXXXX"
	D = WWWWWWWW.WWWWWWWW()
	D['depth'] += 1
	dkeys = D.keys()
	if D['depth'] > 0:
		for k in dkeys:
			D['_'+k] = D[k]
	underscore_str = ''
	for i in range(D['depth']):
		underscore_str += '_'
	D['type'] = XXXXXXXX.__doc__
	D['state'] = d2n("'",D['type'],"'")
	D['regarding'] = d2s("Regarding",D['state'])
	D['entry timer'] = None
	cy(D['regarding'],'depth =',D['depth'])
"""

FUNCTION_STRING = """
	def f########(P):"""

FUNCTION_AUTO_UTILS_STRING = """
		doc = f########.__doc__
		cy(D['regarding'],doc)
		def parent(P):
			cg("parent")
			return D[underscore_str+doc](P)"""
#
##############################################
timer = Timer()
for modulename in ['State','Calibrate0']:
	timer.reset()
	codelines = txt_file_to_list_of_strings(opjk('scratch/States/'+modulename+'.kpy'))

	for i in rlen(codelines):
		if '[< Class,' in codelines[i]:
			e = codelines[i].split(',')
			classname = e[-2]
			classparent = e[-1]
			break    
	codelines[i] = CLASS_STRING.replace('XXXXXXXX',classname).replace('WWWWWWWW',classparent)
	if classparent == 'None':
		codelines[i] = codelines[i].replace("D['depth'] += 1","D['depth'] = 0")
		codelines[i] = codelines[i].replace("import None","")
		codelines[i] = codelines[i].replace("None.None()",'{}')

	function_number = 0
	for i in rlen(codelines):
		if "[< def_Function(P):" in codelines[i]:
			function_number += 1
			codelines[i] = FUNCTION_STRING.replace('########',str(function_number))

	function_number = 0
	for i in rlen(codelines):
		if "[< function_auto-utils" in codelines[i]:
			function_number += 1
			codelines[i] = FUNCTION_AUTO_UTILS_STRING.replace('########',str(function_number))

	for i in rlen(codelines):
		if "[<put_functions_into_D" in codelines[i]:
			newstring = "\tfor f in ["
			for j in range(1,1+function_number):
				newstring += d2n("f",j,',')
			newstring += "]:\n\t\tD[f.__doc__] = f"
			#newstring += "\n\t\tcr(D[f.__doc__])"
			codelines[i] = newstring

	list_of_strings_to_txt_file(opjk('scratch/States/'+modulename+'.py'),codelines)

	cg('Adjusted',modulename+'.kpy','to',modulename+'.py','in',timer.time(),'seconds.')

#EOF