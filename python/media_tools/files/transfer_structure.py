#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 16:47:20 2022

@author: danaukes
"""

import os
import shutil
import yaml
import argparse

#dry_run = False
#verbose = True
#files_from_to = []

def transfer_structure(input_file,path_to,dry_run=True,verbose=True):
    settings = os.path.normpath(os.path.expanduser(input_file))
    path_to = os.path.normpath(os.path.expanduser(path_to))

    if verbose:
        print('loading structure')
        
    with open(settings ,'r') as f:
        info = yaml.load(f,Loader = yaml.Loader)

    #path_to = '/cloud/drive_stanford/backups/nas/photos/2022/unsorted'

    files_from_to = []

    all_folders = []

    for item in info['files']:
        if verbose:
            print(item)
        folder,filename = os.path.split(item)
        file_from = os.path.join(path_to,filename)
        file_to= os.path.join(path_to,item)
        folder_to= os.path.join(path_to,folder)

        all_folders.append(folder_to)
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
        

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('path',metavar='path',type=str,help='path', default = './')
    parser.add_argument('-v','--verbose',dest='verbose',action='store_true',default = False)
    parser.add_argument('-d','--dry-run',dest='dry_run',action='store_true', default = False)
    #parser.add_argument('-o','--output-file',dest='output_file',default = None)
    parser.add_argument('-i','--input_file',dest='input_file',default = None)
    args = parser.parse_args()
    
    transfer_structure(args.input_file,args.path,args.dry_run,args.verbose)
