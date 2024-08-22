# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 11:00:56 2021

@author: danaukes
"""

import file_sorter.support as fus
import file_sorter.images as fui
import yaml
import os
import shutil
import argparse

if __name__=='__main__':

    parser = argparse.ArgumentParser()
    
    parser.add_argument('path',metavar='path',type=str,help='path', default = './')
    # parser.add_argument('-c','--copy',dest='copy',default = None)
    parser.add_argument('-r','--remove',dest='remove',action='store_true', default = None)
    parser.add_argument('-v','--verbose',dest='verbose',action='store_true', default = None)

    args = parser.parse_args()

    path = os.path.normpath(os.path.abspath(os.path.expanduser(args.path)))

    with open(os.path.expanduser(path)) as f:
        local_compare2 = yaml.load(f,Loader=yaml.Loader)
    
    # if args.copy is not None:
    #     copy_path = os.path.normpath(os.path.abspath(os.path.expanduser(args.copy)))
    #     if os.path.exists(copy_path):
    #         if os.path.isdir(copy_path):
    #             pass
    #         else:
    #             raise(Exception('Output Path exists as a file'))
    #     else:
    #         os.makedirs(copy_path)
    

    
    to_remove = []
    to_keep = []
    duplicates = []

    if isinstance(local_compare2,fus.HashFile):


        for key,value in local_compare2.hash_file_dict.items():
            if len(value)>1:
                # print(value)
                duplicates.append(value.copy())
        
        for files in duplicates:
            # l = len(files)
            # where = [1*('recovery' in path) for path in files]
            # m = sum(where)
            keep = files[0]
            to_keep.append(keep)
            if not os.path.exists(keep):
                raise(Exception('re-run!'))
            # toss = files
            # print('keeping: ',keep,'\ntossing: ',files)
            to_remove.extend(files[1:])
            # for item in files[1:]:

    elif isinstance(local_compare2,list):
        to_remove.extend(local_compare2)
        
    if args.verbose:
        print('to keep:\n',yaml.dump(to_keep))
        print('to remove:\n',yaml.dump(to_remove))

    for item in to_remove:
        if os.path.exists(item):
            if args.remove:
                if args.verbose:
                    print('removing: ', item)
                os.remove(item)
        