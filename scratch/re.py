# https://developers.google.com/edu/python/regular-expressions

from kzpy3.utils3 import *

if False:
	str = 'an example word:catt!!'
	match = re.search(r'word:\w\w\w', str)
	if match:
	  print 'found', match.group()
	else:
	  print 'did not find'

	"""
	P|a|b|c

	P[a][b][c]

	D`a``this is a string key`this_is_a_variable_key`0`1``string!` = 47

	`a``this is a string key`this_is_a_variable_key`0`1``string!` = 47
	"""

start = "``abc d`efg``xyzzz MM`arg`0"

implicit_P = r'\b\['
quote_key = r'``([\w\s]+)\b'
non_quote_key = r'`([\w]+)\b'

bracket = r'(\[[\w`\b]+\])'
match = re.findall(bracket, "headings = _[`U_heading_gain`] * U[behavioral_mode][abc_][`index`]][`heading`]")
print match#.group()

b = .[abc,1,2,W[defg,1,2,E[hijk,1,2,3]]]

b = P[abc][1][2][W[defg][1][2][E[hijk][1][2][3]]]

 a = .[`abc d, efg, `Can this state be entered?, argqq, 1, `0 ]

 a = .|`abc d,efg][`Can this state be entered?][argqq][1][`0,|
 a = P[`abc d][efg][`Can this state be entered?][argqq][1][`0]
 a = P["abc d"][efg]["Can this state be entered?"][argqq][1]["0"]

 
 a = P[`abc d][efg][`Can this state be entered?][argqq][1,`0]

 a = P["abc d"][efg]["Can this state be entered?"][argqq][1]["0"]

 l = O|`left_image,`vals,21328|
 |`Verbose,`blue,| = False
 |`Verbose|`blue,|,| = False
 V = Verbose|`blue,|

 .|V,`left image,| = 99
 P|V,`left image,| = 99



b = _/`abc` 1 2 W/`defg` 1 2 E/`hijk` 1 `2` 3]]]	...


A = E[`hijk` 1 `2` 3]	...
B = W[`defg` 1 2 A]]	...
b = _[`abc` 1 2 B]		...

[<

headings = _['U_heading_gain'] * U[ behavioral_mode][_['index']]['heading']

headings = _[`U_heading_gain`] * U[behavioral_mode _[`index`] `heading`]	

A _[`U_heading_gain`]
B = _[`index`]
C = U[ behavioral_mode B `heading`]
headings = A * C

>]




start = " a = P|`abc d,efg,`Can this state be entered,argqq,1,`0|\n"

headings = _[`U_heading_gain`] * U[behavioral_mode _[`index`] `heading`]	...

start = " a = P|`abc d|efg|`xyzzz MM|arg|1|`0`\n"
start = start+start

implicit_P = r'\b(\[)'
quote_key = r'\|`([\w\s]+)\b'
non_quote_key = r'\|([\w]+)\b'


print start
a = start
a = a.replace(' |','P|'); print a
a = re.sub(quote_key,r'["\1"]',start); print a
a = re.sub(non_quote_key,r'[\1]',a); print a
a = a.replace(']`',']'); print a



b = ".[abc,1,2,W[defg,1,2,E[hijk,1,2,3]]]"
b = b.replace('.[','P[')
b = b.replace(',','][')
print b




