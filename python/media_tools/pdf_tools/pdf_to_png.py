# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 13:01:03 2021

@author: danaukes
"""

import glob
import os
from pdf2image import convert_from_path, convert_from_bytes

from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

pdfs = glob.glob(r'C:\Users\danaukes\papers\PhD-Dissertation\Images\**\**.pdf')

for pdf in pdfs:
    folder,file = os.path.split(pdf)
    file_root,dummy = os.path.splitext(file)
    images = convert_from_path(pdf)
    if len(images)==1:
        index_string = ''
    else:
        index_string = '_{1:03.0f}'

    for ii,image in enumerate(images):
        # i = images[0]
        factor = 1000/image.width
        
        if factor<1:
            image = image.resize((int(factor*image.width),int(factor*image.height)))
        image.save(os.path.join(folder,'{0}{1}.png'.format(file_root,index_string.format(ii))),'png')
