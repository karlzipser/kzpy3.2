
weight_file_directories = [opjD('home'),opjD('disk'),opjD('disk2')]#[opjh('pytorch_models'),opjm('pytorch_modes')]
weight_file_paths = []
for w in weight_file_directories:
    weight_file_paths += sggo(w,'*.SqueezeNet')


txt = ['#!/bin/bash']
options = "OPTIONS='exit "
for w in weight_file_paths:
	options += fname(w) + ' '
options += "'"
txt.append(options)
txt.append('COLUMNS=12')
txt.append("echo 'network menu:'")
txt.append("select opt in $OPTIONS; do")
txt.append("\tCOLUMNS=12")
if_str = 'if'
for w in weight_file_paths:
   txt.append(d2n("\t",if_str," [ \"$opt\" = '",fname(w),"' ]; then"))
   txt.append(d2n("\t\techo ",w))
   if_str = 'elif'
txt.append(d2n("\telif [ \"$opt\" = 'exit' ]; then"))
txt.append('\tbreak')
txt.append('\telse')
txt.append('\t\techo bad option')
txt.append('\tfi')
txt.append('done')
list_of_strings_to_txt_file(opjD('temp.sh'),txt)


