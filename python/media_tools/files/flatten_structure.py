#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 19:10:55 2022

@author: danaukes
"""

import os
import shutil

verbose = False
dry_run = False

root_path = '/home/danaukes/Desktop/test'

for directory, subdirectories, files in list(os.walk(root_path,topdown=True))[1:]:
    for file in files:
        file_from = os.path.join(directory,file)
        if verbose:
            print('move ', file_from, 'to ', file_to)
        if not dry_run:
            try:
                shutil.move(file_from,root_path)
            except shutil.Error as e:
                print(e)
        