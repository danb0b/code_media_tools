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
    # # parser.add_argument('-p','--path',dest='path',default = '*.mp4')
    # # parser.add_argument('-c','--config',dest='config',default = None)
    # # parser.add_argument('-f','--filetype',dest='filetypes',default = 'mp4')
    # # parser.add_argument('-t','--thumbs',dest='thumbs',action='store_true', default = None)
    # parser.add_argument('-t','--thumb_path',dest='thumb_path',default = None)
    parser.add_argument('-v','--verbose',dest='verbose',action='store_true',default = False)
    # parser.add_argument('-q','--crf',dest='crf',default = None)
    # parser.add_argument('-p','--preset',dest='preset',default = None)
    parser.add_argument('-d','--dry-run',dest='dry_run',action='store_true', default = True)
    # # parser.add_argument('command',metavar='command',type=str,help='command', default = '')
    # # parser.add_argument('--token',dest='token',default = None)
    args = parser.parse_args()
    # print('path: ',args.path)
    
    flatten(args.path,args.dry_run,args.verbose)
