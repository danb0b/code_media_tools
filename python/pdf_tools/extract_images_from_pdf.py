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
        # for key,value in 
        print(jj)
        try:

            xObjects = page0['/Resources']['/XObject']
        
            for key,value in xObjects.items():
                xObject = value.getObject()
                if xObject['/Subtype'] == '/Image':
                    
                    output_file = '{0}_{1:03.0f}'.format(filename,ii)
                    
                    output_path_filename = os.path.join(op,output_file)
                    print(output_path_filename)
                    size = (xObject['/Width'], xObject['/Height'])
                    data = xObject.getData()
                    if xObject['/ColorSpace'] == '/DeviceRGB':
                        mode = "RGB"
                    else:
                        mode = "P"
        
                    if xObject['/Filter'] == '/FlateDecode':
                        img = Image.frombytes(mode, size, data)
                        img.save(output_path_filename  + ".png")
                    elif xObject['/Filter'] == '/DCTDecode':
                        img = open(output_path_filename  + ".jpg", "wb")
                        img.write(data)
                        img.close()
                    elif xObject['/Filter'] == '/JPXDecode':
                        img = open(output_path_filename + ".jp2", "wb")
                        img.write(data)
                        img.close()
                    
                    ii+=1

        except KeyError:
            pass
                
import os
import sys

# directory = 'C:/Users/danaukes/Dropbox (Personal)/scans'
# directory = 'C:/Users/danaukes/Dropbox (Personal)/projects/2019-12-27 Recipes'
# directory = r'G:\My Drive\classes\2020-2021-S-EGR-557-foldable-robotics\shared documents\course-documents'

import glob


#for dirpath, dirnames, filenames, dirnames in os.walk(directory):
# pdfs = glob.glob(os.path.join(directory,'*.pdf'))

pdfs = [r'G:\My Drive\classes\2020-2021-S-EGR-557-foldable-robotics\shared documents\course-documents\2021_Intro_Bio_small.pdf']
for filepath in pdfs:
    
    path,file = os.path.split(filepath)
    
    output_path = os.path.normpath(os.path.join(path,'output'))
    
    
    if not os.path.exists(output_path):
        if not os.path.isdir(output_path):
            os.mkdir(output_path)

    get_images(filepath,output_path)
    