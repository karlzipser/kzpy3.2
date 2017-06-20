# paste this into ipython command line to run

data_folder = 'Desktop/RPi_data/26Jan16_11h20m51s' #'scratch/2015/11/RPi_images/26Jan16_09h13m05s'

l = txt_file_to_list_of_strings(opjh(data_folder,'session_list-'+data_folder.split('/')[-1]+'.txt'))
command_dic = {}
for s in l:
    f = s.split(' ')[0]
    command_dic[f] = s

from kzpy3.vis import *
plt.ion()
img_dic = {}
img_folder = opjh(data_folder,'jpg')
_,img_filenames = dir_as_dic_and_list((opj(img_folder)))
for i in range(0,len(img_filenames)):
    f = img_filenames[i]
    print f
    if f not in img_dic:
        img_dic[f] = imread((opj(img_folder,f)))
    plt.clf()
    mi(img_dic[f],img_title=command_dic[f])
    plt.show()
    
    plt.pause(0.001)
