# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 13:56:52 2019

@author: danaukes
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 08:15:20 2019

@author: danaukes
"""

duplicate_folder_path='C:/Users/danaukes/Desktop/duplicates'

import file_sorter.support as fus
import os
import sys
import yaml
import shutil

force = True

def load_progress(filename):           
    with open(filename,'r') as f:
        source_files,matched_files, unmatched_files = yaml.load(f,Loader=yaml.FullLoader)
    return source_files,matched_files, unmatched_files

filename = 'progress.yaml'

source_files,matched_files, unmatched_files = load_progress(filename)

if not os.path.exists(duplicate_folder_path):
    os.mkdir(duplicate_folder_path)

for file,dummy in matched_files:
    print(file)
    try:
        shutil.move(file,duplicate_folder_path)
    except FileNotFoundError:
        pass
    except OSError as e:
        if 'already exists' in e.args[0]:
            if force:
                fn = os.path.split(file)[1]
                nf = os.path.join(duplicate_folder_path,fn)
                try:
                    shutil.move(file,nf)
                except FileNotFoundError:
                    pass
            else:
                pass
#    os.
    
#            for a,b in f1.readlines(), f2.readlines():
#            a=fa.readline()
#            b=fb.readline()
#   
#results = []         
#for item in comparison_set:
##    print(item)
#    results.append(compare_file_data(*item))
#        
#    
#print('###########################')
#print('unmatched files')
#print(unmatched)