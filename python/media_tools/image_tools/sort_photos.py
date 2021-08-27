# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 13:40:17 2018

@author: danaukes
"""

import sys
import os
import shutil
#import time

import PIL.Image
import PIL.ExifTags

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

def sort_by_key(folder,searchkey,subfilter = None):
    return_same = lambda x:x
    subfilter = subfilter or return_same
    files = {}
    
    extensions = ['.jpg','.png']
    
    other_files = {}
#    other_files['noexif']= []
#    other_files['nokey'] = []
#    other_files['screengrab'] = []
    
    
    for filename in os.listdir(folder):
        filename2 = os.path.join(folder,filename)
        if not os.path.isdir(filename2):
            try:
                dummy,ext = os.path.splitext(filename2)
                if ext.lower() in extensions:

                    img = PIL.Image.open(filename2)
    #                print(filename)
                    rect = (img.width,img.height)
    #                print(rect)
                    if rect in screen_grab_sizes:
                        try:
                            other_files['screengrab'].append((folder,filename))
                        except KeyError:
                            other_files['screengrab']=[]
                            other_files['screengrab'].append((folder,filename))
                    else:
    
                        try:
                            exif_data = img._getexif()
                            if exif_data is None:
                                try:
                                    other_files['noexif'].append((folder,filename))
                                except KeyError:
                                    other_files['noexif']=[]
                                    other_files['noexif'].append((folder,filename))
                            else:
                                search_key_rev = reverse_keys[searchkey]
                                if search_key_rev not in exif_data.keys():
                                    try:
                                        other_files['nokey'].append((folder,filename))
                                    except KeyError:
                                        other_files['nokey']=[]
                                        other_files['nokey'].append((folder,filename))
                                else:
                                    filter_key = exif_data[search_key_rev]
                                    filter_key = subfilter(filter_key)
                                    try:
                                        files[filter_key].append((folder,filename))
                                    except KeyError:
                                        files[filter_key] = []
                                        files[filter_key].append((folder,filename))
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
        
            
def move_files(folder,files):
#    print(files)
    #time.sleep(5)
    for key, value in files.items():
        if not not key:
            new_folder = os.path.join(folder,key)
            if not os.path.exists(new_folder):
                os.mkdir(new_folder)
            for dirname,filename in value:
                try:
                    shutil.move(os.path.join(dirname,filename),os.path.join(new_folder,filename))
                except shutil.SameFileError:
                    pass
                
def date_time_to_date(date_time):
    date,time = date_time.split()
    year,month,day = date.split(':')
    date2 = '{0:s}-{1:s}-{2:s}'.format(year,month,day)
    return date2
        

if __name__=='__main__':

    date_kwargs = dict(searchkey = 'DateTime',subfilter=date_time_to_date)
    model_kwargs = dict(searchkey = 'Model')
    kwargss= {'model':model_kwargs,'date':date_kwargs}

#    folder,file = os.path.split(sys.argv[0])
#    print('argv: ',os.path.abspath(sys.argv[0]))
    print('curdir: ',os.path.abspath(os.curdir))
    folder = os.path.abspath(os.curdir)

#    print(folder)
    #folder = 'C:\\Users\\danaukes\\Dropbox (ASU)\\camera'
    #folder = 'Y:\\2018\\Sara'
    #folder = 'C:\\Users\\danaukes\\Desktop\\camera'
    #folder = 'C:\\Users\\danaukes\\Desktop\\photos'
#    folder = 'Y:\\2018'
#    folder = 'C:\\Users\\danaukes\\Dropbox (Personal)\\Camera Uploads from Sara'

    if len(sys.argv)>=2:
        kwargs = kwargss[sys.argv[1].lower()]
    else:
        kwargs = dict(searchkey = 'Model')
#    print(kwargs)
    
    files2,other_files2  = sort_by_key(folder,**kwargs)
    print(files2)
    files3 = group_small_folders(files2,10)
    print(files3.keys())

    move_files(folder,files3)
    move_files(folder,other_files2)    