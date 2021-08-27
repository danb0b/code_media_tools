# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 20:22:05 2021

@author: danaukes
"""

import PIL
from PIL import Image
import os
import argparse
import yaml
import shutil
from IPython.display import display
import media_tools
from media_tools.video_tools.shrink_videos import Movie

# listOfImageNames = ['/path/to/images/1.png',
                    # '/path/to/images/2.png']

    
# class Image(object):
#     def __init__(self,file):
#         self.file = file
        
size = 128, 128


def fix(input):
    return os.path.normpath(os.path.expanduser(input))
    
source_root = fix(r'~\Dropbox (Personal)\Camera Uploads from Sara')
gallery_root = fix('~/Desktop/gallery')

if os.path.exists(gallery_root):
    shutil.rmtree(gallery_root)

for folder,subfolders,files in os.walk(source_root):
    images = [item for item in files if os.path.splitext(item)[1][1:] in media_tools.image_filetypes]
    videos = [item for item in files if os.path.splitext(item)[1][1:] in media_tools.video_filetypes]
    
    print(yaml.dump(images))
    print(yaml.dump(videos))
    
    to_strip = os.path.commonpath([source_root,folder])
    elements = to_strip.split(os.path.sep)
    tail = folder.split(os.path.sep)[len(elements):]
    newfolder = os.path.join(gallery_root,*tail)
    os.makedirs(newfolder)
    # to_strip = os.path.normpath(to_strip).split(os.path.sep)
    
    # os.makedirs()
    
    for item in images:
        i = Image.open(os.path.join(folder,item))
        i.thumbnail(size)
        i.save(os.path.join(newfolder,item))
        
    for item in videos:
        print('process video',item)
        movie = Movie(os.path.join(folder,item),video_path = folder,thumb_path = folder,crf = None,preset=None)
        try:
            movie.process(force=True)
        except FileNotFoundError:
            print('file not found: ',item)
        
    #     # i.show()
    #     # display(i)
    
    
    
if __name__=='__main__':

    pass
    # parser = argparse.ArgumentParser()
    
    # parser.add_argument('path',metavar='path',type=str,help='path', default = '*.mp4')
    # # parser.add_argument('-p','--path',dest='path',default = '*.mp4')
    # # parser.add_argument('-c','--config',dest='config',default = None)
    # # parser.add_argument('-f','--filetype',dest='filetypes',default = 'mp4')
    # # parser.add_argument('-t','--thumbs',dest='thumbs',action='store_true', default = None)
    # parser.add_argument('-t','--thumb_path',dest='thumb_path',default = None)
    # parser.add_argument('-v','--video_path',dest='video_path',default = None)
    # parser.add_argument('-q','--crf',dest='crf',default = None)
    # parser.add_argument('-p','--preset',dest='preset',default = None)
    # parser.add_argument('-f','--force',dest='force',action='store_true', default = None)
    # # parser.add_argument('command',metavar='command',type=str,help='command', default = '')
    # # parser.add_argument('--token',dest='token',default = None)
    # args = parser.parse_args()
    # print('path: ',args.path)
    
    