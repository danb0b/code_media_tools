#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 16:47:20 2022

@author: danaukes
"""

import os
import shutil
import yaml

path_from = '/storage/nas/photos/2022/unsorted/'
# path_from = '~/Desktop/photos/2022'

path_from = os.path.normpath(os.path.expanduser(path_from))

dry_run = False
verbose = True

files20 = []
for path, subdirs, files in os.walk(path_from):
    if verbose:
        print(path)
    files1 = [os.path.join(path,file) for file in files]
    files2= [item.split(path_from)[1] for item in files1]
    for item in files2:
        if item.startswith('/'):
            files20.append(item[1:])
        else:
            files20.append(item)

settings = os.path.normpath(os.path.abspath(os.path.expanduser('~/structure_2022.yaml')))

info = {}
info['root'] = path_from
info['files'] = files20

with open(settings ,'w') as f:
    yaml.dump(info,f)
    
    
