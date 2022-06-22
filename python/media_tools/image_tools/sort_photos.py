#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 10:19:04 2022

@author: danaukes
"""

import os
import random
import exiftool
import yaml
import argparse
import shutil

def pick_key(file,data,priority):
    keys = data.keys()

    for key in priority:
        if key in keys:
            return key

def get_value(file,data,priority):
    key = pick_key(file, data, priority)

    try:
        value = data[key]
    except KeyError:
        value = None
    return value

def sort_size(size):
    return tuple((sorted(size))[::-1])

def get_size(file,data):
    h_key = pick_key(file,data,height_priority)
    w_key = pick_key(file,data,width_priority)

    try:
        h = data[h_key]
        w = data[w_key]

    except KeyError:
        return None

    return sort_size((w,h))


def date_time_to_date(date_time):
    date,time = date_time.split()
    year,month,day = date.split(':')
    date2 = '{0:s}-{1:s}-{2:s}'.format(year,month,day)
    return date2    
        
screen_grab_sizes = []
screen_grab_sizes.append((1080,1920))
screen_grab_sizes.append((1920,1080))
screen_grab_sizes.append((1242,2688))
screen_grab_sizes.append((1125,2436))
screen_grab_sizes.append((828,1792))
screen_grab_sizes.append((1242,2208))
screen_grab_sizes.append((750,1334))
screen_grab_sizes.append((640,1136))

screen_grab_sizes = [sort_size(item) for item in screen_grab_sizes]


date_priority = ['QuickTime:CreationDate','EXIF:CreateDate']
model_priority = ['EXIF:Model','QuickTime:Model','QuickTime:AndroidModel']
height_priority = ['EXIF:ExifImageHeight','QuickTime:ImageHeight','File:ImageHeight']
width_priority = ['EXIF:ExifImageWidth','QuickTime:ImageWidth','File:ImageWidth']
mime_priority = ['File:MIMEType']

path = '/home/danaukes/nas/photos/2022/'

def get_info(path,recursive = False,sample = None):
    info = {}
    all_directories = list(os.walk(path,topdown=True))
    if not recursive:
        all_directories = all_directories[0:1]
    
        
    for current_path,subdirectories,files, in all_directories:
        full_filenames = [os.path.join(current_path,file) for file in files]
        if sample is not None:
            random.shuffle(full_filenames)
            full_filenames = full_filenames[:int(sample)]

        if not not full_filenames:
        
            with exiftool.ExifToolHelper() as et:
                metadata = et.get_metadata(full_filenames)
        
            for ii,(file,data) in enumerate(zip(full_filenames,metadata)):
                
                model = get_value(file, data, model_priority)

                if not not model:
                    has_model = 'has_model'
                else:
                    has_model = 'no_model'

                mime = get_value(file, data, mime_priority)
                try:
                    mime_class = mime.split('/')[0]
                except AttributeError:
                    mime_class = None
                date_time = get_value(file, data, date_priority)
                try:
                    date = date_time_to_date(date_time)
                except AttributeError:
                    date = None
                size = get_size(file,data)
        
                screengrab='not_screengrab'
                if mime_class=='image':
                    if size in screen_grab_sizes:
                        screengrab='screengrab'
                
                my_info = {}
                my_info['model'] = model
                my_info['has_model'] = has_model
                my_info['date_time'] = date_time
                my_info['date'] = date
                my_info['size'] = size
                my_info['screengrab'] = screengrab
                my_info['mime'] = mime
                my_info['mime_class'] = mime_class
                
                info[file] = my_info
                # print(ii,file, model, date, size, screengrab,mime_class)
    return info

def move_files(folder,files,verbose = False,dry_run=False):
#    print(files)
    #time.sleep(5)
    for key, value in files.items():
        if not not key:
            new_folder = os.path.join(folder,key)
            if not os.path.exists(new_folder):
                if verbose:
                    print('make dir: ',new_folder)
                if not dry_run:
                    os.mkdir(new_folder)

            for filename in value:
                if verbose:
                    print('move ',filename,' to ',new_folder)
                if not dry_run:
                    try:
                        filename_root = os.path.split(filename)[1]
                        shutil.move(filename,os.path.join(new_folder,filename_root))
                    except shutil.SameFileError as f:
                        print(f)
                    except FileNotFoundError as f:
                        print(f)
            
if __name__=='__main__':

    parser = argparse.ArgumentParser()
    
    parser.add_argument('path',metavar='path',type=str,help='path', default = None)
    parser.add_argument('-k','--key',dest='key',help='sort key= "date" or "model(default)"',default = 'model')
    parser.add_argument('-d','--dry-run',dest='dry_run',action='store_true', default = False)
    parser.add_argument('-v','--verbose',dest='verbose',action='store_true', help='debug = True or False', default = False)
    parser.add_argument('-r','--recursive',dest='recursive',action='store_true', help='debug = True or False', default = False)
    parser.add_argument('-o','--output',dest='output', help='output filename', default = None)
    parser.add_argument('--sample',dest='sample', help='sample size per folder', default = None)
    parser.add_argument('-m','--min-folder-num',dest='min_folder_num', help='minimum number of files for a new folder', default = 10)
    parser.add_argument('-i','--input',dest='input', help='input filename', default = None)

    args = parser.parse_args()

    path = os.path.normpath(os.path.abspath(os.path.expanduser(args.path)))

    if args.verbose:
        print('path: ',path)
        print('sort key: ',args.key)
        print('verbose: ',args.verbose)
        print('dry run: ',args.dry_run)
        print('recursive: ',args.recursive)
        print('input: ',args.input)
        print('output: ',args.output)
        print('sample: ',args.sample)
        print('min_folder_num: ',args.min_folder_num)
        
    if not args.input:
            
        info = get_info(path,args.recursive,args.sample)
    
        sorted_info = {}
        
        for file,file_info in info.items():
            key = file_info[args.key]
            try:
                sorted_info[key].append(file)
            except KeyError:
                sorted_info[key] = [file]
    
        try:        
            sorted_info['unsorted'] = sorted_info[None]
            del sorted_info[None]
        except KeyError:
            pass
    
        for key in list(sorted_info):
            value = sorted_info[key]
            if len(value)<int(args.min_folder_num):
                sorted_info['unsorted'].extend(value)
                del sorted_info[key]
                
        if args.output:
            with open(os.path.normpath(os.path.expanduser(args.output)),'w') as f:
                yaml.dump([path,sorted_info],f)    
    else:
        with open(os.path.normpath(os.path.expanduser(args.input))) as f:
            path,sorted_info = yaml.load(f,Loader=yaml.Loader)
        
            
    move_files(path,sorted_info,verbose = args.verbose, dry_run = args.dry_run)
