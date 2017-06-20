#! //anaconda/bin/python

from kzpy3.utils import *

"""
[integer]-[subimage letter]-[whatever]{optional: __[integer]}.['png' or 'jpg']

from the latex doc folder:


python ~/kzpy3/scratch/latex_formatter3.py -b -o

#ln -s ~/Google_Drive/2015-11/Zipser.bib .
"""

path = os.getcwd()#sys.argv[1]

try:
	latex_formatter_mode = txt_file_to_list_of_strings(opj(path,'.Zipser_latex_mode'))[0]
except:
	sys.exit("""


**** Error, unable to load hidden file .Zipser_latex_mode . . .
Perhaps """+path+""" is not a LaTex doc directory?""")
print('Using ' + latex_formatter_mode)

if latex_formatter_mode != 'latex_formatter3_22Nov2015':
	sys.exit(d2s('*** Error,',latex_formatter_mode,' is an unknown formatter mode'))

unix("ln -s ~/Google_Drive/2015-11/Zipser.bib .")

dir_dic,dir_lst=dir_as_dic_and_list(opj(path,'figures'))

figure_dic = {}

print('Figure files:')

for l in dir_lst:
	a = l.split('.')[0].split('-')
	t = l.split('.')[-1]
	
	if t == 'png' or t == 'jpg' or t == 'pdf':
		if a[0].isdigit():
			
			if len(l.split('.')[0].split('__')) > 1:
				#print('HERE!!!!!!!')
				w = np.float(l.split('.')[0].split('__')[-1])
			else:
				w = 30
			
			s = a[1]
			n = int(a[0])
			#print((a,n,s,t))
			print(d2n('\t',l))
			if n not in figure_dic:
				figure_dic[n] = {}
				figure_dic[n]['subfigures'] = {}
			figure_dic[n]['subfigures'][s] = {}
			figure_dic[n]['subfigures'][s]['filename'] = l
			figure_dic[n]['subfigures'][s]['width'] = np.float(w/100.0)

_,legend_dir_lst=dir_as_dic_and_list(opj(path,'text','legends'))

for l in legend_dir_lst:
	a = l.split('.')
	t = a[-1]
	if t == 'txt':
		n = int(a[0])
		txt = txt_file_to_list_of_strings(opj(path,'text','legends',l))
		main_txt = []
		for tx in txt:
			txs = tx.split('|')
			#print txs
			if len(txs) > 1:
				figure_dic[n]['subfigures'][txs[1]]['txt'] = txs[2]
			else:
				main_txt.append(tx)
		figure_dic[n]['txt'] = main_txt

#print(figure_dic)

title_text = txt_file_to_list_of_strings(opj(path,'text','title.txt'))[0]
author_text_lst = txt_file_to_list_of_strings(opj(path,'text','authors.txt'))
author_text = """"""
for t in author_text_lst:
	author_text += t+"\n"


a = """
\\documentclass[11pt, oneside]{article}   	% use "amsart" instead of "article" for AMSLaTeX format
\\usepackage{geometry}                		% See geometry.pdf to learn the layout options. There are lots.
\\geometry{letterpaper,margin=1.2in}                   		% ... or a4paper or a5paper or ... 
\\usepackage[margin=0.5in]{caption}
%\\geometry{landscape}                		% Activate for rotated page geometry
\\usepackage[parfill]{parskip}    		% Activate to begin paragraphs with an empty line rather than an indent
\\usepackage{graphicx}				% Use pdf, png, jpg, or eps with pdflatex; use eps in DVI mode
\\usepackage[font=normal,skip=6pt]{caption}
\\usepackage{subcaption}
\\graphicspath{ {.}}
								% TeX will automatically convert eps --> pdf in pdflatex		
\\usepackage{amssymb}
\\usepackage{natbib}
\\usepackage{authblk}
%SetFonts
\\renewcommand*\\rmdefault{phv}

%SetFonts
\\title{\\vspace{-2cm}\\textbf{"""+title_text+"""}}

\\author{"""+author_text+"""}
\\affil{Redwood Center for Theoretical Neuroscience, U.C. Berkeley\\\ California, U.S.A.\\\ karlzipser@berkeley.edu}
\\renewcommand\Affilfont{\itshape\small}

%\\date{}							% Activate to display a given date or no date

\\begin{document}
\\maketitle

%%%%%%%%%%%%%%%%%%%
%
\\begin{abstract}
%\\it
\\noindent
"""


txt = txt_file_to_list_of_strings(opj(path,'text','abstract.txt'))
for t in txt:
	a += t
a = a +"""\\end{abstract}
%
%%%%%%%%%%%%%%%%%%%
"""

sections = ['introduction','methods','results','discussion']

for s in sections:
	a = a + """
%%%%%%%%%%%%%%%%%%%
%
\\section*{"""+s[0].upper()+s[1:]+"""}

"""
	txt = txt_file_to_list_of_strings(opj(path,'text',s+'.txt'))
	for t in txt:
		a += t + "\n"
	a = a + """
%
%%%%%%%%%%%%%%%%%%%
"""

a = a + """
\\bibliographystyle{natbib}
\\bibliography{Zipser}
\\end{document} 
"""

body_str = a

#fig_str_dic = {}
ns = sorted(figure_dic.keys())
for n in ns:
	a=""""""
	caption = ""
	for c in figure_dic[n]['txt']:
		caption += c + "\n"
	a = a + """
%%%%%%%%%%%%%%%%%%%%%%%%%
%
\\begin{figure}[!tbp]"""
	if len(figure_dic[n]['subfigures'].keys()) > 1:
		for s in sorted(figure_dic[n]['subfigures'].keys(),key=natural_keys):
			#print(n,s)
			if 'txt' in figure_dic[n]['subfigures'][s]:
				sub_caption = figure_dic[n]['subfigures'][s]['txt']
			else:
				sub_caption = ""
			a = a + """
  \\begin{subfigure}{"""+str(figure_dic[n]['subfigures'][s]['width'])+"""\\textwidth}
    \\includegraphics[width=\\textwidth]{figures/"""+figure_dic[n]['subfigures'][s]['filename']+"""}
    \\caption{"""+sub_caption+"""}
    \\label{fig:"""+str(n)+s+"""}
  \\end{subfigure}"""
	else:
		s = figure_dic[n]['subfigures'].keys()[0]
		a = a + """
    \\includegraphics[width="""+str(figure_dic[n]['subfigures'][s]['width'])+"""\\textwidth]{figures/"""+figure_dic[n]['subfigures'][s]['filename']+"""}"""
  	a = a + """
  \\centering
  \\caption{"""+caption+"""}
  \\label{fig:"""+str(n)+"""}
\end{figure}
%
%%%%%%%%%%%%%%%%%%%%%%%%%
"""
#	fig_str_dic[n] = a
	body_str = body_str.replace(d2n('<<FIGURE ',n,'>>'),a)
#print(a)
output_file_path = opj(path,'Zipser.tex')
print(d2s('******** Writing to',output_file_path))
list_of_strings_to_txt_file(output_file_path,[body_str])
#unix(d2s('open',opj(path,'main.tex')))

sys_argv = sys.argv
if len(sys_argv) < 2: # Add default argumets if none provided.
	sys_argv.append('-b')
	sys_argv.append('-o')

for i in range(1,len(sys.argv)):
	if sys.argv[i] == '-b':
		print("******** Run in bibliography mode.")
		unix('/Library/TeX/texbin/pdflatex Zipser')
		unix('/Library/TeX/texbin/bibtex Zipser')
		unix('/Library/TeX/texbin/pdflatex Zipser')
		unix('/Library/TeX/texbin/pdflatex Zipser')
		unix('/Library/TeX/texbin/pdflatex Zipser')
		
unix('/Library/TeX/texbin/pdflatex Zipser')

"""
for i in range(1,len(sys.argv)):
	if sys.argv[i] == '-o':
		print('******** Open pdf')
		unix('open Zipser.pdf')
"""

for i in range(1,len(sys.argv)):
	if sys.argv[i] == '-o':
		print('******** Open pdf')
		osa('tell app "Preview" to close front window')
		unix('open Zipser.pdf')

