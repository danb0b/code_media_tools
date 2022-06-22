# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 11:07:21 2021

@author: danaukes
"""
import os
import fitz

import argparse
import glob
import os
import yaml
import subprocess

# path = r'C:\Users\danaukes\Desktop'
# path_out = os.path.join(path,'output')
# os.makedirs(path_out)

# file = os.path.join(path,'biomechanics.pdf')
def save_images(file):
    folder,filename = os.path.split(file)
    filename_plain,my_ext = os.path.splitext(filename)
    extract_folder = os.path.join(folder,filename_plain)
    if not os.path.exists(extract_folder):
        os.makedirs(extract_folder)
    
    doc = fitz.open(file)
    for ii in range(len(doc)):
        jj = 0
        for img in doc.get_page_images(ii):
            xref = img[0]
            filename = os.path.join(extract_folder,"page_{0:03.0f}-{1:02.0f}.png".format(ii,jj))
            pix1 = fitz.Pixmap(doc, xref)
            if (pix1.n - pix1.alpha) < 4:       # this is GRAY or RGB
                pix1.save(filename)
            else:               # CMYK: convert to RGB first
                pix1 = fitz.Pixmap(fitz.csRGB, pix1)
                pix1.save(filename)
                pix1 = None
            pix = None
            jj+=1

if __name__=='__main__':

    parser = argparse.ArgumentParser()
    
    parser.add_argument('path',metavar='path',type=str,help='path', default = '*.pdf')
    # parser.add_argument('-p','--path',dest='path',default = '*.mp4')
    # parser.add_argument('-c','--config',dest='config',default = None)
    # parser.add_argument('-f','--filetype',dest='filetypes',default = 'mp4')
    # parser.add_argument('-t','--thumbs',dest='thumbs',action='store_true', default = None)
    # parser.add_argument('-t','--thumb_path',dest='thumb_path',default = None)
    # parser.add_argument('-v','--video_path',dest='video_path',default = None)
    # parser.add_argument('-q','--crf',dest='crf',default = None)
    # parser.add_argument('-p','--preset',dest='preset',default = None)
    # parser.add_argument('-f','--force',dest='force',action='store_true', default = None)
    # parser.add_argument('command',metavar='command',type=str,help='command', default = '')
    # parser.add_argument('--token',dest='token',default = None)

    args = parser.parse_args()
    print('path: ',args.path)
    # print('config: ',args.config)

    # force = args.force or False
    # path = args.path
    # print('computed path: ',path)
    
    # filetypes = args.filetypes.split(',')
    filenames = glob.glob(os.path.expanduser(args.path))
    # files = [clean_path(file) for file in files]
    print(yaml.dump(filenames))


    for filename in filenames:
        save_images(filename)
    
    # for item in files:
    #     if os.path.splitext(item)[1]=='.yaml':
