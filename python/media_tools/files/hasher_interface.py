# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 23:49:30 2020

@author: danaukes
"""

import media_tools.files.support as fus
import media_tools.files.images as fui
import yaml
import os
import argparse



if __name__=='__main__':

    parser = argparse.ArgumentParser()
    
    parser.add_argument('path',metavar='path',type=str,help='path', default = './')
    parser.add_argument('-o','--output',dest='output',default = None)
    parser.add_argument('-r','--recursive',dest='recursive',action='store_true', default = False)
    parser.add_argument('-v','--verbose',dest='verbose',action='store_true', default = False)
    parser.add_argument('-m','--method',dest='method',default = 'sha256',help='"size" or "sha256"')
    parser.add_argument('-s','--save-hashfile',dest='save_hashfile',action='store_true', default = False)
    
    args = parser.parse_args()

    method = args.method or 'size'
    
    hashfile_name = None
    
    if method=='size':
        hasher = fus.hash_filesize
        if args.save_hashfile:
            hashfile_name = 'hash_filesize.yaml'
    elif method=='sha256':
        hasher = fus.hash_file
        if args.save_hashfile:
            hashfile_name = 'hash_sha256.yaml'
    else:
        raise(Exception('hasher type not valid'))
    
    
    # parser.add_argument('-p','--preset',dest='preset',default = None)

    # print('path: ',args.path)

    # path1 = r'/home/danaukes/nas/photos/2021'
    # path2 = r'/home/danaukes/nas/photos/2020'
    path = os.path.normpath(os.path.abspath(os.path.expanduser(args.path)))
    if os.path.splitext(path)[1]=='.yaml' or os.path.splitext(path)[1]=='.yml':
        with open(path) as f:
            new_item = yaml.load(f,Loader=yaml.Loader)
    
        if isinstance(new_item,fus.HashFile):
            # hf = fus.HashFile.load(path)
            files = new_item.file_hash_dict.keys()
            duplicates = []
    
            for key,value in new_item.hash_file_dict.items():
                if len(value)>1:
                    duplicates.extend(value)
    
            if args.verbose:
                print('Duplicates to check:',duplicates)
    
            hash1 = fus.scan_list(*duplicates,directories_recursive=args.recursive,file_filter=fus.filter_yaml,hasher=hasher,directory_hashfile_name=hashfile_name,verbose=args.verbose)
        elif isinstance(new_item,list):
            hash1 = fus.scan_list(*new_item,directories_recursive=args.recursive,file_filter=fus.filter_yaml,hasher=hasher,directory_hashfile_name=hashfile_name,verbose=args.verbose)
    else:
        hash1 = fus.scan_list(path,directories_recursive=args.recursive,file_filter=fus.filter_yaml,hasher=hasher,directory_hashfile_name=hashfile_name,verbose=args.verbose)

    # if args.verbose:
    #     print(yaml.dump(hash1))

    if args.output is not None:
        hash1.save(args.output)

    duplicates2 = []

    for key,value in hash1.hash_file_dict.items():
        if len(value)>1:
            duplicates2.extend(value)
            
    if args.verbose:
        print('duplicate hashes:',yaml.dump(duplicates2))
        
        
