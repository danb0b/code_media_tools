# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 13:48:17 2019

@author: danaukes
"""

import os
import yaml
import support

def read_url(filename):
    strings = []
    with open(filename,'r') as f:
        strings = f.readlines()
    for string in strings:
        if string.lower().startswith('url='):
            string = string.lower().replace('url=','')
            string = string.strip()
            return string
    raise Exception('asedf')
    
def filter_urls(filename):
    return os.path.splitext(filename)[1] in ['.url']
    
        
if __name__=='__main__':
    orig = 'C:/Users/danaukes/Dropbox (Personal)/bookmarks'    
    orig_hashfile = support.scan_compare_dir(orig,hasher = read_url,file_filter = filter_urls, recursive=True)
#    new = 'C:/Users/danaukes/Dropbox (Personal)/bookmarks/to read and sort'
#    new_hashfile = support.scan_compare_dir(new,hasher = read_url,file_filter = filter_urls, recursive=True)
#    a = set(orig_hashfile.hashes)
#    b = set(new_hashfile.hashes)
#    c = list(a.intersection(b))
#    print(c)
#    d=new_hashfile.hash_file_dict[c[0]]