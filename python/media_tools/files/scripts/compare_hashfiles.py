#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 09:48:39 2021

@author: danaukes
"""
import media_tools.files.support as fus
import media_tools.files.images as fui
import yaml
import os
import shutil
import argparse



if __name__=='__main__':

    parser = argparse.ArgumentParser()
    
    parser.add_argument('path1',metavar='path1',type=str,help='path1', default = './')
    parser.add_argument('path2',metavar='path2',type=str,help='path2', default = './')
    parser.add_argument('-o','--output-path',dest='output_path',default = None)
    # parser.add_argument('-r','--recursive',dest='recursive',action='store_true', default = False)
    # parser.add_argument('-v','--verbose',dest='verbose',action='store_true', default = False)
    # parser.add_argument('-m','--method',dest='method',default = None)
    # parser.add_argument('-s','--save-hashfile',dest='save_hashfile',action='store_true', default = False)
    
    args = parser.parse_args()

    print(args.path1,args.path2)

    # method = args.method or 'size'
    
    # hashfile_name = None
    
    # if method=='size':
    #     hasher = fus.hash_filesize
    #     if args.save_hashfile:
    #         hashfile_name = 'hash_filesize.yaml'
    # elif method=='sha256':
    #     hasher = fus.hash_file
    #     if args.save_hashfile:
    #         hashfile_name = 'hash_sha256.yaml'
    # else:
    #     raise(Exception('hasher type not valid'))
        
        
    with open(os.path.expanduser(args.path1)) as f:
        local_compare = yaml.load(f,Loader=yaml.Loader)
    with open(os.path.expanduser(args.path2)) as f:
        remote_compare = yaml.load(f,Loader=yaml.Loader)
    
    same_hashes = list(set(local_compare.hashes).intersection(set(remote_compare.hashes)))
    same_names_remote = [filename for key in same_hashes for filename in remote_compare.hash_file_dict[key]]
    same_names_local = [filename for key in same_hashes for filename in local_compare.hash_file_dict[key]]
    
    print('\nSame hashes (local):')
    print(yaml.dump(same_hashes))
    print('\nSame hashes (remote):')
    print(yaml.dump(same_names_remote))
    print('\nSame hashes (local):')
    print(yaml.dump(same_names_local))
    
    
    if args.output_path is not None:
        
        output_path = os.path.expanduser(args.output_path)
        
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            
        with open(os.path.join(os.path.expanduser(args.output_path),'duplicates_local.yaml'),'w') as f:
            yaml.dump(same_names_local,f)
        with open(os.path.join(os.path.expanduser(args.output_path),'duplicates_remote.yaml'),'w') as f:
            yaml.dump(same_names_remote,f)
        
        
        
    # new_local_file_hashes2 = set(local_compare2.hashes).difference(set(same_file_hashes))
    # new_local_file_names2 = [filename for key in new_local_file_hashes2 for filename in local_compare2.hash_file_dict[key]]
    
    # new_local_file_names = list(set(new_local_file_names1+new_local_file_names2))
    
    # new_path = os.path.join(os.path.expanduser('~'),'Desktop','new')
    # if not os.path.exists(new_path):
    #     os.mkdir(new_path)
    # for filename in new_local_file_names:
        
    #     new_file = os.path.join(new_path,os.path.split(filename)[1])
    #     shutil.copy2(filename,new_file)
    # #     # os.rename(filename, new_file)
    # #     # os.remove(filename)
