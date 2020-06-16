# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import PyPDF4 as pypdf

from PIL import Image

#fn='egr_honors_opportunity_document_f2017.pdf'

#if __name__ == '__main__':

def get_images(filepath,op):
    print(op)
    path,file = os.path.split(filepath)
    filename = os.path.splitext(file)[0]

    input1 = pypdf.PdfFileReader(open(filepath, "rb"))

    ii=0
    for jj in range(input1.numPages):

        page0 = input1.getPage(jj)
        xObject = page0['/Resources']['/XObject'].getObject()
    
    
        for obj in xObject:
            if xObject[obj]['/Subtype'] == '/Image':
                
                output_file = '{0}_{1:03.0f}'.format(filename,ii)
                
                output_path_filename = os.path.join(op,output_file)
                print(output_path_filename)
                size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                data = xObject[obj].getData()
                if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                    mode = "RGB"
                else:
                    mode = "P"
    
                if xObject[obj]['/Filter'] == '/FlateDecode':
                    img = Image.frombytes(mode, size, data)
                    img.save(output_path_filename  + ".png")
                elif xObject[obj]['/Filter'] == '/DCTDecode':
                    img = open(output_path_filename  + ".jpg", "wb")
                    img.write(data)
                    img.close()
                elif xObject[obj]['/Filter'] == '/JPXDecode':
                    img = open(output_path_filename + ".jp2", "wb")
                    img.write(data)
                    img.close()
                
                ii+=1
                
                
import os
import sys

directory = 'C:/Users/danaukes/Dropbox (Personal)/scans'
directory = 'C:/Users/danaukes/Dropbox (Personal)/projects/2019-12-27 Recipes'
import glob


#for dirpath, dirnames, filenames, dirnames in os.walk(directory):
pdfs = glob.glob(os.path.join(directory,'*.pdf'))

for filepath in pdfs:
    
    path,file = os.path.split(filepath)
    
    output_path = os.path.normpath(os.path.join(path,'output'))
    
    
    if not os.path.exists(output_path):
        if not os.path.isdir(output_path):
            os.mkdir(output_path)

    get_images(filepath,output_path)
    