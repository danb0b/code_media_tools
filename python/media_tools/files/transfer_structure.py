#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 16:47:20 2022

@author: danaukes
"""

import os
import shutil
import yaml

path_from = '/nas/photos/2022/'
path_to = '/cloud/drive_stanford/backups/nas/photos/2022/'

dry_run = False
verbose = True
files_from_to = []

for path, subdirs, files in os.walk(path_from):
    files1 = [os.path.join(path,file) for file in files]
    files2= [item.split(path_from)[1] for item in files1]
    files20 = []
    for item in files2:
        if item.startswith('/'):
            files20.append(item[1:])
        else:
            files20.append(item)
    files3= [os.path.join(path_to,item) for item in files20]
    files4 = [os.path.join(path_to,item) for item in files]
    files_from_to.extend(zip(files4,files3))

settings = os.path.normpath(os.path.abspath(os.path.expanduser('~/structure.yaml')))

with open(settings ,'w') as f:
    yaml.dump(files_from_to,f)
    
    
all_folders = []
    
for file_from, file_to in files_from_to:
    all_folders.append(os.path.split(file_to)[0])

all_folders = list(set(all_folders))

for item in all_folders:
    if verbose:
        print('make new directory: ',item)
    if not dry_run:
        os.makedirs(item,exist_ok=True)
    
for file_from, file_to in files_from_to:
    if verbose:
        print('move ',file_from,' to ',file_to)
    
    if not dry_run:
        try:
            shutil.move(file_from,file_to)
        except shutil.SameFileError as f:
            print(f)
        except FileNotFoundError as f:
            print(f)
    
    # os.makedirs(folders)
    # shutil.move(file_from, file_to)
    
