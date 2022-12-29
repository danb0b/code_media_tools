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
import media_tools.gallery.support as support
import subprocess

# listOfImageNames = ['/path/to/images/1.png',
# '/path/to/images/2.png']


# class Image(object):
#     def __init__(self,file):
#         self.file = file

size = 1000, 200
size_non_thumbnail = 1000, 1000

#rebuild_from_scratch=False
# rebuild_from_scratch = True
#rebuild_html_only = False
#crf = None
#crf=21
#crf = 40
#preset = None
#preset = 'slow'
#preset = 'ultrafast'
#verbose = True

import os

def mywalk(top, maxdepth):
    dirs, nondirs = [], []
    for entry in os.scandir(top):
        (dirs if entry.is_dir() else nondirs).append(entry.path)
    yield top, dirs, nondirs
    if maxdepth > 1:
        for path in dirs:
            for x in mywalk(path, maxdepth-1):
                yield x



def fix(input):
    return os.path.normpath(os.path.expanduser(input))


def build(source_root,gallery_root,crf=40,preset='ultrafast',rebuild_from_scratch=True,rebuild_html_only=False,verbose=True,max_depth=100):

    dry_run=False

    #source_root = fix('/cloud/drive_asu_idealab/videos')
    # source_root = fix('/storage/nas/photos/2022')
    # source_root = fix('~/cloud/drive_stanford/library/videos')

    #gallery_root = fix('~/Desktop/gallery')
    # gallery_root = fix('~/Desktop/2022')
    # gallery_root = fix('/home/danaukes/Desktop/library_videos')

    crf = float(crf)
    max_depth = int(max_depth)
    
    source_root = fix(source_root)
    gallery_root = fix(gallery_root)

    if rebuild_from_scratch:
        if os.path.exists(gallery_root):
            shutil.rmtree(gallery_root)

    for folder, subfolders, files in mywalk(source_root,max_depth):
        images = [item for item in files if (os.path.splitext(
            item)[1][1:]).lower() in media_tools.image_filetypes]
        videos = [item for item in files if (os.path.splitext(
            item)[1][1:]).lower() in media_tools.video_filetypes]

        if verbose:
            print(yaml.dump(images))
            print(yaml.dump(videos))

        to_strip = os.path.commonpath([source_root, folder])
        elements = to_strip.split(os.path.sep)
        tail = folder.split(os.path.sep)[len(elements):]
        newfolder = os.path.join(gallery_root, *tail)
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

        markdown_file_path = os.path.join(newfolder, 'index.md')
        html_file_path = os.path.join(newfolder, 'index.html')

        s = ''
        s += '## Subfolders\n\n'
        for item in subfolders:
            s += '* [{0}]({0}/index.html)\n'.format(item)
        s += '\n## Pictures\n\n'
        for item in images:
            a, b = os.path.splitext(item)
            s += '[![]({0})]({1}) '.format(a+'_thumb'+b, item)
        s += '\n\n## Videos\n\n'
        for item in videos:
            a, b = os.path.splitext(item)
            thumb = a+'_thumb.png'
            vid = a+'.mp4'
            s += '[![]({0})]({1}) '.format(thumb, vid)
        with open(markdown_file_path, 'w') as f:
            f.write(s)

        subprocess.run('pandoc "{0}" -o "{1}"'.format(markdown_file_path,
                    html_file_path), capture_output=True, shell=True)

        # to_strip = os.path.normpath(to_strip).split(os.path.sep)

        # os.makedirs()

        bad_photos = []
        jj_last = 0
        if not rebuild_html_only:
            for ii, item in enumerate(images):
                jj = (round(ii/len(images)*100))
                if jj > jj_last:
                    print('\r', jj, end="")

                if verbose:
                    print('process image: ', item, newfolder)

                if not dry_run:
                   support.process_image(item, folder, newfolder,size, size_non_thumbnail, bad_photos)

                jj_last = jj

            for item in videos:
                if verbose:
                    print('process video', item)

                if False:
                    if not dry_run:
                        support.process_video(item, folder, newfolder,crf, preset, rebuild_from_scratch,verbose=False,size=size)

        #     # i.show()
        #     # display(i)
if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    #parser.add_argument('path',metavar='path',type=str,help='path', default = '*.mp4')
    # # parser.add_argument('-p','--path',dest='path',default = '*.mp4')
    # # parser.add_argument('-c','--config',dest='config',default = None)
    # # parser.add_argument('-f','--filetype',dest='filetypes',default = 'mp4')
    # # parser.add_argument('-t','--thumbs',dest='thumbs',action='store_true', default = None)
    parser.add_argument('-i','--input-path',dest='input_path',default = None)
    parser.add_argument('-o','--output-path',dest='output_path',default = None)
    # parser.add_argument('-v','--video_path',dest='video_path',default = None)
    parser.add_argument('-q','--crf',dest='crf',default = '40')
    parser.add_argument('-p','--preset',dest='preset',default = 'ultrafast')
    parser.add_argument('-s','--scratch',dest='scratch',help="rebuild from scratch",action='store_true', default = False)
    parser.add_argument('--html',dest='html',help="rebuild html only",action='store_true', default = False)
    #parser.add_argument('-d','--dry-run',dest='dry_run',help="dry run",action='store_true', default = False)
    parser.add_argument('-v','--verbose',dest='verbose',help="verbose",action='store_true', default = False)
    parser.add_argument('-d','--max-depth',dest='max_depth',help="max depth", default = 100)
    # # parser.add_argument('command',metavar='command',type=str,help='command', default = '')
    # # parser.add_argument('--token',dest='token',default = None)
    args = parser.parse_args()
    # print('path: ',args.path)
    build(args.input_path,args.output_path,args.crf,args.preset,args.scratch,args.html,args.verbose,args.max_depth)
