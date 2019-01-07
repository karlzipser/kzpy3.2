from kzpy3.utils2 import *
from kzpy3.misc.All_Names_Module import *

"""
import re

QUOTED_STRING_RE = re.compile(
    r"(?P<quote>['\"])(?P<string>.*?)(?<!\\)(?P=quote)")
regex = r'\b\w+\b'
for line in lines:
	list1 = QUOTED_STRING_RE.findall(line)
	#list1=re.findall(regex,line)
	print list1

regex = r'\b\w+\b'
for line in lines:
	list1=re.fin``````````````dall(regex,line)
	print list1
"""

#regex = r'^[a-zA-Z0-9][ A-Za-z0-9_-]*$'
regex = r'\b\w+\b'
lines = txt_file_to_list_of_strings("/Users/karlzipser/kzpy3/Grapher_app_for_preprocessed_data/Main.py")
changed_lines = []
for line in lines:
	for word in use_words_listv:
		line = line.replace("'"+word+"'",word)
	changed_lines.append(line)
list_of_strings_to_txt_file(opjD('temp1.py'),changed_lines)

lines = txt_file_to_list_of_strings(opjD('temp1.py'))
changed_lines = []
for line in lines:
	var_names = re.findall(regex,line)
	print var_names
	for word in var_names:
		if word in Use_words_dic:
			line = line.replace(word,"'"+word+"'")
	changed_lines.append(line)
list_of_strings_to_txt_file(opjD('temp2.py'),changed_lines)


regex = r'^[a-zA-Z0-9][ A-Za-z0-9_-]*$'

txt = ""
for line in lines:
	txt += line+'\n'


names = [
    node.id for node in ast.walk(ast.parse(txt)) 
    if isinstance(node, ast.Name)
]
#print names
for word in use_words_listv:
	if word in names:
		txt = txt.replace(word,"'"+word+"'")
new_lines = txt.split('\n')
list_of_strings_to_txt_file(opjD('temp.py'),new_lines)

new_lines = []
for line in lines:
	for word in use_words_listv:
		line = line.replace("'"+word+"'",word)
	words = re.findall(regex,line)
	print words
	for w in words:
		if w in Use_words_dic:
			line = line.replace(w,"'"+w+"'")
	new_lines.append(line)
list_of_strings_to_txt_file(opjD('temp.py'),new_lines)


