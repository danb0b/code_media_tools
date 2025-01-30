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

def extract(path,dpi):
    pdfs = glob.glob(path)
    print('pdfs: ',pdfs)
    for pdf in pdfs:
        print('pdf:', pdf)
        folder,file = os.path.split(pdf)
        file_root,dummy = os.path.splitext(file)
        output_folder = os.path.join(folder,file_root+'_extract')
        try:
            os.makedirs(output_folder)
        except FileExistsError:
            pass
        dpi = int(dpi)
        images = convert_from_path(pdf,output_folder=output_folder,dpi=dpi,fmt='png',output_file=file_root+'_')
        # if len(images)==1:
        #     index_string = ''
        # else:
        #     index_string = '_{0:03.0f}'
    
        # for ii,image in enumerate(images):
            # i = images[0]
            # factor = 3000/image.width
            
            # if factor<1:
                # image = image.resize((int(factor*image.width),int(factor*image.height)))
            # image.save(os.path.join(folder,'{0}{1}.png'.format(file_root,index_string.format(ii))),'png')


if __name__=='__main__':
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-d','--dpi',dest='dpi',metavar='dpi',type=int,help='dpi', default = 100)
    parser.add_argument('path',metavar='path',type=str,help='path', default = None,nargs='+')

    args = parser.parse_args()

    paths = [os.path.normpath(os.path.expanduser(item)) for item in args.path]
    print('paths: ',paths)
    for path in paths:
        extract(path,args.dpi)
