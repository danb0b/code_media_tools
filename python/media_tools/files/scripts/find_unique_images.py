# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 13:50:03 2019

@author: danaukes
"""

import media_tools.files.images2 as fui
import media_tools.files.support as fus

path = '/home/danaukes/syncthing/Camera/'
compare_info = fus.scan_list(path, directories_recursive=True,directory_hashfile_name = 'hash.yaml',file_filter=fui.filter_img_filetype,hasher=fui.my_p_hash)
compare_info.save('~/phash.yaml')
compare_info2=fus.HashFile.load('~/phash.yaml')
for key,value in compare_info2.hash_file_dict.items():
    if len(value)>1:
        print(key,value)