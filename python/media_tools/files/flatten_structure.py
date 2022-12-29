#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 19:10:55 2022

@author: danaukes
"""

import os
import shutil
import argparse

#root_path = '/home/danaukes/Desktop/test'

def flatten(path,dry_run=True,verbose=True):

    path = os.path.normpath(os.path.expanduser(path))

    for directory, subdirectories, files in list(os.walk(path,topdown=True))[1:]:
        for file in files:
            file_from = os.path.join(directory,file)
            if verbose:
                print('move ', file_from, 'to ', path)
            if not dry_run:
                try:
                    shutil.move(file_from,path)
                except shutil.Error as e:
                    print(e)
        
if __name__=='__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('path',metavar='path',type=str,help='path', default = './')
    parser.add_argument('-v','--verbose',dest='verbose',action='store_true',default = False)
    parser.add_argument('-d','--dry-run',dest='dry_run',action='store_true', default = False)
    args = parser.parse_args()
    
    flatten(args.path,args.dry_run,args.verbose)
