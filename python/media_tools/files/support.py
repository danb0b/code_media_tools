# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 09:38:49 2019

@author: danaukes
"""

import os
import yaml

def fix(path_in):
    path_out = os.path.normpath(os.path.abspath(os.path.expanduser(path_in)))
    return path_out


class HashFile(object):
    def __init__(self,hash_file_dict,file_hash_dict,hashes):
        self.hash_file_dict = hash_file_dict
        self.file_hash_dict = file_hash_dict
        self.hashes = hashes
#        self.comparison_type = comparison_type

    @classmethod
    def build(cls,*compare_files,hasher=None,verbose=False):
        compare_hash_dict = {}
        compare_hashes = []
        compare_hash_dict_rev={}
        
        hasher = hasher or hash_filesize 
            
        ii = 0
        l = len(compare_files)
        for filename in compare_files:
            filename = os.path.normpath(filename)
            img_hash= hasher(filename)
            compare_hash_dict[filename] = img_hash
            compare_hashes.append(img_hash)
            if img_hash not in compare_hash_dict_rev:
                compare_hash_dict_rev[img_hash] = [filename]
            else:
                compare_hash_dict_rev[img_hash].append(filename)
            if verbose:
                if ii%10==0:
                    print('getting file info',ii,l)
            ii+=1
        
        compare_hash_set = list(set(compare_hashes))
        new = cls(compare_hash_dict_rev,compare_hash_dict,compare_hash_set)
        
        return new
    
    def save(self,*args):
        with open(os.path.normpath(os.path.expanduser(os.path.join(*args))),'w') as f:
            yaml.dump(self,f)

    @classmethod            
    def load(cls,*args):
        with open(os.path.normpath(os.path.expanduser(os.path.join(*args)))) as f:
            new = yaml.load(f,Loader=yaml.Loader)
        return new
    
    def merge(self,other):
        for key, value in other.hash_file_dict.items():
            if key in self.hash_file_dict:
                self.hash_file_dict[key].extend(value)
            else:
                self.hash_file_dict[key]=value.copy()
        self.file_hash_dict.update(other.file_hash_dict)
        self.hashes.extend(other.hashes)

        
def filter_files(items,file_filter):
    return [item for item in items if (file_filter(item))]

# def scan_file_list(list):
#     return HashFile.build(all_compare_files,hasher)

def dummy(dirpath,dirnames,filenames,verbose,directory_hashfile_name):
    dirpath = fix(dirpath)
    filenames = [os.path.join(dirpath,item) for item in filenames]
    filenames = filter_files(filenames,file_filter)
    
    hash_file = HashFile.build(*filenames,hasher=hasher)
    if directory_hashfile_name is not None:
        hash_file.save(dirpath,directory_hashfile_name)

    if verbose:
        print('finding files',dirpath)

    all_compare_files.extend(filenames)
    global_hash_file.merge(hash_file)


def scan_list(*compare_paths,hasher = None, file_filter = None, directories_recursive=False,directory_hashfile_name = None,verbose=False):
    hasher = hasher or hash_filesize 
    file_filter = file_filter or filter_none
    
    all_compare_files = []    
    global_hash_file = HashFile.build(hasher=hasher)

    for item in compare_paths:
        item = fix(item)
        # print(item)
        if os.path.isdir(item):
            if directories_recursive:
                for dirpath,dirnames,filenames in os.walk(item):
                    dummy(dirpath,dirnames,filenames)
            else:
                dirpath = item
                dirpath = fix(dirpath)
                filenames = os.listdir(dirpath)
                filenames = [os.path.join(dirpath,item) for item in filenames]
                filenames = [item for item in filenames if os.path.isfile(item)]
                filenames = filter_files(filenames,file_filter)
            
                hash_file = HashFile.build(*filenames,hasher=hasher)
                if directory_hashfile_name is not None:
                    hash_file.save(dirpath,directory_hashfile_name)

                if verbose:
                    print('finding files',dirpath)
    
                all_compare_files.extend(filenames)
                global_hash_file.merge(hash_file)

        else:
            hash_file = HashFile.build(item,hasher=hasher)

            if verbose:
                print('finding files',item)

            all_compare_files.append(item)
            global_hash_file.merge(hash_file)
            
    return global_hash_file

def filter_none(filename):
    return True

def filter_yaml(filename):
    fn,ext = os.path.splitext(filename)
    if ext in ['.yaml','.yml']:
        return False
    return True

def hash_filesize(filename):
    size = os.path.getsize(filename)
    return size

def hash_file(filename):
    import hashlib
    
    # file = ".\myfile.txt" # Location of the file (can be set a different way)
    BLOCK_SIZE = 65536 # The size of each read from the file
    
    file_hash = hashlib.sha256() # Create the hash object, can use something other than `.sha256()` if you wish
    with open(filename, 'rb') as f: # Open the file to read it's bytes
        try:
            fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
            while len(fb) > 0: # While there is still data being read from the file
                file_hash.update(fb) # Update the hash
                fb = f.read(BLOCK_SIZE) # Read the next block from the file
        except OSError:
            pass
    
    return file_hash.hexdigest() # Get the hexadecimal digest of the hash
    
    
def check_match(filea,fileb):
    with open(filea,'rb') as  fa:
        with open(fileb,'rb') as  fb:
            result = set(fa).symmetric_difference(fb)
    match= (len(result)==0)
    return match


def save_progress(source_files,matched_files,unmatched_files):           
    with open('progress.yaml','w') as f:
        yaml.dump([source_files,matched_files, unmatched_files],f)

def rebuild_compare_info(*compare_dirs, filename = 'compare_info.yaml',**kwargs):
    if os.path.exists(filename):
        os.remove(filename)
    compare_info = scan_list(*compare_dirs, **kwargs)
    compare_info.save('./',filename)
    
def find_items_with_matching_sizes(compare_size_dict_rev):
    items = []
    for key,value in compare_size_dict_rev.items():
        if len(value)>1:
            items.append((key,value))
    return items

if __name__=='__main__':
    pass