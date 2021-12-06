#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 21:17:11 2021

@author: danaukes
"""

import sys
import os
import shutil
#import time
import yaml

import PIL.Image
import PIL.ExifTags

import argparse
reverse_keys = dict([value,key] for key,value in PIL.ExifTags.TAGS.items())
# extensions = ['.jpg','.png','.jpeg']

def get_info(path):
    img = PIL.Image.open(path)
    exif_data = img._getexif()
    exif2 = {}
    for key,value in exif_data.items():
        exif2[PIL.ExifTags.TAGS[key]]=value
    
    # if exif_data is None:
        # pass


    # search_key_rev = reverse_keys[searchkey]

    return exif2


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('path',metavar='path',type=str,help='path', default = None)
    
    args = parser.parse_args()
    
    path = os.path.normpath(os.path.expanduser(args.path))
    exif_data = get_info(path)
    s = yaml.dump(exif_data)
    print(s)