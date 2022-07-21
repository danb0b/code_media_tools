#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 16:47:20 2022

@author: danaukes
"""

import os
import shutil
import yaml

dry_run = False
verbose = True
files_from_to = []

settings = os.path.normpath(os.path.abspath(os.path.expanduser('~/structure_2021.yaml')))

if verbose:
    print('loading structure')
    
with open(settings ,'r') as f:
    info = yaml.load(f,Loader = yaml.Loader)

path_to = '/home/danaukes/Desktop/photos/2021'

files_from_to = []

all_folders = []

for item in info['files']:
    if verbose:
        print(item)
    folder,filename = os.path.split(item)
    file_from = os.path.join(path_to,filename)
    file_to= os.path.join(path_to,item)
    all_folders.append(folder)
    files_from_to.append((file_from,file_to))
    
all_folders = list(set(all_folders))

for item in all_folders:
    if verbose:
        print('make new directory: ',item)
    if not dry_run:
        try:
            os.makedirs(item,exist_ok=True)
        except FileNotFoundError:
            pass
    
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
    
