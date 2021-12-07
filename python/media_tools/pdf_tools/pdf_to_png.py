# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 13:01:03 2021

@author: danaukes
"""

import glob
import os
import argparse
from pdf2image import convert_from_path, convert_from_bytes

from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

def extract(path):
    pdfs = glob.glob(path)
    
    for pdf in pdfs:
        folder,file = os.path.split(pdf)
        file_root,dummy = os.path.splitext(file)
        images = convert_from_path(pdf)
        if len(images)==1:
            index_string = ''
        else:
            index_string = '_{0:03.0f}'
    
        for ii,image in enumerate(images):
            # i = images[0]
            factor = 1000/image.width
            
            if factor<1:
                image = image.resize((int(factor*image.width),int(factor*image.height)))
            image.save(os.path.join(folder,'{0}{1}.png'.format(file_root,index_string.format(ii))),'png')


if __name__=='__main__':
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('path',metavar='path',type=str,help='path', default = None)
    # parser.add_argument('-s','--sort-method',dest='sort_method',help='sort method = "date" or "model(default)"',default = 'model')
    # parser.add_argument('-d','--dry-run',dest='dry_run',action='store_true', default = None)
    # parser.add_argument('--debug',dest='debug',action='store_true', help='debug = True or False', default = False)
    # parser.add_argument('-o','--output',dest='output', help='output filename', default = None)
    # parser.add_argument('-i','--input',dest='input', help='input filename', default = None)
    args = parser.parse_args()

    extract(args.path)