# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 20:22:05 2021

@author: danaukes
"""

import PIL
from PIL import Image,  ExifTags
import os
import argparse
import yaml
import shutil
from IPython.display import display
import media_tools
from media_tools.video_tools.shrink_videos import Movie
import subprocess

# listOfImageNames = ['/path/to/images/1.png',
                    # '/path/to/images/2.png']

    
# class Image(object):
#     def __init__(self,file):
#         self.file = file
        
size = 1000,200

rebuild_from_scratch=False
rebuild_html_only = False
crf = None
# crf=21
preset = None
# preset = 'slow'
verbose = False

def get_rotate_amount(exif):
    try:
        tags_inverse = dict([(value.lower(),key) for key,value in ExifTags.TAGS.items()])
        orientation_key = tags_inverse['orientation']
        
        # exif = image.getexif()
    
        if exif[orientation_key] == 3:
            rotate_amount = 180
        elif exif[orientation_key] == 6:
            rotate_amount = 270
        elif exif[orientation_key] == 8:
            rotate_amount = 90
        else:
            rotate_amount = 0

        return rotate_amount

    except (AttributeError, KeyError, IndexError):
        return 0

def fix(input):
    return os.path.normpath(os.path.expanduser(input))
    
source_root = fix('~/cloud/drive_asu_idealab/videos')
# source_root = fix('~/cloud/drive_stanford/library/videos')

gallery_root = fix('~/Desktop/gallery')
# gallery_root = fix('/home/danaukes/Desktop/library_videos')

if rebuild_from_scratch:
    if os.path.exists(gallery_root):
        shutil.rmtree(gallery_root)

for folder,subfolders,files in os.walk(source_root):
    images = [item for item in files if os.path.splitext(item)[1][1:] in media_tools.image_filetypes]
    videos = [item for item in files if os.path.splitext(item)[1][1:] in media_tools.video_filetypes]
    
    if verbose:
        print(yaml.dump(images))
        print(yaml.dump(videos))
    
    to_strip = os.path.commonpath([source_root,folder])
    elements = to_strip.split(os.path.sep)
    tail = folder.split(os.path.sep)[len(elements):]
    newfolder = os.path.join(gallery_root,*tail)
    try:
        os.makedirs(newfolder)
    except FileExistsError:
        if rebuild_from_scratch:
            raise
        else:
            pass

    #images = [item for item in files if os.path.splitext(item)[1][1:] in image_filetypes]
    #videos = [item for item in files if os.path.splitext(item)[1][1:] in video_filetypes]
    
    #print(yaml.dump(images))
    #print(yaml.dump(videos))

    markdown_file_path=os.path.join(newfolder,'index.md')
    html_file_path=os.path.join(newfolder,'index.html')

    s = ''    
    s+='## Subfolders\n\n'
    for item in subfolders:
        s+='* [{0}]({0}/index.html)\n'.format(item)
    s+='\n## Pictures\n\n'
    for item in images:
        s+='[![]({0})]({0}) '.format(item)
    s+='\n\n## Videos\n\n'
    for item in videos:
        thumb = os.path.splitext(item)[0]+'_thumb.png'
        vid = os.path.splitext(item)[0]+'.mp4'
        s+='[![]({0})]({1}) '.format(thumb,vid)
    with open(markdown_file_path,'w') as f:
        f.write(s)

    subprocess.run('pandoc "{0}" -o "{1}"'.format(markdown_file_path,html_file_path),capture_output=True,shell=True)
    
    # to_strip = os.path.normpath(to_strip).split(os.path.sep)
    
    # os.makedirs()
    
    bad_photos = []
    jj_last = 0
    if not rebuild_html_only:
        for ii,item in enumerate(images):
            
            jj = (round(ii/len(images)*100))
            if jj>jj_last:
                print('\r',jj, end = "")
            
            from_file_name = os.path.join(folder,item)
            try:
                i = Image.open(from_file_name)
                e = i.getexif()
                r = get_rotate_amount(e)
                if r in (0,180):
                    i.thumbnail(size)
                else:
                    i.thumbnail(size[::-1])
                if r!=0:
                    i=i.rotate(r, expand=True)
                i.save(os.path.join(newfolder,item))
            #     # i.show()
            #     # display(i)
            except PIL.UnidentifiedImageError:
                bad_photos.append(from_file_name)
            jj_last = jj
        
        for item in videos:
            if verbose:
                print('process video',item)
            movie = Movie(os.path.join(folder,item),video_path = newfolder,thumb_path = newfolder,crf = crf,preset=preset)
            try:
                movie.process(force=rebuild_from_scratch,verbose=verbose)
                i = Image.open(movie.thumb_dest)
                i.thumbnail(size)
                thumb = os.path.splitext(movie.thumb_dest)[0]+'_thumb.png'
                i.save(thumb)
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
    
    