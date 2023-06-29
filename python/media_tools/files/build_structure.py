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

def build_structure(path_in,output_file = None,verbose=True):

    path_in = os.path.normpath(os.path.expanduser(path_in))

    files20 = []
    for path, subdirs, files in os.walk(path_in):
        if verbose:
            print(path)
        files1 = [os.path.join(path,file) for file in files]
        files2= [item.split(path_in)[1] for item in files1]
        for item in files2:
            if item.startswith('/'):
                files20.append(item[1:])
            else:
                files20.append(item)

    info = {}
    info['root'] = path_in
    info['files'] = files20

    if output_file is not None:

        output_file = os.path.normpath(os.path.abspath(os.path.expanduser(output_file)))

        with open(output_file ,'w') as f:
            yaml.dump(info,f)
        

    if verbose or (output_file is None):
        s = yaml.dump(info)
        print(s)
    
if __name__=='__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('path',metavar='path',type=str,help='path', default = './')
    parser.add_argument('-v','--verbose',dest='verbose',action='store_true',default = False)
    parser.add_argument('-o','--output-file',dest='output_file',default = None)
    args = parser.parse_args()

    build_structure(args.path,args.output_file, args.verbose)
