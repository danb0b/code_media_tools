# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 13:40:17 2018

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

#ignore = []
#ignore.append('UserComment')
#ignore.append('MakerNote')
#
#whitelist = []
#whitelist.append('width')

screen_grab_sizes = []
screen_grab_sizes.append((640,1136))
screen_grab_sizes.append((750,1334))
screen_grab_sizes.append((1080,1920))
screen_grab_sizes.append((1136,640))
screen_grab_sizes.append((1920,1080))
reverse_keys = dict([value,key] for key,value in PIL.ExifTags.TAGS.items())

extensions = ['.jpg','.png','.jpeg']


def sort_by_key(folder,searchkey,subfilter = None,debug=False):
    return_same = lambda x:x
    subfilter = subfilter or return_same
    files = {}
    
    other_files = {}
#    other_files['noexif']= []
#    other_files['nokey'] = []
#    other_files['screengrab'] = []
    
    
    for filename in os.listdir(folder):
        
        filename2 = os.path.join(folder,filename)
        if not os.path.isdir(filename2):

            if debug:
                print(filename)

            try:
                dummy,ext = os.path.splitext(filename2)
                if ext.lower() in extensions:

                    img = PIL.Image.open(filename2)
    #                print(filename)
                    rect = (img.width,img.height)
    #                print(rect)
                    if rect in screen_grab_sizes:
                        try:
                            other_files['screengrab'].append(filename)
                        except KeyError:
                            other_files['screengrab']=[]
                            other_files['screengrab'].append(filename)
                    else:
    
                        try:
                            exif_data = img._getexif()
                            if exif_data is None:
                                try:
                                    other_files['noexif'].append(filename)
                                except KeyError:
                                    other_files['noexif']=[]
                                    other_files['noexif'].append(filename)
                            else:
                                search_key_rev = reverse_keys[searchkey]
                                if search_key_rev not in exif_data.keys():
                                    try:
                                        other_files['nokey'].append(filename)
                                    except KeyError:
                                        other_files['nokey']=[]
                                        other_files['nokey'].append(filename)
                                else:
                                    filter_key = exif_data[search_key_rev]
                                    filter_key = subfilter(filter_key)
                                    try:
                                        files[filter_key].append(filename)
                                    except KeyError:
                                        files[filter_key] = []
                                        files[filter_key].append(filename)
                        except AttributeError as e:
                            if e.args[0]=="'PngImageFile' object has no attribute '_getexif'":
                                pass
                            else:
                                raise
                    img.close()
            except OSError as e:
                print(e)
    return files,other_files

def group_small_folders(files,num):
    files = files.copy()
    if 'unsorted' not in files:
        files['unsorted'] = []
    for key in list(files.keys()):
        if len(files[key])<num:
            files['unsorted'].extend(files[key])
            del files[key]
    return files
        
            
def move_files(folder,files,debug = False,dry_run=False):
#    print(files)
    #time.sleep(5)
    for key, value in files.items():
        if not not key:
            new_folder = os.path.join(folder,key)
            if not os.path.exists(new_folder):
                if debug:
                    print('make dir: ',new_folder)
                if not dry_run:
                    os.mkdir(new_folder)

            for filename in value:
                if debug:
                    print('move ',filename,' to ',new_folder)
                if not dry_run:
                    try:
                        shutil.move(os.path.join(folder,filename),os.path.join(new_folder,filename))
                    except shutil.SameFileError as f:
                        print(f)
                    except FileNotFoundError as f:
                        print(f)
                
def date_time_to_date(date_time):
    date,time = date_time.split()
    year,month,day = date.split(':')
    date2 = '{0:s}-{1:s}-{2:s}'.format(year,month,day)
    return date2
        

if __name__=='__main__':

    parser = argparse.ArgumentParser()
    
    parser.add_argument('path',metavar='path',type=str,help='path', default = None)
    parser.add_argument('-s','--sort-method',dest='sort_method',help='sort method = "date" or "model(default)"',default = 'model')
    parser.add_argument('-d','--dry-run',dest='dry_run',action='store_true', default = None)
    parser.add_argument('--debug',dest='debug',action='store_true', help='debug = True or False', default = False)
    parser.add_argument('-o','--output',dest='output', help='output filename', default = None)
    parser.add_argument('-i','--input',dest='input', help='input filename', default = None)
    

    args = parser.parse_args()


    date_kwargs = dict(searchkey = 'DateTime',subfilter=date_time_to_date, debug=args.debug)
    model_kwargs = dict(searchkey = 'Model', debug=args.debug)
    kwargss= {'model':model_kwargs,'date':date_kwargs}

    folder = os.path.normpath(os.path.abspath(os.path.expanduser(args.path)))

    if args.debug:
        print('folder: ',folder)
        print('sort method: ',args.sort_method)
        print('debug: ',args.debug)
        print('dry run: ',args.dry_run)
        print('input: ',args.input)
        print('output: ',args.output)

    if not args.input:
        kwargs = kwargss[args.sort_method]
        files2,other_files2  = sort_by_key(folder,**kwargs)
        files3 = group_small_folders(files2,10)
    else:
        with open(os.path.normpath(os.path.expanduser(args.input))) as f:
            files3,other_files2 = yaml.load(f,Loader=yaml.Loader)


    if args.debug:
        # print(files2)
        print(files3.keys())

    move_files(folder,files3,debug = args.debug,dry_run = args.dry_run)
    move_files(folder,other_files2,debug = args.debug,dry_run = args.dry_run)    
    
    if args.output:
        with open(os.path.normpath(os.path.expanduser(args.output)),'w') as f:
            yaml.dump([files3,other_files2],f)